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
        "diameter": diameter*3.3,
        "hub_height": hub_height,
        "layout_x": layout_x,
        "layout_y": layout_y,
        "n_turbines": n_turbines
    }

if __name__ == "__main__":
    pass