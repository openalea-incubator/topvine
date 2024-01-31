from alinea.topvine.caribu.caribu import illuminate, getfromid
from alinea.topvine.topvine_2023 import topvine
from alinea.topvine.genodata import *

import pandas as pd
from statistics import median, mean
import seaborn as sns
# %gui qt5

def simulate(**kwargs):
    scene = topvine(branches=False, trunk=False, display=False, **kwargs)[0]
    cs, raw, agg = illuminate(scene)
    thekeys = {s.id: s.name for s in scene}
    theresult = pd.DataFrame(agg)

    thenewcolumn = []

    for key in theresult.index:
        thenewcolumn.append(thekeys[key])

    theresult['id'] = thenewcolumn

    for key in theresult.index:
        if theresult.loc[key]['id'] != thekeys[key]:
            print('error in ' + key)
    return theresult

class Simgenorder(object):

    def __init__(self):
        self.list=[]

    def add(self, couple):
        errline = "Error: simulation order is a list of pair of genotype and number"
        if len(couple) != 2 or not isinstance(couple[0],Genotype) or not isinstance(couple[1],int):
            print(errline)
        self.list.append(couple)

def multisim(orders):
    if not isinstance(orders,Simgenorder):
        errline = "Error: simulation order must be a Simgenorder object"
        print(errline)
        return

    resultlist=[]
    ornum=0
    for order in orders.list:
        ornum=ornum+1
        print("serving order "+str(ornum))

        for simno in range(order[1]):
            if simno%10 == 0:
                print("sim "+ str(simno+1)+ " of " + str(order[1]) )
            resultlist.append(simulate(gen=order[0]))

    return resultlist


myorder = Simgenorder()
myorder.add((Carignan,25))
myorder.add((Chasselas,25))
myorder.add((Clairette,25))
myorder.add((Marselan,25))
myorder.add((Mauzac,25))
myorder.add((Mourverde,25))
myorder.add((Petit_Verdot,25))
myorder.add((Vermentino,25))

grandresults = multisim(myorder)


###################### DATA ANALYSIS ##########################################

medians = []

for r in grandresults:
    medians.append(median(r["Ei"]))

sns.histplot(medians[0:25])
sns.histplot(medians[25:50])
sns.histplot(medians[50:75])
sns.histplot(medians[75:100])
sns.histplot(medians[100:125])
sns.histplot(medians[125:150])
sns.histplot(medians[150:175])
sns.histplot(medians[175:200])

means = []

for r in grandresults:
    means.append(mean(r["Ei"]))

sns.histplot(means[1:25])


minslist = []

for r in grandresults:
    mins = 0
    for ei in r["Ei"]:
        if ei<100:
            mins=mins+1
    minslist.append(mins)

sns.histplot(minslist[0:25])
sns.histplot(minslist[25:50])
sns.histplot(minslist[50:75])
sns.histplot(minslist[75:100])
sns.histplot(minslist[100:125])
sns.histplot(minslist[125:150])
sns.histplot(minslist[150:175])
sns.histplot(minslist[175:200])


ratiolist = []
for r in range(0,len(medians)):
    ratiolist.append(medians[r]/minslist[r])

sns.histplot(ratiolist[0:25])
sns.histplot(ratiolist[25:50])
sns.histplot(ratiolist[50:75])
sns.histplot(ratiolist[75:100])
sns.histplot(ratiolist[100:125])
sns.histplot(ratiolist[125:150])
sns.histplot(ratiolist[150:175])
sns.histplot(ratiolist[175:200])

# ratio SF primaire secondaire

rprimsec = []
for r in grandresults:
    pri=0
    sec=0
    for line in range(0,len(r)):
        if getfromid(r.iloc[line]['id'],'phy')%100 == 0:
            pri=pri+r.iloc[line]['area']
        else:
            sec=sec+r.iloc[line]['area']
    rprimsec.append(pri/(pri+sec))


