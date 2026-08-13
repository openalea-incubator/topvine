from pathlib import Path
import numpy as np
import pandas as pd

import openalea.topvine.data_samples as ds
from openalea.topvine import conditional_multivariate_normal as cmn
from openalea.topvine.gen_normal_canopy import create_normalized_canopy
from openalea.topvine.gen_shoot_param import gen_shoot_param
from openalea.topvine.generate_rameau_moyen import generate_rameau_moyen, Genotype
from openalea.topvine.topologise import toponthefly_2023
from openalea.topvine.vine_topiary import VineTopiary2023
from openalea.topvine.shoot import Shoot_2023
# from openalea.topvine.write_geom_file import write_geom_file


def shoot_generator(
        carto: list[tuple[np.ndarray, int]],
        genotype: Genotype,
) -> tuple[list[tuple[list, list]], list[list[float]]]:
    """Calculates, per plant per shoot per internode: individual leaf area and internode length.

    Args:
        carto:
        genotype: Genotype object

    Returns:

    """
    plants = []
    shoot_lengths = []

    for plant_xyz, nb_spurs in carto:
        thisplant = []
        thisplantshootlength = []
        for _ in range(nb_spurs):
            ramtopv: pd.DataFrame = generate_rameau_moyen(g=genotype)
            shoot: tuple[list, list] = toponthefly_2023(shoot_specs= ramtopv)
            thisplant.append(shoot)
            thisplantshootlength.append(sum(ramtopv["IN_I_length"]))
        plants.append(thisplant)
        shoot_lengths.append(thisplantshootlength)

    return plants, shoot_lengths


def permute_third_n_fourth(listx: np.ndarray) -> np.ndarray:
    return listx.copy().take([0, 1, 3, 2])


def permute_third_n_fourth_array(arrayx: np.ndarray) -> np.ndarray:  # meant for 4x4 arrays
    res = arrayx.copy()
    res[:2, 2:] = res[:2, -1:1:-1]
    res[2:, :2] = res[-1:1:-1, :2]
    res[[2, 3], [2, 3]] = res[[3, 2], [3, 2]]
    res[[2, 3], [3, 2]] = res[[3, 2], [2, 3]]
    return res


def update_shootstats(
        means: np.ndarray,
        varcovar: np.ndarray,
        genotype_mean_shoot_length: float,
        shoot_length: float,
):
    reordered_means = permute_third_n_fourth(listx=means)
    reordered_varcovar = permute_third_n_fourth_array(arrayx=varcovar)

    normalized_length: float = shoot_length / genotype_mean_shoot_length

    distribution = cmn.MultivariateNormal(μ=reordered_means, Σ=reordered_varcovar)

    # compute the cond. dist. of the part before index 3
    distribution.partition(3)

    conditional_mean, conditional_covariance_matrix = distribution.cond_dist(
        ind=0,
        z=normalized_length,
    )

    newvarcovar = np.append(
        np.append(
            conditional_covariance_matrix,
            np.zeros(shape=(conditional_covariance_matrix.shape[0], 1)),
            axis=1,
        ),
        np.zeros(shape=(1, conditional_covariance_matrix.shape[1] + 1)),
        axis=0,
    )

    newmeans = np.append(
        conditional_mean,
        np.array([normalized_length]),
        axis=0
    )

    return (
        permute_third_n_fourth(listx=newmeans),
        permute_third_n_fourth_array(arrayx=newvarcovar),
    )


def translate_coordinates(
        basal_coordinates: np.ndarray,
        shift: np.ndarray,
) -> np.ndarray:
    return basal_coordinates + shift


