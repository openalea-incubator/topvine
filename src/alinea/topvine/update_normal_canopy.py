from __future__ import absolute_import
import numpy
import random
from . import leaf
from . import shoot
from six.moves import range


class update_normal_canopy(object):
    """  updates a list of normalised shoot objects with a new topology using update_topo method """ 

    def __init__(self):
        pass


    def __call__(self, tab_shoot, topol, dl_leaf):

        for i in range(len(tab_shoot)):
            for j in range(len(tab_shoot[i])):
                tab_shoot[i][j].update_topo(topol,dl_leaf)

        return tab_shoot
