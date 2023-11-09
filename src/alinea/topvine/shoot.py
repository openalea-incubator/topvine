from __future__ import absolute_import
from __future__ import print_function
import numpy
import random
from . import leaf
from six.moves import range

class Shoot:
    def __init__(self, Pgeom, topol, law):
        self.geom = Pgeom
        self.topo = []
        for i in range(len(topol)):
            self.topo.append([leaf.Leaf(rand='Cyl', lawf=law, len=topol[i][0],id=str((i+1)*100))])#id leaf I = rang phyto*100

        for i in range(len(self.topo)):
            if len(topol[i])>1:
                for j in range(1,len(topol[i])):
                    self.topo[i].append(leaf.Leaf(rand='Cyl', lawf=law, len=topol[i][j],id=str((i+1)*100+j)))#id leaf II = rang phyto*100+rang feuilles II

    def __str__(self): #appeler quand 'print obj'
        """ display shoot object as a string """
        res = 'geom: '+str(self.geom)+'\n'
        res = res + 'topo: '+'\n'+'_'+'\n'
        for i in range(len(self.topo)):
            x1,x2='|','-'
            res = res + x1
            if len(self.topo[i])>1:
                for j in range(1,len(self.topo[i])):
                    res = res + x2

                res = res + '\n'
            else:
                res = res + '\n'

        return res

    def display(self,opt='i'): 
        """ display shoot object; option: s=string, l=leaf length, c=coord, i=id"""
        res = 'geom: '+str(self.geom)+'\n'
        res = res + 'topo: '+'\n'+'_'+'\n'
        for i in range(len(self.topo)):
            if opt=='s':
                x1,x2='|','-'
            elif opt=='l':
                x1=str(self.topo[i][0].len)+'-'
            elif opt=='c':
                x1=str(self.topo[i][0].coord)
            elif opt=='i':
                x1=str(self.topo[i][0].id)+'-'

            res = res + x1
            if len(self.topo[i])>1:
                for j in range(1,len(self.topo[i])):
                    if opt=='l':
                        x2=str(self.topo[i][j].len)+'-'
                    elif opt=='c':
                        x2=str(self.topo[i][j].coord)
                    elif opt=='i':
                        x2=str(self.topo[i][j].id)+'-'

                    res = res + x2

                res = res + '\n'
            else:
                res = res + '\n'

        print(res)

    def get_nbII(self,topo='none'):
        """ returns a list of secondary leaf number per rank ; can be applied to shoot objects (no arguments), or to simple topology with leaf lengths only (as required to define shoot objects)"""
        res=[]
        if topo=='none':
            topo = self.topo

        for i in range(len(topo)):
            res.append(len(topo[i])-1)

        return res

    def get_topol(self):
        """ returns a simple topology with leaf lengths (as required to define shoot objects)"""
        res=[]
        for i in range(len(self.topo)):
            res.append([self.topo[i][0].len])

        for i in range(len(self.topo)):
            for j in range(1,len(self.topo[i])):
                res[i].append(self.topo[i][j].len)

        return res

    def writeshoot(self,f):
        pass

    def update_topo(self, new_topo, law):
        n = len(self.topo)
        deltaI = len(new_topo)- n
        if deltaI>0:#add I phytomer           
            for i in range(deltaI):
                self.topo.append([leaf.Leaf(rand='Cyl', lawf=law, id=str((n+i+1)*100))])

        if deltaI<0: #remove I phytomer
            self.topo=self.topo[:len(new_topo)]

        deltaII = numpy.array(self.get_nbII(new_topo))-numpy.array(self.get_nbII())
        for i in range(len(deltaII)):
            n2 = len(self.topo[i])
            if deltaII[i]>0:#add II phytomer           
                for j in range(deltaII[i]):
                    self.topo[i].append(leaf.Leaf(rand='Cyl', lawf=law, id=str((i+1)*100+j+n2)))
    
            if deltaII[i]<0: #remove II phytomer
                self.topo[i]=self.topo[i][:len(new_topo[i])]

        for i in range(len(self.topo)):#update len
            for j in range(len(self.topo[i])):
                self.topo[i][j].len = new_topo[i][j]

        #return deltaII