def set_stand_geometry(
        carto: list[tuple[np.ndarray, int]],
        spur_coordinates: list[list[tuple[float]]],
        spur_bud_distance: list[tuple[float]],
        shoot_fraction_per_azimut_sectors: list[float],
        shoot_stats: list[tuple[np.ndarray, np.ndarray]],
        genotype_mean_shoot_length: float,
        shoot_lengths_per_plant: list[list[float]],
) -> list[list[tuple[int, np.ndarray, float, float, float, float, float]]]:
    """Sets the geometry params of each plant in the simulated stand (placette).

    Args:
        carto:
        spur_coordinates: mean and standard deviation of x, y, z coordinates of spurs
        spur_bud_distance: mean and standard deviation of shifts on x, y, z coordinates between spurs
        shoot_fraction_per_azimut_sectors: (dimensionless) fraction of shoots in the four azimuth sectors
        shoot_stats: vectors of the mean and covariance values of each of the four parameters describing a shoot coordinates, i.e.:
            - initial inclination angle: (degrees) Basal shoot elevation angle (between -90 and 90)
            - curvature: (degrees): the difference between basal and distal shoot tangent angle (between -180 and 180)
            - maximum curvature point fraction: (dimensionless): ratio between the length from the origin of the shoot to the point of maximal curvature and the total length of the shoot (between 0 and 1)
            - Normalized length: (dimensionless) ratio between the actual shoot length and the mean shoot length for the "Cultivar" x "Training system" pair considered
        genotype_mean_shoot_length: (cm) mean shoot length of the simulated genotype
        shoot_lengths_per_plant: (cm) length of each shoot per plant in the stand

    Returns:
        For each plant, for each shoot, the following information:
            - (int) shoot order in the plant (dimensionless)
            - (np.ndarray) bud coordinates, i.e. base of the shoot (m)
            - (float) Mean shoot azimuth angle (degrees, between 0 and 360)
            - (float) Basal shoot elevation angle (initial inclination angle, degrees, between -90 and 90)
            - (float) Curvature (degrees), defined as the difference between basal and distal shoot tangent angle (between -180 and 180)
            - (float) Maximum curvature point fraction (dimensionless), defined as the ratio between the length from the origin of the shoot to the point of maximal curvature and the total length of the shoot (between 0 and 1)
            - (float) Normalized length (dimensionless), defined as the ratio between the actual shoot length and the mean shoot length for the "Cultivar" x "Training system" pair considered

    """
    stand_geometry = []
    generator = gen_shoot_param()

    for (plant_basal_xyz, spurs_number), plant_shoot_lengths in zip(carto, shoot_lengths_per_plant):
        plant_geometry = []
        spurs_params: list[tuple[int, np.ndarray]] = generator.generate_spur_coordinates(
            nb_spurs=spurs_number,
            spurs0=spur_coordinates,
            dspurs=spur_bud_distance,
        )

        # For each plant, the number of spurs is equal to the number of shoots,
        # both are generated based on the number of spurs in the carto table.
        for (spur_order, spur_coords), shoot_length in zip(spurs_params, plant_shoot_lengths):
            newstats : list[tuple[np.ndarray, np.ndarray]] = []
            for i in range(len(shoot_stats)):
                newstats.append(
                    update_shootstats(
                        means=shoot_stats[i][0],
                        varcovar=shoot_stats[i][1],
                        genotype_mean_shoot_length=genotype_mean_shoot_length,
                        shoot_length=shoot_length,
                    )
                )

            shoot_params: list[float] = generator.generate_shoot_spatial_params(
                f_azi=shoot_fraction_per_azimut_sectors,
                shoot_param=newstats,
            )

            plant_geometry.append(
                tuple(
                    [
                        spur_order,
                        translate_coordinates(basal_coordinates=spur_coords, shift=plant_basal_xyz),
                        *shoot_params
                    ]
                )
            )

        stand_geometry.append(plant_geometry)

    return stand_geometry


def generate_shoots(
        stand_geometry: list[list[tuple[int, np.ndarray, float, float, float, float, float]]],
        stand_topology: list[list[tuple[list[list[float]], list[list[float]]]]],
        leaf_stats: tuple[tuple[str, int, float, float]],
) -> list[list[Shoot_2023]]:
    """Generates all shoots of the stand

    Args:
        stand_geometry: for each plant in the stand, for each branch, the values of parameters that define the geometry of the shoot:
            - (int) shoot order in the plant (dimensionless)
            - (ndarray) bud coordinates, i.e. base of the shoot (m)
            - (float) Mean shoot azimuth angle (degrees, between 0 and 360)
            - (float) Basal shoot elevation angle (initial inclination angle, degrees, between -90 and 90)
            - (float) Curvature (degrees), defined as the difference between basal and distal shoot tangent angle (between -180 and 180)
            - (float) Maximum curvature point fraction (dimensionless), defined as the ratio between the length from the origin of the shoot to the point of maximal curvature and the total length of the shoot (between 0 and 1)
            - (float) Normalized length (dimensionless), defined as the ratio between the actual shoot length and the mean shoot length for the "Cultivar" x "Training system" pair considered
        stand_topology: for each plant in the stand, for each branch, values of parameters that define the topology of the shoot:
            - list[list[float] leaf area (cm2) of primary (first item) and secondary (remaining items) at each primary internode of the shoot
            - list[list[float] length (cm) of primary internodes (each internode length is set in a list)
        leaf_stats: distribution laws for leaf orientation


    Returns:
        shoot objects of the stand

    """
    res: list[list[Shoot_2023]] = []
    for i_plant in range(len(stand_geometry)):
        plant = []
        for i_shoot in range(len(stand_geometry[i_plant])):
            plant.append(
                create_normalized_canopy(
                    shoot_params=[[stand_geometry[i_plant][i_shoot]]],
                    topol=stand_topology[i_plant][i_shoot],
                    dl_leaf=leaf_stats,
                )
            )

        res.append(plant)
    return res


