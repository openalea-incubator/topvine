from __future__ import absolute_import
from openalea.plantgl.all import *
from numpy import array, sin, cos, pi, ceil
import random
from openalea.core.pkgmanager import PackageManager
from six.moves import range
pm = PackageManager()
pkg = pm.get('alinea.topvine') 
path_topvine = ''
if pkg :
    path_topvine = pkg.path

import sys
sys.path.insert(0, path_topvine)

from Obj3Dutils import *
import IOtable



def luz_label(sp_opt, num_phyI, num_shoot, num_plant, num_phyII=0):
    num_phy = num_phyI*10**2 + num_phyII
    lab = str(int(sp_opt*10**11+num_phy*10**6+num_shoot*10**3+num_plant))
    return (12-len(lab))*'0'+lab


def sc_turtle36(ls_pt, MaScene, size=0.01):
    """ """    
    turt = turtle36()
    count1, count2 = 0, 0
    for i in range (len(ls_pt)):
        fI = transformation(turt, size, size, size, 0,0, 0, ls_pt[i][0], ls_pt[i][1], ls_pt[i][2]) 
        id1 = luz_label(1, count1, 0, count2, 0)#luz_label(1, i, 0, 1, 0)
        fI.setName(id1)
        MaScene.add(Shape(fI, Material(Color3(23,140,31))))
        if count1==999:
            count1=0
            count2=count2+1
        else:
            count1=count1+1


    return MaScene




def optim_sec(vabs, dseil = 0.03):
    """ """
    ls_azi = [0.26179938779914941, 0.78539816339744828, 1.308996938995747, 1.8325957145940459, 2.3561944901923448, 2.8797932657906435, 3.4033920413889427, 3.9269908169872414, 4.4505895925855397, 4.9741883681838388, 5.4977871437821371, 6.0213859193804362, 0.26179938779914941, 0.78539816339744828, 1.308996938995747, 1.8325957145940459, 2.3561944901923448, 2.8797932657906435, 3.4033920413889427, 3.9269908169872414, 4.4505895925855397, 4.9741883681838388, 5.4977871437821371, 6.0213859193804362, 0.26179938779914941, 0.78539816339744828, 1.308996938995747, 1.8325957145940459, 2.3561944901923448, 2.8797932657906435, 3.4033920413889427, 3.9269908169872414, 4.4505895925855397, 4.9741883681838388, 5.4977871437821371, 6.0213859193804362]
    ls_incli = [1.308996938995747]*12+[0.78539816339744828]*12+[0.26179938779914941]*12

    if len(vabs)==36:
        maxi = max(vabs)
        mini = max(0, maxi-dseil)
        ls_id = []
        # recupere les id proches du maxi
        for i in range(len(vabs)):
            if vabs[i]>=mini:
                ls_id.append(i)

        if len(ls_id)==1:
            angles = [ls_azi[ls_id[0]], ls_incli[ls_id[0]]]
        else:#+d'un secteur concerne - en tire un au hasard
            x = int(ceil(random.uniform(0, len(ls_id)))-1.)
            angles = [ls_azi[ls_id[x]], ls_incli[ls_id[x]]]

    else:#si turtle pas conforme (pas 36 secteurs recupere) -> tire au hasard
        x = int(ceil(random.uniform(0, 36))-1.)
        angles = [ls_azi[x], ls_incli[x]]        

    return angles

#vabs = [0.034452,0.005456,0.018872,0.017149,0.030699,0.166925,0.312396,0.345153,0.352012,0.388114,0.244779,0.016541,0.216051,0.106046,0.014783,0.007876,0.034788,0.124494,0.183052,0.290545,0.363042,0.422387,0.344953,0.215857,0.108616,0.091277,0.046771,0.057287,0.055264,0.085458,0.082562,0.223741,0.246051,0.174511,0.294539,0.240964]
#optim_sec(vabs)



def compute_optim_angle(dict, dseuil = 0.03):
    """ a partir du bilan radiatif des turtle remplacant les feuilles - prend le max par secteur (dans une gamme definie par un seuil
        renvoie angle correspondants - si turtle incomplet tire au hasard; si plusieurs dans la gamme du seuil, tire au hasard dans cette liste"""

    #def d'un id unique a partir de Plt et Elt
    for j in range(len(dict['Elt'])):
        dict['Opak'][j] = int(str(dict['Plt'][j]) + str(dict['Elt'][j]))

    #parcours le dict et segmente en feuilles
    v_angle_out, v_leaf = [], []
    i=0
    id = dict['Opak'][i]
    v_leaf.append(dict['Eabsm2'][i])
    nbl = len(dict['Elt'])
    while i<nbl-1:
        i = i+1
        new_id = dict['Opak'][i]
        
        if  new_id == id and i < nbl-1:#continue
            v_leaf.append(dict['Eabsm2'][i])
        elif i == nbl-1:#derniere ligne
            ang = optim_sec(v_leaf, dseuil)
            v_angle_out.append(ang)
        else:#changement de feuille
            ## finit feuille precedente
            id = new_id
            ang = optim_sec(v_leaf, dseuil)
            v_angle_out.append(ang)
            ## commence nouvelle
            v_leaf = []
            v_leaf.append(dict['Eabsm2'][i])

    return v_angle_out
    #me manque une feuille avec cet algo
