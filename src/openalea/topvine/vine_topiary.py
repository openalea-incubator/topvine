from __future__ import absolute_import

from openalea.plantgl.all import Scene, Viewer
from six.moves import range

from openalea.topvine.primitive import trunk
from openalea.topvine.topiary import Topiary, Topiary_2023


class VineTopiary(object):
    """Generates a scaled PGL scene from a list of normalised shoot objects."""

    def __init__(self):
        self.scene = Scene()

    def generate_scene(
            self,
            tab_shoot,
            dl_leaf,
            allo,
            boolI,
            boolT, boolB
    ):
        for i in range(len(tab_shoot)):
            coord = tab_shoot[i][0].geom[1]
            for j in range(len(tab_shoot[i])):
                coord = (coord + tab_shoot[i][j].geom[1]) / 2
                Topiary(
                    scene=self.scene,
                    shoot=tab_shoot[i][j],
                    allo=allo,
                    lawf=dl_leaf,
                    visu_en=boolI
                )

            if boolT:
                trunk(self.scene, coord / 100., 'cordon')

            # a ameliorer: / type / calcul plus precis des rangs sur moy plus larges ou sur donnees filees en entree

        Viewer.display(self.scene)
        return self.scene


class VineTopiary2023(object):
    """  Generates a scaled PGL scene from a list of normalised shoot objects """

    def __init__(self):
        self.scene = Scene()

    def generate_scene(
            self,
            tab_shoot,
            dl_leaf,
            allo,
            boolI,
            boolT,
            display=True,
    ):
        for plant in range(len(tab_shoot)):
            for shoot in range(len(tab_shoot[plant])):
                Topiary_2023(
                    scene=self.scene,
                    shoot=tab_shoot[plant][shoot],
                    allo=allo,
                    lawf=dl_leaf,
                    visu_en=boolI,
                    num_vine=plant,
                    num_shoot=shoot,
                )
            coord = tab_shoot[plant][round(len(tab_shoot[plant]) / 2)].geom[1]

            # add a trunk if option is set to True
            if boolT is True:
                trunk(
                    MaScene=self.scene,
                    coord=coord / 100.,
                    type='cordon',
                )

            # a ameliorer: / type / calcul plus precis des rangs sur moy plus larges ou sur donnees filees en entree

        if display:
            Viewer.display(self.scene)

        return self.scene