class Shoot_2023:
    def __init__(self, Pgeom, topol, law):
        self.geom = Pgeom
        self.topo = []
        for i in range(len(topol[0])):
            self.topo.append(
                [leaf.Leaf(rand='Cyl', lawf=law, len=topol[0][i][0], lin=topol[1][i][0], id=str((i + 1) * 100))])  # id leaf I = rang phyto*100

        for i in range(len(self.topo)):
            if len(topol[0][i]) > 1:
                for j in range(1, len(topol[0][i])):
                    self.topo[i].append(leaf.Leaf(rand='Cyl', lawf=law, len=topol[0][i][j], id=str(
                        (i + 1) * 100 + j)))  # id leaf II = rang phyto*100+rang feuilles II

    def __str__(self):  # appeler quand 'print obj'
        """ display shoot object as a string """
        res = 'geom: ' + str(self.geom) + '\n'
        res = res + 'topo: ' + '\n' + '_' + '\n'
        for i in range(len(self.topo)):
            x1, x2 = '|', '-'
            res = res + x1
            if len(self.topo[i]) > 1:
                for j in range(1, len(self.topo[i])):
                    res = res + x2

                res = res + '\n'
            else:
                res = res + '\n'

        return res

    def display(self, opt='i'):
        """ display shoot object; option: s=string, l=leaf length, c=coord, i=id"""
        res = 'geom: ' + str(self.geom) + '\n'
        res = res + 'topo: ' + '\n' + '_' + '\n'
        for i in range(len(self.topo)):
            if opt == 's':
                x1, x2 = '|', '-'
            elif opt == 'l':
                x1 = str(self.topo[i][0].len) + '-'
            elif opt == 'c':
                x1 = str(self.topo[i][0].coord)
            elif opt == 'i':
                x1 = str(self.topo[i][0].id) + '-'

            res = res + x1
            if len(self.topo[i]) > 1:
                for j in range(1, len(self.topo[i])):
                    if opt == 'l':
                        x2 = str(self.topo[i][j].len) + '-'
                    elif opt == 'c':
                        x2 = str(self.topo[i][j].coord)
                    elif opt == 'i':
                        x2 = str(self.topo[i][j].id) + '-'

                    res = res + x2

                res = res + '\n'
            else:
                res = res + '\n'

        print(res)

    def get_nbII(self, topo='none'):
        """ returns a list of secondary leaf number per rank ; can be applied to shoot objects (no arguments), or to simple topology with leaf lengths only (as required to define shoot objects)"""
        res = []
        if topo == 'none':
            topo = self.topo

        for i in range(len(topo)):
            res.append(len(topo[i]) - 1)

        return res

    def get_topol(self):
        """ returns a simple topology with leaf lengths (as required to define shoot objects)"""
        res = []
        for i in range(len(self.topo)):
            res.append([self.topo[i][0].len])

        for i in range(len(self.topo)):
            for j in range(1, len(self.topo[i])):
                res[i].append(self.topo[i][j].len)

        return res

    def writeshoot(self, f):
        pass

    def update_topo(self, new_topo, law):
        n = len(self.topo)
        deltaI = len(new_topo) - n
        if deltaI > 0:  # add I phytomer
            for i in range(deltaI):
                self.topo.append([leaf.Leaf(rand='Cyl', lawf=law, id=str((n + i + 1) * 100))])

        if deltaI < 0:  # remove I phytomer
            self.topo = self.topo[:len(new_topo)]

        deltaII = numpy.array(self.get_nbII(new_topo)) - numpy.array(self.get_nbII())
        for i in range(len(deltaII)):
            n2 = len(self.topo[i])
            if deltaII[i] > 0:  # add II phytomer
                for j in range(deltaII[i]):
                    self.topo[i].append(leaf.Leaf(rand='Cyl', lawf=law, id=str((i + 1) * 100 + j + n2)))

            if deltaII[i] < 0:  # remove II phytomer
                self.topo[i] = self.topo[i][:len(new_topo[i])]

        for i in range(len(self.topo)):  # update len
            for j in range(len(self.topo[i])):
                self.topo[i][j].len = new_topo[i][j]

        # return deltaII