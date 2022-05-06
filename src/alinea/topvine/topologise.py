# formerly 'topologise'
import IOtable

#add a step to check file format : write a specific procedure
class topologise(object):
    """ topologise rammoy files """ 

    def __call__(self, path):
        #check file format
        ram_moy = file(path, 'r')
        tab_rammoy = IOtable.table_csv(ram_moy) 
        ram_moy.close()
        topo = []
        for i in range(1,len(tab_rammoy)):#primary leaves
            topo.append([tab_rammoy[i][1]])

        for i in range(1,len(tab_rammoy)):#secondary leaves
            n = int(tab_rammoy[i][0])
            if n>0:
                for j in range(n):
                    topo[i-1].append(tab_rammoy[i][2])

        return topo

    def check_format (self, tab_rammoy):
        pass
