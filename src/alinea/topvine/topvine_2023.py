import numpy as np

import alinea.topvine.data_samples as ds
from alinea.topvine.gen_normal_canopy import gen_normal_canopy_2023
from alinea.topvine.gen_shoot_param import gen_shoot_param
from alinea.topvine.translate_shoots import translate_shoots
from alinea.topvine.vine_topiary import vine_topiary_2023
from alinea.topvine.generate_rameau_moyen import generate_rammoy_topvine, Genotype
from alinea.topvine.topologise import topologise
from alinea.topvine import conditional_multivariate_normal as cmn
from alinea.topvine.write_geom_file import write_geom_file
from alinea.topvine.genodata import *


def shoot_generator(_carto, _genotype):
    list_plant = []
    shoot_lengths = []
    topol = topologise()
    for plant in range(0, len(_carto)):
        thisplant = []
        thisplantshootlength = []
        for branch in range(0, _carto[plant][1]):
            ramtopv = generate_rammoy_topvine(_genotype)
            shoot = topol.toponthefly_2023(ramtopv.values.tolist())
            thisplant.append(shoot)
            thisplantshootlength.append(sum(ramtopv["IN_I_length"]))
        list_plant.append(thisplant)
        shoot_lengths.append(thisplantshootlength)
    return [list_plant, shoot_lengths]


def permute_third_n_fourth(listx):
    listp = []
    for i in range(0, len(listx)):
        if abs(i - 2) + abs(i - 3) > 1:
            listp.append(listx[i])
        elif i == 2:
            listp.append(listx[i + 1])
        else:
            listp.append(listx[i - 1])
    if type(listx) is np.ndarray:
        listp = np.array(listp)
    return listp


def permute_third_n_fourth_array(arrayx):  # meant for 4x4 arrays
    arrayp = []
    for i in range(0, 4):
        linee = []
        for j in range(0, 4):
            if abs(i - 2) + abs(i - 3) > 1 and abs(j - 2) + abs(j - 3) > 1:
                linee.append(arrayx[i, j])
            elif i == 2 and abs(j - 2) + abs(j - 3) > 1:
                linee.append(arrayx[i + 1, j])
            elif i == 3 and abs(j - 2) + abs(j - 3) > 1:
                linee.append(arrayx[i - 1, j])
            elif abs(i - 2) + abs(i - 3) > 1 and j == 2:
                linee.append(arrayx[i, j + 1])
            elif abs(i - 2) + abs(i - 3) > 1 and j == 3:
                linee.append(arrayx[i, j - 1])
            else:
                linee.append(arrayx[i + (3 - i) + (2 - i), j + (3 - j) + (2 - j)])
        arrayp.append(linee)
    return np.array(arrayp)


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


def shoot_realizator(_geom, _shoot_data, _leafstats):
    generator = gen_normal_canopy_2023()
    table_shoot = []
    for plant in range(0, len(_geom)):
        thisplant = []
        for branch in range(0, len(_geom[plant])):
            thisplant.append(generator([[_geom[plant][branch]]], _shoot_data[plant][branch], _leafstats)[0][0])
        table_shoot.append(thisplant)
    return table_shoot


def topvine(stand_path='/data/carto.csv', gen=Genotype(),
            dl_shoot_path='/data/2W_VSP_GRE_ramd.csv', dl_path='/data/Law-leaf-2W-Grenache.csv',
            allom_path='/data/allo_Grenache.csv', branches=True, trunk=True, name='geom2023.csv', geomfile=0):
    carto = ds.stand_file(stand_path)  # [posxyz_plant, nb_coursons]
    shoot_data = shoot_generator(carto,
                                 gen)  # [topology and leaf surface for each plant, length of every shoot for each plant]
    if geomfile != 0:
        geom = ds.geom_file(geomfile)
    else:

        spurs0, dspurs, f_azi, shootstats = ds.dl_shoot_file(dl_shoot_path)

        geom = stand_simulator(carto, spurs0, dspurs, f_azi, shootstats, gen.mean_shoot_length, shoot_data[1])
        write_geom = write_geom_file()
        write_geom(geom, name)

    dl = ds.dl_file(dl_path)
    tab_shoot = shoot_realizator(geom, shoot_data[0], dl)

    vt = vine_topiary_2023()
    allometry = ds.allometry_file(allom_path)

    scene = vt(tab_shoot, dl, allometry, branches, trunk, False)

    return [scene, geom]

# %gui qt5

# from openalea.mtg.mtg import *

# g = MTG()
