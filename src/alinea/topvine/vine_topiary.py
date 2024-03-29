from __future__ import absolute_import
import numpy
import random
from . import leaf
from . import shoot
from . import topiary
from .coor3D import *
from .primitive import *
from six.moves import range


class vine_topiary(object):
    """  Generates a scaled PGL scene from a list of normalised shoot objects """

    def __init__(self):
        pass

    def __call__(self, tab_shoot, dl_leaf, allo, boolI, boolT, boolB):
        MaScene = Scene()
        MonViewer = Viewer
        for i in range(len(tab_shoot)):
            coord = tab_shoot[i][0].geom[1]
            for j in range(len(tab_shoot[i])):
                coord = (coord + tab_shoot[i][j].geom[1]) / 2
                top = topiary.Topiary(MaScene, tab_shoot[i][j], allo, dl_leaf, visu_en=boolI)
            # add a trunk if option is set to True
            if boolT == True:
                trunk(MaScene, coord / 100., 'cordon')

            # a ameliorer: / type / calcul plus precis des rangs sur moy plus larges ou sur donnees filees en entree

        MonViewer.display(MaScene)
        return MaScene


class vine_topiary_2023(object):
    """  Generates a scaled PGL scene from a list of normalised shoot objects """

    def __init__(self):
        pass

    def __call__(self, tab_shoot, dl_leaf, allo, boolI, boolT, boolB, display=True):
        MaScene = Scene()
        MonViewer = Viewer
        for plant in range(len(tab_shoot)):
            # coord = tab_shoot[i][0].geom[1]
            for shoot in range(len(tab_shoot[plant])):
                # coord = (coord + tab_shoot[i][j].geom[1]) / 2
                top = topiary.Topiary_2023(MaScene, tab_shoot[plant][shoot], allo, dl_leaf, visu_en=boolI,
                                           num_vine=plant,
                                           num_shoot=shoot)
            coord = tab_shoot[plant][round(len(tab_shoot[plant]) / 2)].geom[1]
            # add a trunk if option is set to True
            if boolT is True:
                trunk(MaScene, coord / 100., 'cordon')

            # a ameliorer: / type / calcul plus precis des rangs sur moy plus larges ou sur donnees filees en entree
        if display:
            MonViewer.display(MaScene)
        return MaScene
