from __future__ import absolute_import
from numpy import *
from six.moves import range

def groupOutput_phyto(caribu_dict, key='EiSup', sum_ =False):
    # add a unique id per phytomer
    caribu_dict['id'], caribu_dict['av'] =[], []
    for i in range (len(caribu_dict[key])):
        opt = str(int(caribu_dict['Opt'][i]))
        phyto = str(int(caribu_dict['Plt'][i]))
        phyto = (4-len(phyto))*'0'+phyto
        shoot = str(int(caribu_dict['Opak'][i]))
        shoot = (3-len(shoot))*'0'+shoot
        pl = str(int(caribu_dict['Elt'][i]))
        pl = (3-len(pl))*'0'+pl
        lab = opt+phyto+shoot+pl #label luzerne
        caribu_dict['id'].append(lab)

    #compute average for elements of key with the same id
    i=0
    av = {}
    id = caribu_dict['id'][i]
    while i<len(caribu_dict['id']):
        v, s = [], []
        while id == caribu_dict['id'][i]:
            v.append(caribu_dict[key][i])
            s.append(caribu_dict['Area'][i])
            i=i+1
            if i==len(caribu_dict['id']):
                break

        if sum_ == False:
            av[id] = [id, sum(v)/sum(s), sum(s)]#pondere par taille des triangles, renvoie aussi surface
        else:
            av[id] = [id, sum(v), sum(s)]

        if i==len(caribu_dict['id']):
            break
        else:
            id = caribu_dict['id'][i]


    #add the average into the av column
    for i in range(len(caribu_dict[key])):
        caribu_dict['av'].append(av[caribu_dict['id'][i]][1])

    return caribu_dict, av#caribu_dict#['output, ']




