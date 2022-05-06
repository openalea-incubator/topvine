from __future__ import absolute_import
from . import leaf
from . import shoot
from .coor3D import *
from .primitive import *
import math
from six.moves import range

class Topiary:

    def __init__(self, scene, shoot, allo, lawf, omega = 45*numpy.pi/180., LongPetiole = 0.12, visu_en = True, num_vine=1, num_shoot=1):
        """ add 3D shoot to PlantGL scene object """
        #faire general ou pas?? possibilite de prendre entree topo + L + + arc ou forme topiaire?
        #ici topiairy de rameau de vigne
        #TT pour eventuellement piloter changement de loi de distibution avec une date et evolution des angles ?
        #->trellis_opt=['TTnone','trellisnone'] en parametre d'entree

        NombrePhyto = len(shoot.topo)
        LongRamMoy = self.allo_LN(allo[0],NombrePhyto) #en metres
        LimNS = 0. 
        

        #initialise parametres du rameau
        LongRam = shoot.geom[5]*LongRamMoy
        LongPhyto = LongRam/NombrePhyto
        CourbureActu = shoot.geom[3]  
        NumInflexion =  math.ceil(shoot.geom[6]*NombrePhyto)
        Xi = shoot.geom[1][0]*0.01 
        Yi = shoot.geom[1][1]*0.01 
        Zi = shoot.geom[1][2]*0.01

        for phyto in range(NombrePhyto) :
            if phyto < NumInflexion :
                dCourbure = shoot.geom[3]/2 / NumInflexion
            else : 
                dCourbure = shoot.geom[3]/2 / (NombrePhyto - NumInflexion)

            Xii =  numpy.cos(CourbureActu*numpy.pi/180) * LongPhyto * numpy.cos(shoot.geom[2] *numpy.pi/180) + Xi
            Yii =  numpy.cos(CourbureActu*numpy.pi/180) * LongPhyto * numpy.sin(shoot.geom[2] *numpy.pi/180) + Yi
            Zii =  numpy.sin(CourbureActu*numpy.pi/180) * LongPhyto + Zi
    
            #mise en place de l'entre noeud I
            if visu_en == True :
                en = en0()
                t_en = transformation(en,0.01,0.01,LongPhyto, shoot.geom[2]*numpy.pi/180,(90-CourbureActu)*numpy.pi/180,0, Xi,Yi,Zi)
                t_ens = Shape(t_en, Material(Color3(198,179,37)))
                t_ens.setName(self.vine_label(0, (phyto+1), num_shoot, num_vine))
                scene.add(t_ens)

            #mise en place de la feuille I
            Lin = LongPhyto
            Lb = LongPetiole
            coord = shoot.topo[phyto][0].set_coord0(Lin, Lb, omega)
            coordF = self.set_coordF(coord, numpy.array([Xi,Yi,Zi]), shoot.geom[2] *numpy.pi/180, (-90+CourbureActu)*numpy.pi/180)

            NSstat = self.NSstatus(coordF, LimNS)
            angles = shoot.topo[phyto][0].set_anglesF(lawf, NSstat)
            tir1 = angles[1]*numpy.pi/180#Tirage_anglesF (Tab_loi_feuilles[2][0], Tab_loi_feuilles[2][1], Tab_loi_feuilles[2][2])*numpy.pi/180
            tir2 = -(90-angles[0])*numpy.pi/180#-(90-Tirage_anglesF (Tab_loi_feuilles[0][0], Tab_loi_feuilles[0][1], Tab_loi_feuilles[0][2]))*numpy.pi/180

            f = leaf0() # a remplacer par primitive.leaf0()
            fI = transformation(f,shoot.topo[phyto][0].len*0.01,shoot.topo[phyto][0].len*0.01,1,tir1 ,0, tir2,coordF[0],coordF[1],coordF[2]) 
            fIs = Shape(fI, Material(Color3(23,140,31)))
            fIs.setName(self.vine_label(1, int(shoot.topo[phyto][0].id), num_shoot, num_vine)) #stockage d'un label canestra dans l'objet geom
            scene.add(fIs)


            #mise en place des feuilles II
            if len(shoot.topo[phyto])>1:
                Lb = self.allo_LN(allo[1], len(shoot.topo[phyto])-1) #en metres
                for i in range (1,len(shoot.topo[phyto])):
                    coord = shoot.topo[phyto][i].set_coord0(Lin, Lb, omega)
                    coordF = self.set_coordF(coord, numpy.array([Xi,Yi,Zi]), shoot.geom[2] *numpy.pi/180, (-90+CourbureActu)*numpy.pi/180)
        
                    NSstat = self.NSstatus(coordF, LimNS)
                    angles = shoot.topo[phyto][i].set_anglesF(lawf, NSstat)
                    tir1 = angles[1]*numpy.pi/180#Tirage_anglesF (Tab_loi_feuilles[2][0], Tab_loi_feuilles[2][1], Tab_loi_feuilles[2][2])*numpy.pi/180
                    tir2 = -(90-angles[0])*numpy.pi/180#-(90-Tirage_anglesF (Tab_loi_feuilles[0][0], Tab_loi_feuilles[0][1], Tab_loi_feuilles[0][2]))*numpy.pi/180
        
                    f = leaf0()
                    fII = transformation(f,shoot.topo[phyto][i].len*0.01,shoot.topo[phyto][i].len*0.01,1,tir1 ,0, tir2,coordF[0],coordF[1],coordF[2]) 
                    fIIs = Shape(fII, Material(Color3(23,140,31)))
                    fIIs.setName(self.vine_label(1, int(shoot.topo[phyto][i].id), num_shoot, num_vine))
                    scene.add(fIIs)


            Xi =  Xii
            Yi =  Yii
            Zi =  Zii
            CourbureActu = CourbureActu + dCourbure

        self.scene = scene


    def allo_LN(self,allo,N):
        L = allo[0]*N + allo[1]   
        if L<=0.005:
            L=0.005
    
        return L*0.001#en m

    def set_coordF(self, coord, t, r_azi,r_incli):
        r_coord = RotateAxis (coord, r_azi, r_incli) #remplacer par coor3D.RotateAxis()
        return Translate (r_coord, t)#remplacer par coor3D.Translate()


    def NSstatus(self,coord, limNS):
        if coord[1]<limNS:
            return 1#N
        else:
            return 0#S

    def vine_label(self, sp_opt, num_phy, num_ram, num_vine):
        lab = str(int(sp_opt*10**11+num_phy*10**6+num_ram*10**3+num_vine))
        return (12-len(lab))*'0'+lab

