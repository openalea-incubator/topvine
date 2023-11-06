from __future__ import absolute_import
import numpy
import random
from . import leaf
from . import shoot
from six.moves import range


class gen_normal_canopy(object):
    """  generates a list of normalised shoot objects associationg average topology with geometric features (primary shoot geom, leaf angles, leaf dimensions) """ 

    def __init__(self):
        pass


    def __call__(self, tab_geom, topol, dl_leaf):
        res = []

        for i in range(len(tab_geom)):
            ### topl = generate_rameau(NFI,NFII,LEN, SF, sd, sd)
            p = []
            for j in range(len(tab_geom[i])):
                p.append(shoot.Shoot(tab_geom[i][j], topol, dl_leaf))

            res.append(p)

        return res


class gen_normal_canopy_2023(object):
    """  generates a list of normalised shoot objects associationg average topology with geometric features (primary shoot geom, leaf angles, leaf dimensions) """

    def __init__(self):
        pass


    def __call__(self, tab_geom, topol, dl_leaf):
        res = []

        for i in range(len(tab_geom)):
            ### topl = generate_rameau(NFI,NFII,LEN, SF, sd, sd)
            p = []
            for j in range(len(tab_geom[i])):
                p.append(shoot.Shoot(tab_geom[i][j], topol, dl_leaf))

            res.append(p)

        return res