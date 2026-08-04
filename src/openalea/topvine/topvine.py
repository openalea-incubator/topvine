import numpy as np

import openalea.topvine.data_samples as ds
from openalea.topvine import conditional_multivariate_normal as cmn
from openalea.topvine.gen_normal_canopy import gen_normal_canopy_2023
from openalea.topvine.gen_shoot_param import gen_shoot_param
from openalea.topvine.generate_rameau_moyen import generate_rammoy_topvine
from openalea.topvine.genodata import *
from openalea.topvine.topologise import topologise
from openalea.topvine.translate_shoots import translate_shoots
from openalea.topvine.vine_topiary import VineTopiary2023
from openalea.topvine.write_geom_file import write_geom_file


def shoot_generator(_carto, _genotype):
    list_plant = []
    shoot_lengths = []
    topol = topologise()
    for plant in range(0, len(_carto)):
        thisplant = []
        thisplantshootlength = []
        for branch in range(0, _carto[plant][1]):
            ramtopv = generate_rammoy_topvine(_genotype)
            shoot: tuple[list, list] = toponthefly_2023(shoot_specs= ramtopv)
            thisplant.append(shoot)
            thisplantshootlength.append(sum(ramtopv["IN_I_length"]))
        list_plant.append(thisplant)
        shoot_lengths.append(thisplantshootlength)
    return [list_plant, shoot_lengths]



def permute_third_n_fourth(listx: np.ndarray) -> np.ndarray:
    return listx.copy().take([0, 1, 3, 2])


def permute_third_n_fourth_array(arrayx: np.ndarray) -> np.ndarray:  # meant for 4x4 arrays
    res = arrayx.copy()
    res[:2, 2:] = res[:2, -1:1:-1]
    res[2:, :2] = res[-1:1:-1, :2]
    res[[2, 3], [2, 3]] = res[[3, 2], [3, 2]]
    res[[2, 3], [3, 2]] = res[[3, 2], [2, 3]]
    return res

def apply_perm_to_shootstats(shootstats):
    newstats = []
    for i in range(0, len(shootstats)):
        means = permute_third_n_fourth(shootstats[i][0])
        vrcvr = permute_third_n_fourth_array(shootstats[i][1])
        newstats.append((means, vrcvr))
    return newstats


def compare_complex_iterables(l1, l2):  # this is just a function I created for verification purposes
    botharelists = isinstance(l1, list) and isinstance(l2, list)
    botharearrays = isinstance(l1, np.ndarray) and isinstance(l2, np.ndarray)
    botharetuples = isinstance(l1, tuple) and isinstance(l2, tuple)
    # print("botharelists "+str(botharelists) +"__botharearrays "+str(botharearrays) +"__botharetuples " + str(botharetuples) +"\n")
    if botharelists or botharearrays or botharetuples:
        if len(l1) == len(l2):
            for i in range(0, len(l1)):
                if not compare_complex_iterables(l1[i], l2[i]):
                    return False
            return True
        else:
            print(str(l1[i]) + "\n is not equal with \n" + str(l1[i]))
            return False
    else:

        boool = l1 == l2
        # print("not iter?? " + str(l1) + " !!  " + str(l2) +" they are " + str(boool))
        if not boool:
            print(str(l1) + "\n is NOOT equal with  \n" + str(l2))
        return boool


def update_shootstats(means, varcovar, avlength, length):
    (reordered_means, reordered_varcovar) = apply_perm_to_shootstats([(means, varcovar)])[0]
    normalized_length = length / avlength
    distribution = cmn.MultivariateNormal(reordered_means, reordered_varcovar)
    # print("reodreredmeans : "+ str(reordered_means))
    # print("reodreredvarcov : " + str(reordered_varcovar))
    distribution.partition(3)
    # compute the cond. dist. of the part before index 3
    ind = 0
    mu2_hat, Sigma2_hat = distribution.cond_dist(ind, normalized_length)
    newvarcovar = np.append(np.append(Sigma2_hat, np.array([[0], [0], [0]]), axis=1),
                            np.array([[0, 0, 0, 0]]), axis=0)
    newmeans = np.append(mu2_hat, np.array([normalized_length]), axis=0)
    (newmeans, newvarcovar) = apply_perm_to_shootstats([(newmeans, newvarcovar)])[0]
    return newmeans, newvarcovar


def stand_simulator(carto, spurs0, dspurs, f_azi, shootstats, avlength, shoot_lengths):
    __geom = []
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
    carto = ds.stand_file(stand_path)  # [posxyz_plant, nb_coursons]
    shoot_data = shoot_generator(carto,
                                 gen)  # [topology and leaf surface for each plant, length of every shoot for each plant]
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
