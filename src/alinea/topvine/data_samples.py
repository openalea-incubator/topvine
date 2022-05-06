""" Provides sample data for testing topvine without reference to file paths, nor needs to call package manager
"""

from __future__ import absolute_import
import os
from six.moves import map
from six.moves import range

topvinedir = os.path.dirname(__file__)

def geom_file(fn = '/data/ex_geom2.csv'):
    from .read_geom_file import read_geom_file
    reader = read_geom_file()
    return reader(topvinedir + fn)
    
def shoot_file(fn='/data/ex_rammoy3.csv'):
    from .topologise import topologise
    reader = topologise()
    return reader(topvinedir + fn)
    
def dl_file(fn='/data/Law-leaf-2W-Grenache.csv'):
    from .get_dl import get_dl
    reader = get_dl()
    return reader(topvinedir + fn)
   
def allometry_file(fn='/data/allo_Grenache.csv'):
    from .read_allometry import read_allometry    
    reader = read_allometry()
    return reader(topvinedir + fn)

def normal_canopy():
    from .gen_normal_canopy import gen_normal_canopy
    generator = gen_normal_canopy()
    return generator(geom_file(), shoot_file(), dl_file())
    
def vine():
    from .tortl_inst_vine import tortl_inst_vine
    
    can = normal_canopy()
    n = len(can)
    return [tortl_inst_vine(can[i], dl_file(), allometry_file()) for i in range(n)]
    
def meteo_j(fn='/data/meteo_j_2007_californieROY.csv'):
    from . import IOtable
    
    meteo_file_path = topvinedir + fn
    f = open(meteo_file_path, 'r')
    table = IOtable.table_csv_str(f)
    f.close()
    for i in range (1,len(table)):
        table[i] = list(map(float, table[i]))

    meteo_dict = IOtable.conv_dataframe(IOtable.t_list(table))
    meteo_dict['DOY'] = list(map(int, meteo_dict['DOY']))
    
    return meteo_dict