sns.histplot(rprimsec[0:25])
sns.histplot(rprimsec[25:50])
sns.histplot(rprimsec[50:75])
sns.histplot(rprimsec[75:100])
sns.histplot(rprimsec[100:125])
sns.histplot(rprimsec[125:150])
sns.histplot(rprimsec[150:175])
sns.histplot(rprimsec[175:200])

sdat = pd.DataFrame({'ratioprimsec':rprimsec,'Ei medians': medians,'genotypes':gennames})
sns.scatterplot(sdat,x='ratioprimsec',y='Ei medians',hue="genotypes").set(xlabel="ratio of primary to secondary leaf surface area")

plantnumbers=[getfromid(grandresults[0].iloc[line]['id'], 'plant') for line in range(0, len(grandresults[0]))]
leaforder=[min(getfromid(grandresults[0].iloc[line]['id'], 'phy')%100,1) + 1 for line in range(0, len(grandresults[0]))]

grandresults[0].insert(loc=4,column='plnumbers',value=plantnumbers)
grandresults[0].insert(loc=5,column='leaforder',value=leaforder)


ei_perplant = [0] * len(set(plantnumbers))
feuilles_perplant = [0] * len(set(plantnumbers))
eiMedian_perplant = [0] * len(set(plantnumbers))
eiMean_perplant = [0] * len(set(plantnumbers))
SF_prim = [0] * len(set(plantnumbers))
SF_sec = [0] * len(set(plantnumbers))
SF_tot = [0] * len(set(plantnumbers))
SF_prop = [0] * len(set(plantnumbers))

for plant in range(0,len(set(plantnumbers))):
    plantdata = grandresults[0][grandresults[0]['plnumbers'].isin([plant])]
    ei_perplant[plant] = sum(plantdata['Ei'])
    feuilles_perplant[plant] = len(plantdata['Ei'])
    eiMedian_perplant[plant] = median(plantdata['Ei'])
    eiMean_perplant[plant] = mean(plantdata['Ei'])
    SF_prim[plant] = sum(plantdata[plantdata['leaforder'].isin([1])]['area'])
    SF_sec[plant] = sum(plantdata[plantdata['leaforder'].isin([2])]['area'])
    SF_tot[plant] = SF_prim[plant] + SF_sec[plant]
    SF_prop[plant] = SF_prim[plant] / SF_tot[plant]

psdat = pd.DataFrame({'ei_perplant': ei_perplant, 'feuilles_perplant': feuilles_perplant, 'eiMedian_perplant': eiMedian_perplant,
                      'eiMean_perplant': eiMean_perplant, 'SF_prim': SF_prim, 'SF_sec': SF_sec, 'SF_tot': SF_tot, 'SF_prop': SF_prop})

sns.scatterplot(psdat,x='SF_tot',y='ei_perplant').set(xlabel="leaf surface area")



########################################################################################################################
######  ADDING 4 COLUMNS TO THE RESULT AND PRINTING IT CSV STYLE ########



gennames = []
for pair in myorder.list:
    for sim in range(0,pair[1]):
        gennames.append(pair[0].name)


simnumber=0
for r in grandresults:
    genocol = [gennames[simnumber] for line in range(0, len(r))]
    simnumber += 1
    simnumcol = [simnumber for line in range(0, len(r))]
    plantnumbers = [getfromid(r.iloc[line]['id'], 'plant') for line in range(0, len(r))]
    leaforder = [min(getfromid(r.iloc[line]['id'], 'phy') % 100, 1) + 1 for line in
                 range(0, len(r))]
    r.insert(loc=4, column='plnumbers', value=plantnumbers)
    r.insert(loc=5, column='leaforder', value=leaforder)
    r.insert(loc=6, column='genotype', value=genocol)
    r.insert(loc=7, column='simnumber', value=simnumcol)
    r.to_csv("lightdata.csv", mode='a')


