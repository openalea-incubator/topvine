from pathlib import Path

from hydroshoot.irradiance import irradiance_distribution, hsCaribu, set_optical_properties
from hydroshoot.params import Params
from hydroshoot.io import HydroShootHourlyInputs as inputs_hourly, HydroShootInputs, verify_inputs


from alinea.topvine.topvine_2022 import topvine
# %gui qt5

scene = topvine(shoot_path='/data/ex_rammoy3_test.csv')[0]

__file__="C:\GitModeles\grapevine//topvine\src//alinea//topvine\Radiation2023.py"

path_project = Path(__file__).parent
wd = path_project
path_weather = path_project / 'meteo.input'

inputs = HydroShootInputs(
        path_project=wd,
        path_weather=path_weather,
        user_params=None,
        scene=scene,
        write_result=False,
        path_output_file=None,
        psi_soil=-0.2,
        gdd_since_budbreak=100.
        )

params = inputs.params

inputs_hourly = inputs_hourly(psi_soil=inputs.psi_soil, sun2scene=inputs.sun2scene)

caribu_source, diffuse_to_total_irradiance_ratio = irradiance_distribution(
    meteo=inputs_hourly.weather,
    geo_location=params.simulation.geo_location,
    irradiance_unit=params.irradiance.E_type,
    time_zone=params.simulation.tzone,
    turtle_sectors=params.irradiance.turtle_sectors,
    turtle_format=params.irradiance.turtle_format,
    sun2scene=inputs_hourly.sun2scene,
    rotation_angle=params.planting.scene_rotation)