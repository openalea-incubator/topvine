import numpy as np

import openalea.topvine.data_samples as ds
from openalea.topvine import conditional_multivariate_normal as cmn
from openalea.topvine.gen_normal_canopy import gen_normal_canopy_2023
from openalea.topvine.gen_shoot_param import gen_shoot_param
from openalea.topvine.topologise import topologise
from openalea.topvine.translate_shoots import translate_shoots
from openalea.topvine.generate_rameau_moyen import generate_rameau_moyen, Genotype
from openalea.topvine.vine_topiary import VineTopiary2023
from openalea.topvine.write_geom_file import write_geom_file

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

def stand_simulator(carto, spurs0, dspurs, f_azi, shootstats, avlength, shoot_lengths):
    __geom = []
    newmeans = np.append(
        conditional_mean,
        np.array([normalized_length]),
        axis=0
    )

    return (
        permute_third_n_fourth(listx=newmeans),
        permute_third_n_fourth_array(arrayx=newvarcovar),
    )


    generator = gen_shoot_param()
    translator = translate_shoots()
    carto_index = 0
    for plant in shoot_lengths:
        # print("debugging" + str(plant))
        plantgeom = []
        spurs = generator.gen_spurs(carto[carto_index][1], spurs0, dspurs)
        shoot_index = 0
        for shootlength in plant:
            # print("debugging" + str(shootlength))
            for i in range(0, len(shootstats)):
                newstats = list(shootstats)
                newstats[i] = update_shootstats(shootstats[i][0], shootstats[i][1], avlength, shootlength)
            shoot_params = spurs[shoot_index] + generator.gen_shoot(f_azi, newstats)
            plantgeom.append(shoot_params)
            shoot_index = shoot_index + 1
        __geom.append(translator(plantgeom, carto[carto_index][0]))
        carto_index = carto_index + 1
    return __geom


def shoot_realizator(
        _geom,
        _shoot_data,
        _leafstats,
) -> list[list[gen_normal_canopy_2023]]:
    generator = gen_normal_canopy_2023()
    table_shoot = []
    for plant in range(0, len(_geom)):
        thisplant = []
        for branch in range(0, len(_geom[plant])):
            thisplant.append(generator([[_geom[plant][branch]]], _shoot_data[plant][branch], _leafstats)[0][0])
        table_shoot.append(thisplant)
    return table_shoot


def topvine(
        stand_path: str = '/data/carto.csv',
        gen: Genotype = Genotype(),
        dl_shoot_path: str = '/data/2W_VSP_GRE_without_ramd.csv',
        dl_path: str = '/data/Law-leaf-2W-Grenache.csv',
        allom_path: str = '/data/allo_Grenache.csv',
        branches: bool = True,
        trunk: bool = True,
        name: str = 'geom2023.csv',
        geomfile: str | None = None,
        display: bool = True
):
    """

    Args:
        stand_path: relative path to the file that includes the plot data (For every plant, XYZ coordinates + number of shoots (coursons))
        gen: grapevine genotype having the average shoot profile (topology, leaf surface and internode length).
        dl_shoot_path: relative path to the file that includes the parameters of distribution laws for shoot.
            - X0,Y0,Z0    : distribution laws for the positioning of the spurs.
            - DX,DY,DZ    : distribution laws for the distancing of the buds in the spurs.
            - Dist        : seems not to be used
            - freq AZI    : frequency of shoot AZI of angle (-20, 20), (20, 160), (160, 200) and (200, 340)
            - x (     )   : means of the 4 other shoot parameters, namely initial elevation, angle between basal and distal tangents (a.k.a curvature), proportion of shoot accounting for half the curvature and normalized length.
            - S (    )    : Covariance matrices for the 4 other shoot parameters for each azimuth range.
            - Note that the normalized length is included in this table because of the original architecture of the program, however it is subsequently superseded according to the simulations of the generate_rameau_moyen.py script, according to the genotype selected.
        dl_path: relative path to the file that includes the parameters of distribution laws for leaves.
            - Elevation South – Elevation North – Azimuth South – Azimuth North
        allom_path: relative path to the file that includes the allometry parameters
            - The first line includes the allometric parameters a & b that link the length of a shoot with its number of phytomers (L = a * n + b).
        branches: whether to show internodes (default: True)
        trunk: whether to show trunk (default: True)
        name: name of the geometry file (for writing)
        geomfile: relative path to geometry file (for reading, default: None)
        display: whether to display the resulting scene (default: True)

    Returns:
        A tuple containing:
            - PGL scence object
            - Shoot objects per plant
    """
    carto: list[tuple[np.ndarray, int]] = ds.stand_file(stand_path)  # [posxyz_plant, nb_coursons]
    shoot_data: tuple[list, list] = shoot_generator(
        carto=carto,
        genotype=gen,
    )
    if geomfile is not None:
        geom = ds.geom_file(fn=geomfile)
    else:

        spurs0, dspurs, f_azi, shootstats = ds.dl_shoot_file(fn=dl_shoot_path)

        geom = stand_simulator(carto, spurs0, dspurs, f_azi, shootstats, gen.mean_shoot_length, shoot_data[1])
        write_geom = write_geom_file()
        write_geom(geom, name)

    dl = ds.dl_file(dl_path)
    tab_shoot = shoot_realizator(
        _geom=geom,
        _shoot_data=shoot_data[0],
        _leafstats=dl,
    )

    allometry = ds.allometry_file(allom_path)

    scene = VineTopiary2023().generate_scene(
        tab_shoot=tab_shoot,
        dl_leaf=dl,
        allo=allometry,
        boolI=branches,
        boolT=trunk,
        display=display,
    )

    return scene, tab_shoot
