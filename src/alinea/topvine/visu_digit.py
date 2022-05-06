import IOtable
#from math import *
from openalea.plantgl.all import *
import primitive
from math import pi

class visu_digit(object):
    """  visualise digitalisation data from .d3d file """ 

    def __init__(self):
        pass


    def __call__(self, f_d3D, ang_cor, coord, MaScene = Scene(), nump=1, teta_row=0):
        f = file(f_d3D, 'r')
        tab = IOtable.table_csv(f) #a remplacer part d3d / utiliser IOtable.table_txt
        f.close()

        MonViewer = Viewer
        xpied, ypied, zpied = coord[0], coord[1], coord[2]

        for i in range (len(tab)) :                       
            feuille = primitive.leaf0(tab[i][7]/100)
            #fI = primitive.transformation(feuille,1,1,1,(tab[i][4])*pi/180 + ang_cor*pi/180,tab[i][6]*pi/180, -tab[i][5]*pi/180,tab[i][1]*0.01+ xpied,tab[i][2]*0.01+ ypied,-tab[i][3]*0.01+zpied) 
            fI = primitive.transformation(feuille,1,1,1,(tab[i][4])*pi/180 + ang_cor*pi/180,tab[i][6]*pi/180, -tab[i][5]*pi/180,tab[i][1]*0.01,tab[i][2]*0.01,-tab[i][3]*0.01) 
            fII = primitive.transformation(fI,1,1,1,teta_row*pi/180, 0, 0,xpied,ypied,zpied) #ajuste selon orientation du rang
            #scale = long mesuree / longeur feuille patron (100mm) ; translation = valeurs x, y , -z exprimees en m ; rotation : azi, rouli, -inclinaison  RQ: modif de l'azi = -pi/2 pour certaines digit (ex: 2fs 3fs 3fg) ms certaines ont pas l'air de marcher ((ex : 1fs 2fg : marche avec +pi/2))
            fIs = Shape(fII, Material(Color3(0,255,0)))
            fIs.setName(self.vine_label(1, i+1, 1, nump))#ajout d'un label canestra
            MaScene.add(fIs)

        MonViewer.display(MaScene)

        return MaScene

    def vine_label(self, sp_opt, num_phy, num_ram, num_vine):
        lab = str(int(sp_opt*10**11+num_phy*10**6+num_ram*10**3+num_vine))
        return (12-len(lab))*'0'+lab
