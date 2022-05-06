from __future__ import absolute_import
import os
#from os.path import join
from openalea.core.pkgmanager import PackageManager
from six.moves import map
from six.moves import range
pm = PackageManager()
pkg = pm.get('alinea.topvine') 
path_topvine = ''
if pkg :
    path_topvine = pkg.path

import sys
sys.path.insert(0, path_topvine)
import IOtable

def open_meteo_file(meteo_file_path):
    '''    open meteo file
    '''
    f = open(meteo_file_path, 'r')
    table = IOtable.table_csv_str (f)
    f.close()

    for i in range (1,len(table)):
        table[i] = list(map(float, table[i]))

    meteo_dict = IOtable.conv_dataframe(IOtable.t_list(table))

    return meteo_dict


def open_meteo_wb(meteo_file_path_j, meteo_file_path_h):
    """ utilise donnees du fichier journalier, sauf pour rayonnement pris dans fichier horaire"""
    #path_j = r'H:\devel\topvine\topvine\data\meteo_j_2007_californieROY.csv'
    dj = open_meteo_file(meteo_file_path_j)
    dj['DOY'] = list(map(int, dj['DOY']))


    #path_ = r'H:\devel\topvine\topvine\data\meteo_h_2007_californieROY.csv'
    d = open_meteo_file(meteo_file_path_h)
    d['DOY'] = list(map(int, d['DOY']))

    Hourly_Rg = {}# dictionnaire cle=DOY, valeur= liste de Rg horaire
    for i in range (min (d['DOY']), max (d['DOY'])+1, 1):
        Hourly_Rg[i] = []
        for j in range(len(d['DOY'])):
            if d['DOY'][j] == i:
                Hourly_Rg[i].append(d['Rg'][j])


    return dj, Hourly_Rg

def mef_meteo_wb(dj, Hourly_Rg, DOY):
    meteo_data = {}
    for i in range(len(dj['DOY'])):
        if dj['DOY'][i]==DOY:
            line = i
            break

    meteo_data['DOY'] = dj['DOY'][line]
    meteo_data['Tmoy'] = dj['Tmoy'][line]
    meteo_data['RH'] = dj['RH'][line]
    meteo_data['u'] = dj['u'][line]
    meteo_data['P'] = dj['P'][line]
    meteo_data['Irrigation'] = dj['Irrigation'][line]
    meteo_data['Eto_FAO56'] = dj['Eto_FAO56'][line]
    meteo_data['Rg'] = Hourly_Rg[DOY]

    return meteo_data
