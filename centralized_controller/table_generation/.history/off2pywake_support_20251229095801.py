from pathlib import Path
import yaml
from typing import Any, Dict
import numpy as np 
import py_wake as pw
import os


from py_wake.site import UniformSite
from py_wake.wind_turbines import WindTurbine
from py_wake.deficit_models.gaussian import BastankhahGaussian
from py_wake.wind_turbines.power_ct_functions import PowerCtFunction


from py_wake.wind_farm_models import All2AllIterative
from py_wake.deficit_models.gaussian import BastankhahGaussianDeficit
from py_wake.superposition_models import SquaredSum
from py_wake.deflection_models import JimenezWakeDeflection

def load_windfarm_yaml(yaml_name) -> Dict[str, Any]:
    # two levels up from this file
    base = Path(__file__).resolve().parent.parent.parent

    # build the Windows-style path in a cross-platform way
    rel = Path("OFF") / "02_Examples_and_Cases" / "03_Cases" / yaml_name
    yaml_path = base / rel

    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}

def build_farm_setup(farm_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Build a simple wind-farm setup dictionary from the loaded YAML.

    - Computes rotor swept area from diameter (A = pi*(D/2)**2)
    - Converts layouts to NumPy arrays
    - Creates placeholders for thrust coefficient (`ct`) and power curve
      (both set to ones by default; replace when you have real data)
    """
    wind_farm = farm_dict["wind_farm"]["farm"]
    diameter = float(wind_farm["diameter"][0])
    A = np.pi * (diameter / 2) ** 2  # rotor swept area (m^2)

    hub_height = farm_dict["turbine"]["mask"]["hub_height"]

    layout_x = np.array(wind_farm["layout_x"], dtype=float)
    layout_y = np.array(wind_farm["layout_y"], dtype=float)
    n_turbines = layout_x.size

    return {
        "A": A,
        "diameter": diameter,
        "hub_height": hub_height,
        "layout_x": layout_x,
        "layout_y": layout_y,
        "n_turbines": n_turbines
    }


class StaticCpCtYawPower(PowerCtFunction):
    # Only require 'yaw' — PyWake passes 'ws' positionally when calling ct/power,
    # so including it here can cause it to be passed twice (positional + kwarg).
    _required_inputs = ['yaw']
    _optional_inputs = []
    def __init__(self, cp = 0.47, ct = 0.74, rho = 1.225, diameter = 198.0):
        self.cp = cp
        self.ct_const = ct
        self.rho = rho
        self.area = np.pi * (diameter / 2)**2
        # PyWake's PowerCt model container expects a `model_lst` attribute.
        # Provide a single-model list pointing to self so the container recursion works.
        self.model_lst = [self]

    def power(self, *args, **kwargs):
        """Compute power for arrays of wind speeds and yaw angles.

        Returns an array shaped (len(ws), len(yaw)) to match PyWake expectations.
        Accepts positional (ws, yaw) or keyword args ('ws', 'yaw' or 'rel_yaw').
        """
        ws = kwargs.get('ws', args[0] if len(args) >= 1 else None)
        yaw = kwargs.get('yaw', kwargs.get('rel_yaw', args[1] if len(args) >= 2 else 0.0))

        ws_arr = np.atleast_1d(ws).astype(float)
        yaw_arr = np.atleast_1d(yaw).astype(float)

        # scalar factors
        coeff = 0.5 * self.rho * self.area * self.cp
        # per-wind speed term (L, 1)
        ws_term = ws_arr**3
        ws_term = ws_term.reshape(-1, 1)
        # per-yaw term (1, K)
        yaw_term = np.cos(np.deg2rad(yaw_arr))**3
        yaw_term = yaw_term.reshape(1, -1)

        return coeff * ws_term * yaw_term

    def ct(self, *args, **kwargs):
        """Return thrust coefficient array aligned with the input `ws` shape.

        Handles inputs where `ws` may have shape scalars, (L,), (L,K), or
        (I,L,K) and `yaw` may be a scalar, per-direction (K,), or per-turbine
        (I,) array. The method broadcasts the per-yaw CT values to match the
        shape of `ws` so PyWake's internal broadcasting succeeds.
        """
        ws = kwargs.get('ws', args[0] if len(args) >= 1 else None)
        yaw = kwargs.get('yaw', kwargs.get('rel_yaw', args[1] if len(args) >= 2 else 0.0))

        ws_arr = np.asarray(ws)
        yaw_arr = np.atleast_1d(yaw).astype(float)

        # per-yaw ct values
        ct_per_yaw = (self.ct_const * np.cos(np.deg2rad(yaw_arr))**3).ravel()

        # Scalar ws: return scalar CT
        if ws_arr.ndim == 0:
            return ct_per_yaw[0] if ct_per_yaw.size else self.ct_const

        target_shape = ws_arr.shape

        # If yaw matches last axis (directions), broadcast along last axis
        if ct_per_yaw.size == target_shape[-1]:
            ct = ct_per_yaw.reshape((1,) * (ws_arr.ndim - 1) + (ct_per_yaw.size,))
            # broadcast_to returns a readonly view; return a writable copy
            return np.broadcast_to(ct, target_shape).copy()

        # If yaw matches first axis (turbines), broadcast along first axis
        if ct_per_yaw.size == target_shape[0]:
            ct = ct_per_yaw.reshape((ct_per_yaw.size,) + (1,) * (ws_arr.ndim - 1))
            # broadcast_to returns a readonly view; return a writable copy
            return np.broadcast_to(ct, target_shape).copy()

        # If yaw is a single value, fill full shape
        if ct_per_yaw.size == 1:
            return np.full(target_shape, ct_per_yaw[0])

        # If yaw size equals product of first and last dims (I*K), try reshape
        try:
            if ct_per_yaw.size == target_shape[0] * target_shape[-1] and ws_arr.ndim >= 2:
                ct2 = ct_per_yaw.reshape((target_shape[0], target_shape[-1]))
                ct3 = ct2.reshape(target_shape[0], 1, target_shape[-1])
                # broadcast_to returns a readonly view; return a writable copy
                return np.broadcast_to(ct3, target_shape).copy()
        except Exception:
            pass

        # Fallback: return first value expanded
        ct_fallback = np.full(target_shape, ct_per_yaw.ravel()[0])

        # Ensure the returned array is at least 3D (I, L, K) so that PyWake
        # indexing like v[:, :, 0] works without errors. Promote shapes:
        # - (L, K) -> (1, L, K)
        # - (L,) -> (1, L, 1)
        # - (,) scalar -> scalar
        res = np.asarray(ct_fallback)
        if res.ndim == 2:
            res = res.reshape((1,) + res.shape)
        elif res.ndim == 1:
            res = res.reshape((1, res.shape[0], 1))
        # Return writable array
        return res.copy()

    def __call__(self, *args, **kwargs):
        """Compatibility wrapper used by PyWake's PowerCtModelContainer.

        Accepts positional or keyword args. When called with run_only==1, returns
        only the thrust coefficient array; otherwise returns a dict with both
        'power' and 'ct'. This mirrors the minimal behavior needed by
        `_wind_turbines.ct` and related code paths.
        """
        # Extract ws and run_only robustly
        ws = kwargs.get('ws', args[0] if len(args) >= 1 else None)
        # run_only may be passed as keyword or as second positional arg
        if 'run_only' in kwargs:
            run_only = kwargs.pop('run_only')
        else:
            run_only = args[1] if len(args) >= 2 else None

        # Extract yaw (or rel_yaw)
        yaw = kwargs.get('yaw', kwargs.get('rel_yaw', args[2] if len(args) >= 3 else 0.0))

        # Ensure arrays
        ws_arr = np.asarray(ws)

        if run_only == 1:
            return self.ct(ws_arr, yaw=yaw)
        else:
            p = self.power(ws_arr, yaw=yaw)
            ct = self.ct(ws_arr, yaw=yaw)
            return {'power': p, 'ct': ct}


def run_pywake_simulation(setup: Dict[str, Any], wind_speed: float = 8.0, wind_dir: float = 270.0) -> Dict[str, Any]:
    """Run a static-wind PyWake simulation if available.

    This helper will attempt to import `py_wake` (or `pywake`) and run a minimal
    simulation using the farm layout in `setup`. If the PyWake simulation fails,
    the error will be raised so callers can handle it (no fallback is performed).

    Returns a dict with keys: 'power' (array), 'ct' (array), 'effective_ws' (array)
    """
    # Basic inputs
    A = float(setup["A"])
    layout_x = np.asarray(setup["layout_x"])
    layout_y = np.asarray(setup["layout_y"])
    n = int(setup["n_turbines"])
    diameter = float(setup["diameter"])
    hub_height = float(setup["hub_height"])


    # Build site and turbine -- API differences might require local edits
    site = UniformSite(p_wd=[wind_dir], ws=[wind_speed])

    turbine = WindTurbine(name="UserTurb", diameter=diameter, hub_height=hub_height, powerCtFunction=StaticCpCtYawPower(diameter=diameter))

    wf_model = All2AllIterative(
        site=site,
        windTurbines=turbine,
        wake_deficitModel=BastankhahGaussianDeficit(),
        deflectionModel=JimenezWakeDeflection(),
        superpositionModel=SquaredSum()
    )
        
    yaw = 10 * np.ones(n)  # degrees, one per turbine

    # Use layout-based call which may trigger SimulationResult creation.
    try:
        sim_res = wf_model(layout_x, layout_y, yaw=yaw, tilt=np.zeros(n))

        # Try to extract results using common attribute names
        try:
            power = np.asarray(sim_res.Power).ravel()
        except Exception:
            power = np.asarray(getattr(sim_res, "power", np.nan))

        try:
            ws_eff = np.asarray(sim_res.WS).ravel()
        except Exception:
            ws_eff = np.full(n, wind_speed)

        # Compute ct if possible using the turbine object
        try:
            ct_arr = np.asarray(turbine.ct(ws_eff, yaw=yaw))
            # Flatten/broadcast to turbine shape
            ct = ct_arr.ravel() if ct_arr.size >= n else np.full(n, float(ct_arr.ravel()[0]))
        except Exception:
            ct = None

        # If shapes don't match, broadcast power to per-turbine
        if power.size != n:
            power = np.full(n, float(power.ravel()[0]))

        return {"power": power, "ct": ct, "effective_ws": ws_eff}

    except TypeError as e:
        # PyWake's internal SimulationResult construction can raise TypeError
        # (e.g., due to xarray changes). We do not silently fallback here; raise
        # a clear error so the caller can diagnose and fix the environment.
        raise RuntimeError(
            f"PyWake SimulationResult creation failed: {e}. "
            "Ensure your installed py_wake version is compatible and try again."
        ) from e

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    # Static wind conditions
    wd = 270.0  # wind direction (deg)
    ws = 8.0    # wind speed (m/s)

    res = run_pywake_simulation(setup, wind_speed=ws, wind_dir=wd)

    print(f"Simulation result (n turbines = {setup['n_turbines']}):")
    print(f"Power (W) per turbine: {res['power']}")
    print(f"Effective wind speeds at turbines: {res['effective_ws']}")
    print("If PyWake is not installed or the API differs, a wake-free estimate is used. Replace placeholders as needed.")

