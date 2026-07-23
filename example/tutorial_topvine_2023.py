""" A python tutorial for running topvine grapevine canopy generator
"""

from openalea.topvine.topvine_2023 import topvine
from openalea.topvine.genodata import (
    Carignan, Chasselas, Clairette,Marselan, Mauzac, Mourverde, Petit_Verdot, Vermentino)
from openalea.topvine.multisim import vine_label, getfromid, TopVineInput, top_multisim
from openalea.plantgl.all import surface
import pandas as pd

from numpy import histogram_bin_edges

from matplotlib import pyplot as plt


def main_one_genotype():
    scene, tab_shoot = topvine(
        stand_path='/data/carto.csv',
        gen=Chasselas,
        dl_shoot_path='/data/2W_VSP_GRE_ramd.csv',
        dl_path='/data/Law-leaf-2W-Grenache.csv',
        allom_path='/data/allo_Grenache.csv',
        display=False
    )

    # at first, we will generate histograms of the first and second order leaf surfaces.
    primarysurfs = []
    secsurfs = []

    for shape in scene:
        if getfromid(aidee=shape.name, what='type') == '1':
            if getfromid(shape.name, 'phy') % 100 == 0:
                primarysurfs.append(surface(shape))
            else:
                secsurfs.append(surface(shape))

    # We superimpose the two histograms with the following commands:
    plt.hist(primarysurfs, bins=28)
    plt.hist(secsurfs, bins=28)

    # Now if we want to extract more detailed information from the simulation, we can use the second element of tpresult.
    # We initialize the lists which we then fill by looping through the "shoot table" which is tab_shoot.

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

    plnb = 0
    shnb = 0

    for plant in tab_shoot:
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

    # And now we integrate all those lists into a data frame where every line corresponds to a leaf.


    # And here some data analysis:
    leaf_data = pd.DataFrame({
        'leafid': leafid,
        "plantnb": plantnb,
        'shootid': shootid,
        'leaforder': leaforder,
        'leafarea': leafarea,
        'phytinternode': phytinternode,
        'leafcoordx': leafcoordx,
        'leafcoordy': leafcoordy,
        'leafcoordz': leafcoordz,
        'leafanglea': leafanglea,
        'leafangleb': leafangleb,
    }
    )

    fig, axs = plt.subplots(nrows=3, sharex='all')
    bins = histogram_bin_edges(leaf_data['leafarea'], bins=30)
    for order, group in leaf_data.groupby('leaforder'):
        axs[0].hist(group['leafarea'], bins=bins, alpha=0.5, label=f"leaf order {str(order)}")
        axs[0].legend()

    for plantnb, group in leaf_data[leaf_data['leaforder'] == 1].groupby('plantnb'):
        axs[1].hist(group['leafarea'], bins=bins, alpha=0.5, label=f"plant {str(plantnb)}")
        axs[1].legend()
        axs[2].scatter(group['leafarea'], group['phytinternode'], label=f"plant {str(plantnb)}")
        axs[2].legend()

    for plantnb, group in leaf_data[leaf_data['leaforder'] == 1].groupby('plantnb'):
        plt.scatter(group['leafarea'], group['phytinternode'], label=str(plantnb))


def main_multiple_genotypes():
    # We can also plan a number of different simulations and then execute all with one command. It suffices to use objects
    # of the class TopVineInput, where the details of the input of each simulation are given. We put them all in a list as
    # below. In this case we only vary the genotype, however it is possible to customize any parameter.

    inputlist = []
    for i in range(10):
        inputlist.append(TopVineInput(gen=Carignan))
    for i in range(10):
        inputlist.append(TopVineInput(gen=Chasselas))
    for i in range(10):
        inputlist.append(TopVineInput(gen=Clairette))
    for i in range(10):
        inputlist.append(TopVineInput(gen=Marselan))
    for i in range(10):
        inputlist.append(TopVineInput(gen=Mauzac))
    for i in range(10):
        inputlist.append(TopVineInput(gen=Mourverde))
    for i in range(10):
        inputlist.append(TopVineInput(gen=Petit_Verdot))
    for i in range(10):
        inputlist.append(TopVineInput(gen=Vermentino))

    # Now using the top_multisim function with a list of TopVineInput objects, we run the series of simulations.

    df = top_multisim(inputlist)

    # The result is a data frame where each line corresponds to a leaf, and the columns are leafid, plantnb, shootid,
    # leaforder, leafarea,  phytinternode, leafcoordx, leafcoordy, leafcoordz, leafanglea, leafangleb, simnumber, genotype.

    # And now we can explore the results, for example by plotting the leaf area vs the internode length of all the leafs of
    # a particular genotype and order.  Or we can plot the leaf angle a against the height of the leaf.

    fig, axs = plt.subplots(nrows=2)
    for shootid, group in df[(df['leaforder'] == 1) & (df['genotype'] == 'Chasselas')].groupby('shootid'):
        axs[0].scatter(group['leafarea'], group['phytinternode'], label=str(shootid))

    for shootid, group in df[df['leaforder'] == 1].groupby('genotype'):
        axs[1].scatter(group['leafanglea'], group['leafcoordz'], label=str(genotype), alpha=0.4)


if __name__ == '__main__':
    import matplotlib

    matplotlib.use('Qt5Agg')

    from IPython import get_ipython

    ip = get_ipython()
    if ip is not None:
        ip.enable_gui("qt")
        INTERACTIVE = True
    else:
        INTERACTIVE = False

    main_one_genotype()
    main_multiple_genotypes()

    if not INTERACTIVE:
        from PyQt5.QtWidgets import QApplication

        QApplication.instance().exec_()
    pass
