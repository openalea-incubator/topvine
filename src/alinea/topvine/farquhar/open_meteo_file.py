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

