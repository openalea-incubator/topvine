from __future__ import absolute_import
from . import leaf
from . import shoot
from .V3Dutils import *
from .Obj3Dutils import *
import numpy
from numpy import sqrt, arccos, array, cos, sin, pi, ceil
from six.moves import range



def allo_LN(allo,N):
    L = allo[0]*N + allo[1]   
    if L<=0.005:
        L=0.005
    
    return L*0.001#en m

def set_coordF(coord, t, r_azi,r_incli):
    r_coord = RotateAxis (coord, r_azi, r_incli) #remplacer par coor3D.RotateAxis()
    return Translate (r_coord, t)#remplacer par coor3D.Translate()


def NSstatus(coord, limNS):
    if coord[1]<limNS:
        return 1#N
    else:
        return 0#S

def tortl_inst_vine(ls_shoots, lawf, allo):
    #a terme : devrait etre une methode de la classe topiary
    omega = 45*pi/180. 
    LongPetiole = 0.12
    visu_en = True

    tortl_inst = []

    #sh = ls_shoots[0][0]#prend premiere shoot de la premiere plante

    for ram in range(len(ls_shoots)):
        sh = ls_shoots[ram]

        NombrePhyto = len(sh.topo)
        LongRamMoy = allo_LN(allo[0],NombrePhyto) #en metres
        LimNS = 0. 
                

        #initialise parametres du rameau
        LongRam = sh.geom[5]*LongRamMoy
        LongPhyto = LongRam/NombrePhyto
        CourbureActu = sh.geom[3]  
        NumInflexion =  ceil(sh.geom[6]*NombrePhyto)
        Xi = sh.geom[1][0]*0.01 
        Yi = sh.geom[1][1]*0.01 
        Zi = sh.geom[1][2]*0.01

        #axe principal
        inst_axe = []
        for phyto in range(NombrePhyto) :
                inst_phyt = []

                if phyto < NumInflexion :
                    dCourbure = sh.geom[3]/2 / NumInflexion
                else : 
                    dCourbure = sh.geom[3]/2 / (NombrePhyto - NumInflexion)

                Xii =  cos(CourbureActu*pi/180) * LongPhyto * cos(sh.geom[2] *pi/180) + Xi
                Yii =  cos(CourbureActu*pi/180) * LongPhyto * sin(sh.geom[2] *pi/180) + Yi
                Zii =  sin(CourbureActu*pi/180) * LongPhyto + Zi 

                #en
                p0, l, r, azi, incli = conv_cyl(array([Xi,Yi,Zi]), array([Xii,Yii,Zii]), 0.05)
                inst_phyt.append([l, azi*180./pi, (pi/2-incli)*180./pi])#angles en degres

                #pet
                Lin = LongPhyto
                Lb = LongPetiole
                coord = sh.topo[phyto][0].set_coord0(Lin, Lb, omega)
                coordF = set_coordF(coord, array([Xi,Yi,Zi]), sh.geom[2] *pi/180, (-90+CourbureActu)*pi/180)
                p0, l, r, azi, incli = conv_cyl(array([Xii,Yii,Zii]), array(coordF), 0.05)
                inst_phyt[0] = inst_phyt[0] + [l, azi*180./pi, (3.14/2-incli)*180./pi]

                #limbe
                lmax = sh.topo[phyto][0].len/1000. #en m
                NSstat = NSstatus(coordF, LimNS)
                angles = sh.topo[phyto][0].set_anglesF(lawf, NSstat)
                tir1 = angles[1]
                tir2 = -(90-angles[0])
                inst_phyt[0] = inst_phyt[0] + [lmax, lmax, tir1, tir2]

                #print phyto, inst_phyt
                inst_axe.append(inst_phyt)
        
                Xi =  Xii
                Yi =  Yii
                Zi =  Zii
                CourbureActu = CourbureActu + dCourbure

        tortl_inst.append(inst_axe)

        #axes secondaires
        CourbureActu = sh.geom[3]  
        Xi = sh.geom[1][0]*0.01 
        Yi = sh.geom[1][1]*0.01 
        Zi = sh.geom[1][2]*0.01

        for phyto in range(NombrePhyto) :

                if phyto < NumInflexion :
                    dCourbure = sh.geom[3]/2 / NumInflexion
                else : 
                    dCourbure = sh.geom[3]/2 / (NombrePhyto - NumInflexion)

                Xii =  cos(CourbureActu*pi/180) * LongPhyto * cos(sh.geom[2] *pi/180) + Xi
                Yii =  cos(CourbureActu*pi/180) * LongPhyto * sin(sh.geom[2] *pi/180) + Yi
                Zii =  sin(CourbureActu*pi/180) * LongPhyto + Zi 

                if len(sh.topo[phyto])>1:
                    inst_axe2 = []
                    Lb = allo_LN(allo[1], len(sh.topo[phyto])-1) #en metres
                    for i in range (1,len(sh.topo[phyto])):
                        inst_phyt = []

                        #en = 0
                        inst_phyt.append([0., 0., 0.])

                        #pet
                        coord = sh.topo[phyto][i].set_coord0(Lin, Lb, omega)
                        coordF = set_coordF(coord, array([Xi,Yi,Zi]), sh.geom[2] *pi/180, (-90+CourbureActu)*pi/180)
                        p0, l, r, azi, incli = conv_cyl(array([Xii,Yii,Zii]), array(coordF), 0.05)
                        inst_phyt[0] = inst_phyt[0] + [l, azi*180./pi, (3.14/2-incli)*180./pi]

                        #limbe
                        lmax = sh.topo[phyto][i].len/1000. #en m
                        NSstat = NSstatus(coordF, LimNS)
                        angles = sh.topo[phyto][i].set_anglesF(lawf, NSstat)
                        tir1 = angles[1]
                        tir2 = -(90-angles[0])

                        inst_phyt[0] = inst_phyt[0] + [lmax, lmax, tir1, tir2]

                        inst_axe2.append(inst_phyt)

                    tortl_inst[ram][phyto].append(inst_axe2)#remplacer 0 par ram si fait une plante

                Xi =  Xii
                Yi =  Yii
                Zi =  Zii
                CourbureActu = CourbureActu + dCourbure


    return tortl_inst#Xi#inst_phyt
