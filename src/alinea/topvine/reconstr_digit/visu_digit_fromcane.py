from __future__ import absolute_import
from numpy import array, pi
from openalea.plantgl.all import *
import random


import alinea.topvine.IOtable
from alinea.topvine.Obj3Dutils import *
from alinea.topvine.coor3D import *
from alinea.topvine.primitive import *
from six.moves import map
from six.moves import range

def random_cyl(r=1.,h=1.): 
    d = r*r +1
    while d > r*r :
        rx= random.uniform(-r,r) 
        ry= random.uniform(-r,r) 
        rz= random.uniform(0,h)
        d = rx*rx + ry*ry   

    return [rx,ry,rz]

def set_coord0(coord, Lin, Lb, omega):
    """ return actual leaf coordinates in a SOR defined by the parrallelogram (Lin, Lb, omega); omega in radians """
    coord = [coord[0]*Lb*cos(omega), coord[1]*Lb*cos(omega), coord[2]*Lin]
    d = coord[0]**2 + coord[1]**2
    return array([coord[0], coord[1], coord[2]+tan(omega)*sqrt(d)])

def set_coordF(coord, t, r_azi,r_incli):
    r_coord = RotateAxis (coord, r_azi, r_incli) #remplacer par coor3D.RotateAxis()
    return Translate (r_coord, t)#remplacer par coor3D.Translate()

def luz_label(sp_opt, num_phyI, num_shoot, num_plant, num_phyII=0):
    num_phy = num_phyI*10**2 + num_phyII
    lab = str(int(sp_opt*10**11+num_phy*10**6+num_shoot*10**3+num_plant))
    return (12-len(lab))*'0'+lab

def lII(nII, par):
    a, b, c = par[0], par[1], par[2]
    return a*nII*nII+b*nII+c#71 cm <-> 15f

def mef_digitcanefile(csv_file_path):
    f = open(csv_file_path, 'r')
    table = IOtable.table_csv_str (f)
    f.close()
    dat_dict = IOtable.conv_dataframe(IOtable.t_list(table))

    dat_dict['X'] = list(map(float, dat_dict['X']))
    dat_dict['Y'] = list(map(float, dat_dict['Y']))
    dat_dict['Z'] = list(map(float, dat_dict['Z']))
    dat_dict['Cane_nb'] = list(map(int, dat_dict['Cane_nb']))
    dat_dict['Plant_Nb'] = list(map(int, dat_dict['Plant_Nb']))
    dat_dict = {'X': dat_dict['X'], 'Y': dat_dict['Y'], 'Z':dat_dict['Z'] , 'Cane_nb': dat_dict['Cane_nb'], 'Plant_Nb': dat_dict['Plant_Nb']}

    nb_sh = max(dat_dict['Cane_nb'])
    nump_ini = min(dat_dict['Plant_Nb'])
    nump_fin = max(dat_dict['Plant_Nb'])
    nb_pl = nump_fin - nump_ini

    sh = []
    for i in range(1, nb_sh+1):
        v = []
        for j in range(len(dat_dict['Cane_nb'])):
            if dat_dict['Cane_nb'][j] == i:
                pt = array([dat_dict['X'][j], dat_dict['Y'][j], -dat_dict['Z'][j]])
                v.append(pt)
                nump = dat_dict['Plant_Nb'][j]

        sh.append([nump, i, v])

    return sh, nump_ini, nump_fin, nb_pl

#csv_file_path = r'H:\devel\topvine\topvine\data\digitCollectionMtp10_rideau_simple.csv'
#sh, nump_ini, nump_fin, nb_pl = mef_digitcanefile(csv_file_path)


