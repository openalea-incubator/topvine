import IOtable

class get_dl(object):
    """  read distribution laws of leaf angles from input file (read_dl_leaf node) """ 
    def __init__(self):
        pass

    def __call__(self, f_dl):        d = file(f_dl, 'r')
        tab_d = IOtable.table_csv_str(d)         d.close()
        for i in range(len(tab_d)):
            tab_d[i][1], tab_d[i][2], tab_d[i][3] = int(tab_d[i][1]), float(tab_d[i][2]), float(tab_d[i][3])
    
        return tab_d
