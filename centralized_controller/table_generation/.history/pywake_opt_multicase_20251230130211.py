from py_wake.site import UniformSite
from py_wake.wind_turbines import WindTurbine
from py_wake import NOJ
import matplotlib.pyplot as plt
import numpy as np
import os
from off2pywake_support import build_farm_setup, load_windfarm_yaml, rotate_points
from py_wake.deficit_models.gaussian import BastankhahGaussian
from py_wake.deflection_models import JimenezWakeDeflection
from py_wake.wind_turbines import WindTurbines
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.examples.data.hornsrev1 import V80
from py_wake.examples.data.iea37._iea37 import IEA37Site, IEA37_WindTurbines
from py_wake.turbulence_models import STF2017TurbulenceModel


def init_pywake():
    farm_dictionary = load_windfarm_yaml("windfarm_information_2x5.yaml")
    setup = build_farm_setup(farm_dictionary)

    ws_array = np.array([0, 4, 6, 8, 10, 12, 18, 25])
    power = np.array([0, 0, 6**3, 8**3, 10**3, 12**3, 18**3, 18**3])*setup["A"]*0.5*1.225 * 0.47/1e6  # in kW
    ct = np.array([0, 0.74, 0.74,0.74, 0.74, 0.74, 0.74, 0.74])

    power_ct = PowerCtTabular(ws = ws_array, power = power, ct = ct, power_unit='W')

    windTurbines = WindTurbines(
        names=['Turbine'],
        diameters=[setup["diameter"]],
        hub_heights=[setup["hub_height"]],
        powerCtFunctions=[power_ct]
    )

    layout_x = setup["layout_x"]
    layout_y = setup["layout_y"]

    return windTurbines, layout_x, layout_y, setup


def optimize_yaw_angles(ws, wd, ti = 0.01, n_points_per_range = 4, search_radius = 20, improvement_margin = 0.01/100):

    windTurbines, layout_x, layout_y, setup = init_pywake()
    site = UniformSite(ws=ws, ti=ti)

    # create the order of turbines based on what the wind hits first
    wind_aligned_distance = np.zeros_like(layout_y)
    for i in range(len(layout_x)):
        _, wind_aligned_distance[i] = rotate_points(layout_x[i], layout_y[i], -wd)
        wind_aligned_distance[i] = -1*wind_aligned_distance[i]

    opt_order = np.argsort(wind_aligned_distance)

    wfm = BastankhahGaussian(site, windTurbines, deflectionModel=JimenezWakeDeflection(), turbulenceModel=STF2017TurbulenceModel())

    yaw = [0 for _ in range(setup["n_turbines"])] 

    for tur_ind in opt_order:

        best_power = 0
        left_end_point = -search_radius
        right_end_point = search_radius
        relative_power_improvement = 1

        simulationResult = wfm(
                    x=layout_x,
                    y=layout_y,
                    wd=[wd],
                    yaw=yaw,
                    tilt = 0
                )
        
        best_power = simulationResult.Power.sum().values
        best_yaw_i = 0
        
        while relative_power_improvement > improvement_margin0:
            previous_best_power = best_power
            for yaw_i in np.linspace(left_end_point, right_end_point, n_points_per_range):
                yaw[tur_ind] = yaw_i

                simulationResult = wfm(
                    x=layout_x,
                    y=layout_y,
                    wd=[wd],
                    yaw=yaw,
                    tilt = 0
                )
                sumpower = simulationResult.Power.sum().values
                power_yaw_dict[yaw_i] = sumpower
                # print(f'Tested yaw: {yaw_i} degrees, Total Power: {sumpower} MW')

                tis = simulationResult.TI_eff.values.squeeze()

                if sumpower > best_power:
                    best_power = sumpower
                    best_yaw_i = yaw_i


            relative_power_improvement = (best_power - previous_best_power)/previous_best_power
            # print("-----------------------")
            # print(f'Relative power improvement: {relative_power_improvement*100:.2f}%')
            # print(f'Current best yaw for turbine {tur_ind}: {best_yaw_i} degrees with power {best_power} MW')
            #narrow down the search range
            new_range = (right_end_point - left_end_point)/4
            left_end_point = best_yaw_i - new_range
            right_end_point = best_yaw_i + new_range
                
        yaw[tur_ind] = best_yaw_i
        print(f'Best yaw for turbine {tur_ind} is {best_yaw_i} degrees with total power {best_power} MW')
        power_yaw_dicts.append(power_yaw_dict)

        # Plot power vs yaw angle
        plt.figure()
        plt.scatter(power_yaw_dict.keys(), power_yaw_dict.values())
        plt.xlabel('Yaw Angle [degrees]')
        plt.ylabel('Total Power [MW]')
        plt.title('Power vs Yaw Angle')
        plt.grid(True)
        plt.show()


    simulationResult = wfm(
    x=layout_x,
    y=layout_y,
    wd=[wd],
    yaw=yaw,
    tilt = 0
    )
    

    flow_map = simulationResult.flow_map(ws=ws, wd=wd)

    # get summa power
    total_power = simulationResult.Power.values.sum()
    print(f'Total Power Output: {total_power} MW')
    flow_map.plot_wake_map()
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Wake map for' + f' {ws} m/s and {wd} deg')

    # get the turbulence intensity at each turbine
    tis = simulationResult.TI_eff.values.squeeze()
    for i, ti in enumerate(tis):
        print(f'Turbine {i+1}: Effective Turbulence Intensity = {ti}')

    plt.show()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    optimize_yaw_angles(ws=8, wd=200)