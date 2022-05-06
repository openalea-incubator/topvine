import cPickle as pickle
from os.path import join


def pickleD(data, folder_dir, name):
    '''    pickle dump that returns file path
    '''
    path_name = join(folder_dir, name)#r'H:\Lusignan\Analyses\test_plpy4.dat'
    out = file(path_name, 'w')
    pickle.dump(data, out) 
    out.close()

    return path_name