def topvine(
        stand_path: str | Path = '/data/carto.csv',
        gen: Genotype = Genotype(),
        dl_shoot_path: str | Path  = '/data/2W_VSP_GRE_without_ramd.csv',
        dl_path: str | Path  = '/data/Law-leaf-2W-Grenache.csv',
        allom_path: str | Path  = '/data/allo_Grenache.csv',
        branches: bool = True,
        trunk: bool = True,
        geomfile: str | None = None,
        display: bool = True
):
    """

    Args:
        stand_path: path to the file that includes the plot data (For every plant, XYZ coordinates + number of shoots (coursons))
            - if str: relative path from topvine/ dir
            - if Path: absolute path
        gen: grapevine genotype having the average shoot profile (topology, leaf surface and internode length).
        dl_shoot_path: relative path to the file that includes the parameters of distribution laws for shoot.
            - if str: relative path from topvine/ dir
            - if Path: absolute path
            * distribution laws for shoot:
            - X0,Y0,Z0    : distribution laws for the positioning of the spurs.
            - DX,DY,DZ    : distribution laws for the distancing of the buds in the spurs.
            - Dist        : seems not to be used
            - freq AZI    : frequency of shoot AZI of angle (-20, 20), (20, 160), (160, 200) and (200, 340)
            - x (     )   : means of the 4 other shoot parameters, namely initial elevation, angle between basal and distal tangents (a.k.a curvature), proportion of shoot accounting for half the curvature and normalized length.
            - S (    )    : Covariance matrices for the 4 other shoot parameters for each azimuth range.
            - Note that the normalized length is included in this table because of the original architecture of the program, however it is subsequently superseded according to the simulations of the generate_rameau_moyen.py script, according to the genotype selected.
        dl_path: path to the file that includes the parameters of distribution laws for leaves.
            - if str: relative path from topvine/ dir
            - if Path: absolute path
            * distribution laws for leaves:
            - Elevation South
            – Elevation North
            – Azimuth South
            – Azimuth North
        allom_path: path to the file that includes the allometry parameters
            - if str: relative path from topvine/ dir
            - if Path: absolute path
            * allometry parameters
            - The first line includes the allometric parameters a & b that link the length of a shoot with its number of phytomers (L = a * n + b).
        branches: whether to show internodes (default: True)
        trunk: whether to show trunk (default: True)
        geomfile: relative path to geometry file (for reading, default: None)
        display: whether to display the resulting scene (default: True)

    Returns:
        A tuple containing:
            - PGL scence object
            - Shoot objects per plant
    """
    carto: list[tuple[np.ndarray, int]] = ds.stand_file(stand_path)
    shoot_data: tuple[list, list] = shoot_generator(
        carto=carto,
        genotype=gen,
    )
    if geomfile is not None:
        geom: list[list[tuple[int, np.ndarray, float, float, float, float, float]]] = ds.geom_file(fn=geomfile)
    else:

        spurs0, dspurs, f_azi, shootstats = ds.dl_shoot_file(fn=dl_shoot_path)

        geom: list[list[tuple[int, np.ndarray, float, float, float, float, float]]] = set_stand_geometry(
            carto=carto,
            spur_coordinates=spurs0,
            spur_bud_distance=dspurs,
            shoot_fraction_per_azimut_sectors=f_azi,
            shoot_stats=shootstats,
            genotype_mean_shoot_length=sum(gen.primary_internode_profile),
            shoot_lengths_per_plant=shoot_data[1],
        )
        # write_geom = write_geom_file()
        # write_geom(geom, name)

    dl: tuple[tuple[str, int, float, float]] = ds.dl_file(dl_path)
    shoots: list[list[Shoot_2023]] = generate_shoots(
        stand_geometry=geom,
        stand_topology=shoot_data[0],
        leaf_stats=dl,
    )

    allometry = ds.allometry_file(allom_path)

    scene = VineTopiary2023().generate_scene(
        tab_shoot=shoots,
        dl_leaf=dl,
        allo=allometry,
        boolI=branches,
        boolT=trunk,
        display=display,
    )

    return scene, shoots
