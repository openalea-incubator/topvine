import IOtable
from numpy import array


class read_stand_file(object):
    """  get stand caracteristics from csv stand file """ 

    def __init__(self):
        pass


    def __call__(self, path):
        f = file(path)
        tab = IOtable.table_csv_str(f)
        f.close()

        for i in range(len(tab)): #[array(x,y,z), n]
            tab[i] = [array([float(tab[i][0]), float(tab[i][1]), float(tab[i][2])]), int(tab[i][3])]
            

        return tab
