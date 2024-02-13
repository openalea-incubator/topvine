from multisim import Simgenorder, multisim
from alinea.topvine.genodata import *
from statistics import median, mean
import numpy as np
import seaborn as sns


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


area_uniquevalueratios = []
area_median = []
ratioOneByTwo = []
percentageTwoOfAll = []

for r in grandresults:
    area_uniquevalueratios.append(len(r['area'].value_counts()) / len(r['area']))
    area_median.append(median(r['area']))
    ratioOneByTwo.append(len(np.where(r['leaforder']==1)[0])/len(np.where(r['leaforder']==2)[0]))
    percentageTwoOfAll.append(len(np.where(r['leaforder']==2)[0])/len(r['leaforder']))

areadf = pd.DataFrame({'unique_area_ratio': area_uniquevalueratios, 'area_median' : area_median , 'ratio': ratioOneByTwo, 'percent' :percentageTwoOfAll, 'genotype': gennames})
sns.boxplot(areadf, x="genotype", y="unique_area_ratio")
sns.scatterplot(areadf, x="area_median", y="unique_area_ratio")
sns.scatterplot(areadf, x="ratio", y="unique_area_ratio",hue="genotype")
sns.scatterplot(areadf, x="ratio", y="percent",hue="genotype")