def visu_digit_fromcane(csv_file_path, carto, topo, dazi, dincli, par_allo, l_petI=12., Hpied=None, MaScene = Scene(), forced_or=None):

    sh, nump_ini, nump_fin, nb_pl = mef_digitcanefile(csv_file_path)

    en = Cylinder(1,1,True,6)
    f = transformation(leaf0(), 1., 1., 1., -pi/2,0,0,0,0,0)

    pts_out = []# liste de points du nuage de points simule
    count=0
    for axe in range(len(sh)):
        ls_pt = sh[axe][2]
        nump = sh[axe][0]
        p_ini = carto[nump-nump_ini][0]
        for i in range(len(ls_pt)-1):

            ###rameaux
            p0, l, r, azi, incli = conv_cyl(ls_pt[i], ls_pt[i+1], 0.1)
            p0 = p0+p_ini
            e = transformation(en, 2*r, 2*r, l, azi, 3.14/2.-incli, 0, p0[0], p0[1], p0[2] )
            id1 = luz_label(2, 0, 0, 1, 0)#luz_label(1, i, 0, 1, 0)
            e.setName(id1)
            #e.setName(luz_label(1, i+1, axe+1, num_plant))#ajout d'un label canestra
            #MaScene.add(Shape(e, Material(Color3(181,111,30))))

            ###fI
            pt0 = random_cyl(r=1.,h=1.)
            pt_sc = set_coord0(pt0, l, l_petI, 0.)
            coordF = set_coordF(pt_sc, p0, azi, incli-pi/2.) #shoot.geom[2] *numpy.pi/180, (-90+CourbureActu)*numpy.pi/180

            if forced_or==None:
                if coordF[1]>0:
                    azi = random.gauss(dazi[0], dazi[1])*pi/180.
                    incli = random.gauss(dincli[0], dincli[1])*pi/180.
                else:
                    azi = random.gauss(dazi[0]+180., dazi[1])*pi/180.
                    incli = random.gauss(dincli[0], dincli[1])*pi/180.
            else: #ya liste d'orientations forcee
                azi, incli = forced_or[count][0]+random.gauss(0., pi/24.), forced_or[count][1]+random.gauss(0., pi/24.)#peut y ajouter une dispersion autour de ces valeurs


            lenf=topo[i][0]#140.#taille de feuille a calculer
            fI = transformation(f, lenf, lenf,1, azi,incli, 0.,coordF[0],coordF[1],coordF[2]) 
            id1 = luz_label(1, i, 0, axe, 0)#luz_label(1, 0, 0, 1, 0)
            fI.setName(id1)
            MaScene.add(Shape(fI, Material(Color3(23,140,31))))
            pts_out.append(array([coordF[0],coordF[1],coordF[2]]))
            count = count+1

            ###fII 
            #a finir
            nbII = len(topo[i])-1
            if nbII>=1:
                lramif = lII(nbII, par_allo)
                for j in range(nbII):
                    pt0 = random_cyl(r=1.,h=1.)
                    pt_sc = set_coord0(pt0, l, lramif, pi/2.)
                    coordF = set_coordF(pt_sc, p0, azi, incli-pi/2.) #shoot.geom[2] *numpy.pi/180, (-90+CourbureActu)*numpy.pi/180

                    if forced_or==None:
                        if coordF[1]>0:
                            azi = random.gauss(dazi[0], dazi[1])*pi/180.
                            incli = random.gauss(dincli[0], dincli[1])*pi/180.
                        else:
                            azi = random.gauss(dazi[0]+180., dazi[1])*pi/180.
                            incli = random.gauss(dincli[0], dincli[1])*pi/180.
                    else: #ya liste d'orientations forcee
                        azi, incli = forced_or[count][0]+random.gauss(0., pi/24.), forced_or[count][1]+random.gauss(0., pi/24.)


                    lenf=topo[i][j+1]
                    fII = transformation(f, lenf, lenf,1, azi,incli, 0.,coordF[0],coordF[1],coordF[2]) 
                    id1 = luz_label(1, i, j+1, axe, 0)#luz_label(1, 0, 0, 1, 0)
                    fII.setName(id1)
                    MaScene.add(Shape(fII, Material(Color3(23,140,31))))
                    pts_out.append(array([coordF[0],coordF[1],coordF[2]]))
                    count = count+1

    if Hpied !=None:#si une valeur est donnee pour Hpied ajoute un tronc vertical
        for plant in range(len(carto)):
            p0 = carto[plant][0]
            tc = transformation(en, 2.,2.,Hpied,0.,0.,0,p0[0],p0[1],p0[2])
            id1 = luz_label(2, 0, 0, 1, 0)#luz_label(1, i, 0, 1, 0)
            tc.setName(id1)
            #MaScene.add(Shape(tc, Material(Color3(202,106,27))))

    return MaScene, pts_out


#csv_file_path = r'H:\devel\topvine\topvine\data\digitCollectionMtp10_rideau_simple.csv'
#carto = [[array([-800.,    0.,    0.]), 12], [array([-700.,    0.,    0.]), 12], [array([-600.,    0.,    0.]), 12], [array([-500.,    0.,    0.]), 12], [array([-400.,    0.,    0.]), 12], [array([-300.,    0.,    0.]), 12], [array([-200.,    0.,    0.]), 12], [array([-100.,    0.,    0.]), 12], [array([ 0.,  0.,  0.]), 12], [array([ 100.,    0.,    0.]), 12], [array([ 200.,    0.,    0.]), 12], [array([ 300.,    0.,    0.]), 12], [array([ 400.,    0.,    0.]), 12], [array([ 500.,    0.,    0.]), 12], [array([ 600.,    0.,    0.]), 12], [array([ 700.,    0.,    0.]), 12], [array([ 800.,    0.,    0.]), 12], [array([ 900.,    0.,    0.]), 12]]
#topo = [[49.0], [77.0, 66.0], [99.0, 66.0, 66.0], [116.0, 66.0, 66.0, 66.0, 66.0], [128.0, 66.0, 66.0, 66.0], [136.0, 66.0, 66.0, 66.0, 66.0], [140.0, 66.0, 66.0, 66.0], [141.0, 66.0, 66.0, 66.0], [140.0, 66.0, 66.0], [135.0, 66.0, 66.0], [130.0, 66.0, 66.0], [122.0, 66.0], [114.0, 66.0], [106.0, 66.0], [97.0, 66.0], [90.0, 66.0], [83.0, 66.0], [78.0, 66.0], [75.0, 66.0], [74.0, 66.0], [74.0, 66.0, 66.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0]]

#MaScene = visu_digit_fromcane(csv_file_path, carto, topo, dazi=[90., 30.], dincli=[45., 20.], par_allo=[0.14331, 2.7161, -0.75459], l_petI=12., Hpied=160., MaScene = Scene())
#Monviewer=Viewer
#Monviewer.display(MaScene)


## ecrire turtle_inst adapte pour visu dynamique












