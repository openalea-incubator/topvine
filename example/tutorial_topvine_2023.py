""" A python tutorial for runing topvine grapevine canopy generator
"""

# Should be run in a qt-enabled console (ipython --gui=qt)
# otherwise use ipython %gui magic command:
# %gui qt5    (use this command AFTER the imports)

from alinea.topvine.topvine_2023 import topvine
from alinea.topvine.genodata import *
from alinea.topvine.multisim import vine_label, getfromid, TopVineInput, top_multisim
from openalea.plantgl.all import surface
import pandas as pd
import seaborn as sns

# We start with the input.

# Plot file  (stand file)    --->   carto [posxyz_plant, nb_coursons]
# For every plant, XYZ coordinates + number of shoots
stand_path = '/data/carto.csv'

# Genotype, which will generate the average shoot profile (affects topology, leaf surface and internode length).
# Taken from a number of statistics from firld experiments (as found in genodata.py)
gen = Chasselas

# Distribution laws for shoot parameters (dl shoot file) ---> 2W_VSP_GRE_ramd
# X0,Y0,Z0    : distribution laws for the positioning of the spurs.
# DX,DY,DZ    : distribution laws for the distancing of the buds in the spurs.
# Dist        : seems not to be used
# freq AZI    : frequency of shoot AZI of angle (-20, 20), (20, 160), (160, 200) and (200, 340)
# x (     )   : means of the 4 other shoot parameters, namely initial elevation, angle between basal and distal tangents (a.k.a curvature), proportion of shoot accounting for half the curvature and normalized length.
# S (    )    : Covariance matrices for the 4 other shoot parameters for each azimuth range.
# Note that the normalized length is included in this table because of the original architecture of the program, however it is subsequently superseded according to the simulations of the generate_rameau_moyen.py script, according to the genotype selected.
dl_shoot_path = '/data/2W_VSP_GRE_ramd.csv'

# Distribution laws for leaf parameters (dl file)  --->  Law-leaf-2W-Grenache
# Elevation South – Elevation North – Azimuth South – Azimuth North
dl_path = '/data/Law-leaf-2W-Grenache.csv'

# Allometry file ---> allo_Grenache
# The first line includes the allometric parameters a & b that link the length of a shoot with its number of phytomers (L = a ⋅n+b).
allom_path = '/data/allo_Grenache.csv'

##############################################################################################

##################################  ONE SIMULATION ###########################################

# Here is the result of a simulation following the above input :

topvine(stand_path, gen, dl_shoot_path, dl_path, allom_path)

# But if we want to extract info from the simulation we can work like this:

tpresult = topvine(stand_path, gen, dl_shoot_path, dl_path, allom_path, display=False)

# at first, we will generate histograms of the first and secord order leaf surfaces.
# the result includes two elements, the first one being a plantgl scene from which we can recover all shapes:

shapes = [i for i in tpresult[0]]

# we create two lists and add to them the surface areas of primary and secondary order leaves respectively.
primarysurfs = []
secsurfs = []

for shape in shapes:
    if getfromid(shape.name, 'type') == '1':
        if getfromid(shape.name, 'phy') % 100 == 0:
            primarysurfs.append(surface(shape))
        else:
            secsurfs.append(surface(shape))

sdat = pd.DataFrame({'primarysurfs': primarysurfs})
sdat2 = pd.DataFrame({'secsurfs': secsurfs})

# We superimpose the two histograms with the following commands:

sns.histplot(sdat, x="primarysurfs")
sns.histplot(sdat2, x="secsurfs")

# Now if we want to extract more detailed information from the simulation, we can use the second element of tpresult.
# We initialize the lists which we then fill by looping through the "shoot table" which is tpresult[1].

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

# And now we integrate all those lists into a data frame where every line corresponds to a leaf.

leaf_data = pd.DataFrame({'leafid': leafid, "plantnb": plantnb, 'shootid': shootid, 'leaforder': leaforder,
                          'leafarea': leafarea, 'phytinternode': phytinternode, 'leafcoordx': leafcoordx,
                          'leafcoordy': leafcoordy,
                          'leafcoordz': leafcoordz,
                          'leafanglea': leafanglea, 'leafangleb': leafangleb})

# And here some data analysis:

sns.histplot(leaf_data, x='leafarea', hue='leaforder')
sns.histplot(leaf_data[leaf_data['leaforder'] == 1], x='leafarea', hue='plantnb')
sns.scatterplot(leaf_data[leaf_data['leaforder'] == 1], x="leafarea", y="phytinternode", hue='plantnb')

#############################################################################################

############################MULTISIM#########################################################

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

theresult = top_multisim(inputlist)

# The result is a data frame where each line corresponds to a leaf, and the columns are leafid, plantnb, shootid,
# leaforder, leafarea,  phytinternode, leafcoordx, leafcoordy, leafcoordz, leafanglea, leafangleb, simnumber, genotype.

splt = sns.scatterplot(theresult[(theresult['leaforder'] == 1) & (theresult['genotype'] == 'Chasselas')], x="leafarea",
                       y="phytinternode", hue='shootid')

# And now we can explore the results, for example by plotting the leaf area vs the internode length of all the leafs of
# a particular genotype and order, as above.  Or we can plot the leaf angle a against the hight of the leaf.

splt2 = sns.scatterplot(theresult[(theresult['leaforder'] == 1)], x="leafanglea", y="leafcoordz", hue='genotype',
                        alpha=0.4)
