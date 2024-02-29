from alinea.topvine.topvine_2023 import topvine
import pandas as pd
from alinea.topvine.genodata import *


def vine_label(sp_opt, num_phy, num_ram, num_vine):
    lab = str(str(sp_opt) + "type" + str(num_phy) + "phy" + str(num_ram) + "ram" + str(num_vine) + "plant")
    return lab


def getfromid(aidee, what):
    if what == 'type':
        return aidee.partition(what)[0]
    elif what == 'phy':
        return int(aidee.partition('type')[2].partition(what)[0])
    elif what == 'ram':
        return int(aidee.partition('type')[2].partition('phy')[2].partition(what)[0])
    elif what == 'plant':
        return int(aidee.partition('type')[2].partition('phy')[2].partition('ram')[2].partition(what)[0])
    else:
        print('wrong keyword')


class TopVineInput(object):

    def __init__(self, stand_path='/data/carto.csv', gen=Genotype(),
                 dl_shoot_path='/data/2W_VSP_GRE_without_ramd.csv', dl_path='/data/Law-leaf-2W-Grenache.csv',
                 allom_path='/data/allo_Grenache.csv', branches=True, trunk=True, name='geom2023.csv', geomfile=0,
                 display=False):
        self.stand_path = stand_path
        self.gen = gen
        self.dl_shoot_path = dl_shoot_path
        self.dl_path = dl_path
        self.allom_path = allom_path
        self.branches = branches
        self.trunk = trunk
        self.name = name
        self.geomfile = geomfile
        self.display = display


def top_multisim(inputs):
    simnumber = 0
    leaf_data = pd.DataFrame(
        {'leafid': [], "plantnb": [], 'shootid': [], 'leaforder': [], 'leafarea': [], 'phytinternode': [],
         'leafcoordx': [], 'leafcoordy': [], 'leafcoordz': [], 'leafanglea': [], 'leafangleb': [], 'simnumber': [],
         'genotype': []})
    plnb = 0
    shnb = 0

    for input in inputs:
        simnumber += 1
        if simnumber % 25 == 0:
            print(simnumber)

        tpresult = topvine(**input.__dict__)

        leafid = []
        plantnb = []
        shootid = []
        leaforder = []
        leafarea = []
        phytinternode = []
        leafcoordx = []
        leafcoordy = []
        leafcoordz = []
        leafanglea = []
        leafangleb = []

        for plant in tpresult[1]:
            for shoot in plant:
                for phyto in shoot.topo:
                    for leaf in phyto:
                        leafid.append(vine_label(1, leaf.id, shnb, plnb))
                        plantnb.append(str(plnb))
                        shootid.append(str(str(plnb) + "." + str(shnb)))
                        if int(leaf.id) % 100 == 0:
                            leaforder.append(1)
                            phytinternode.append(leaf.lin)
                        else:
                            leaforder.append(2)
                            phytinternode.append('NA')
                        leafarea.append(leaf.len)
                        leafcoordx.append(leaf.coord[0])
                        leafcoordy.append(leaf.coord[1])
                        leafcoordz.append(leaf.coord[2])
                        leafanglea.append(leaf.angle[0])
                        leafangleb.append(leaf.angle[1])
                shnb += 1
            plnb += 1
        thisdata = pd.DataFrame(
            {'leafid': leafid, "plantnb": plantnb, 'shootid': shootid, 'leaforder': leaforder, 'leafarea':
                leafarea, 'phytinternode': phytinternode, 'leafcoordx': leafcoordx, 'leafcoordy': leafcoordy,
             'leafcoordz': leafcoordz, 'leafanglea': leafanglea, 'leafangleb': leafangleb, 'simnumber': simnumber,
             'genotype': input.gen.name})
        leaf_data = pd.concat((leaf_data, thisdata))

    return leaf_data
