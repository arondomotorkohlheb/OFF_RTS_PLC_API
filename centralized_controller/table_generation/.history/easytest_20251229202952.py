import numpy as np
import matplotlib.pyplot as plt

# import and setup site and windTurbines
from py_wake.site import UniformSite
from off2pywake_support import build_farm_setup, load_windfarm_yaml
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.wind_turbines import WindTurbines
import py_wake
from py_wake import BastankhahGaussian
from py_wake.examples.data.iea37._iea37 import IEA37Site, IEA37_WindTurbines
from py_wake.examples.data.hornsrev1 import V80

site = IEA37Site(16)
windTurbines = V80()
D = windTurbines.diameter()


def plot_deflection(deflectionModel):

    ws = 8  # wind speed
    wd = 200  # wind direction
    ti = 0  # turbulence intensity

    
    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    site = IEA37Site(16)
    site = UniformSite(ws=ws, ti=ti)
    x, y = [0, 400, 800], [0, 0, 0]
    D = setup["diameter"]


    
    ws_array = np.array([ws])
    power = np.array([0.47*ws**3*setup["A"]*1.225])  # in MW
    ct = np.array([0.74])

    power_ct = PowerCtTabular(ws = ws_array, power = power, ct = ct, power_unit='MW')


    windTurbines = WindTurbines(
        names=['Turbine'],
        diameters=[setup["diameter"]],
        hub_heights=[setup["hub_height"]],
        powerCtFunctions=[power_ct]
    )


    wfm = BastankhahGaussian(site, windTurbines, deflectionModel=deflectionModel)

    yaw = [-20,20,0]

    plt.figure(figsize=(14,4))
    fm = wfm(x, y, yaw=yaw, tilt=0, wd=270, ws=10).flow_map()
    fm.plot_wake_map(normalize_with=D)
    center_line = fm.min_WS_eff()
    plt.plot(center_line.x/D, center_line/D,'--k')
    plt.grid()
    return None

    ws = 8  # wind speed
    wd = 200  # wind direction
    ti = 0  # turbulence intensity

    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    # site = UniformSite(ws=ws, ti=ti) # wd is given later in the simulation
    site = IEA37Site(16)


    ws_array = np.array([ws])
    power = np.array([0.47*ws**3*setup["A"]*1.225])  # in MW
    ct = np.array([0.74])

    power_ct = PowerCtTabular(ws = ws_array, power = power, ct = ct, power_unit='MW')

    windTurbines = WindTurbines(
        names=['Turbine'],
        diameters=[setup["diameter"]],
        hub_heights=[setup["hub_height"]],
        powerCtFunctions=[power_ct]
    )

    windTurbines = V80()


    # windTurbines = V80()
    # site = Hornsrev1Site()
    layout_x = setup["layout_x"]
    layout_y = setup["layout_y"]


    site = IEA37Site(16)
    x, y = [0, 400, 800], [0, 0, 0]
    windTurbines = V80()
    D = windTurbines.diameter()


    wfm = BastankhahGaussian(site, windTurbines, deflectionModel=JimenezWakeDeflection())

    #here we import the turbine, site and wake deficit model to use.
    yaws = [50 for _ in range(10)]  # example yaw angles for each turbine in degrees
    simulationResult = wfm(
    x=layout_x,
    y=layout_y,
    wd=[wd],   # constant wind direction [deg]
    yaw=yaws,
    tilt = 0
    )

    # wfm = BastankhahGaussian(site, windTurbines, deflectionModel=deflectionModel)
    

    plt.figure(figsize=(14,4))
    fm = simulationResult.flow_map()
    fm.plot_wake_map()




from py_wake.deflection_models import JimenezWakeDeflection
plot_deflection(JimenezWakeDeflection())
plt.xlabel('x [m]')
plt.ylabel('y [m]')

plt.show()