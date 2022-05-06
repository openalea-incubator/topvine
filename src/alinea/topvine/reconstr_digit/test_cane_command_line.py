
from numpy import array, pi
from openalea.plantgl.all import *
import random

path_topvine = r'H:\devel\topvine\topvine'
import sys
sys.path.insert(0, path_topvine)

import IOtable
from Obj3Dutils import *
from coor3D import *
from primitive import *

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
    f = file(csv_file_path, 'r')
    table = IOtable.table_csv_str (f)
    f.close()
    dat_dict = IOtable.conv_dataframe(IOtable.t_list(table))

    dat_dict['X'] = map(float, dat_dict['X'])
    dat_dict['Y'] = map(float, dat_dict['Y'])
    dat_dict['Z'] = map(float, dat_dict['Z'])
    dat_dict['Cane_nb'] = map(int, dat_dict['Cane_nb'])
    dat_dict['Plant_Nb'] = map(int, dat_dict['Plant_Nb'])
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


def extract_plant(dict, nump):
    plant_dict = {}
    idp = (3-len(str(nump)))*'0'+str(nump)
    for k in dict.keys():
        if str(k)[0]=='1' and str(k)[-3:] == str(idp):#opt=1 et nump=idp
            plant_dict[k]=dict[k]

    return plant_dict




##########
## 3D plant reconstrctuction
##########

#digit file path
csv_file_path = r'H:\devel\topvine\topvine\data\digitCollectionMtp10_rideau_simple_a.csv'#r'H:\devel\topvine\topvine\data\digitCollectionMtp10_rideau_simple.csv'
#map of the plot (plant positions)
carto = [[array([-800.,    0.,    0.]), 12], [array([-700.,    0.,    0.]), 12], [array([-600.,    0.,    0.]), 12], [array([-500.,    0.,    0.]), 12], [array([-400.,    0.,    0.]), 12], [array([-300.,    0.,    0.]), 12], [array([-200.,    0.,    0.]), 12], [array([-100.,    0.,    0.]), 12], [array([ 0.,  0.,  0.]), 12], [array([ 100.,    0.,    0.]), 12], [array([ 200.,    0.,    0.]), 12], [array([ 300.,    0.,    0.]), 12], [array([ 400.,    0.,    0.]), 12], [array([ 500.,    0.,    0.]), 12], [array([ 600.,    0.,    0.]), 12], [array([ 700.,    0.,    0.]), 12], [array([ 800.,    0.,    0.]), 12], [array([ 900.,    0.,    0.]), 12]]
#vaerage shoot topology
topo = [[49.0], [77.0, 66.0], [99.0, 66.0, 66.0], [116.0, 66.0, 66.0, 66.0, 66.0], [128.0, 66.0, 66.0, 66.0], [136.0, 66.0, 66.0, 66.0, 66.0], [140.0, 66.0, 66.0, 66.0], [141.0, 66.0, 66.0, 66.0], [140.0, 66.0, 66.0], [135.0, 66.0, 66.0], [130.0, 66.0, 66.0], [122.0, 66.0], [114.0, 66.0], [106.0, 66.0], [97.0, 66.0], [90.0, 66.0], [83.0, 66.0], [78.0, 66.0], [75.0, 66.0], [74.0, 66.0], [74.0, 66.0, 66.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0], [74.0]]

#3D scene reconstruction
MaScene, pts_out = visu_digit_fromcane(csv_file_path, carto, topo, dazi=[90., 30.], dincli=[45., 20.], par_allo=[0.14331, 2.7161, -0.75459], l_petI=12., Hpied=160., MaScene = Scene())
#Monviewer=Viewer
#Monviewer.display(MaScene)


##########
## Caribu at the leaf scale using openalea nodes
##########

from openalea.core.alea import load_package_manager, function
 
pm = load_package_manager()


scene2can = function(pm['alinea.grassland.luzerne']['scene2can'])
FileCaribuScene = function(pm['alinea.caribu']['FileCaribuScene'])
addSoil = function(pm['alinea.caribu']['addSoil'])
Caribu = function(pm['alinea.caribu']['Caribu'])
LIE = function(pm['alinea.caribu']['LIE'])
ViewMapOnCan = function(pm['alinea.caribu.visualisation']['ViewMapOnCan'])
selectOutput = function(pm['alinea.caribu']['selectOutput'])
Plot_CaribuScene = function(pm['alinea.caribu.visualisation']['Plot CaribuScene'])
caribu_leaf = function(pm['alinea.topvine.macro']['caribu_leaf'])
read_meteo_H_splitter_encapsulated = function(pm['alinea.topvine.macro']['read_meteo_H_splitter_encapsulated'])

pattern_file = r'H:\devel\topvine\topvine\data\ex_vine3.8'
opt_file = r'C:\Python26\lib\site-packages\alinea.caribu-6.0.5-py2.6-win32.egg\alinea\caribu_old\data\par.opt'
#light_file = r'C:\Python26\lib\site-packages\alinea.caribu-6.0.5-py2.6-win32.egg\alinea\caribu_old\data\zenith.light'
canfile = scene2can(MaScene ,'bid.can')

meteo_file_path = r'H:\devel\topvine\topvine\data\data_3107_ch1.csv' #meteorological file of the day
HU = 10 #Hour of the day
latitude = 44.#49.7
met, light_file = read_meteo_H_splitter_encapsulated(meteo_file_path, HU, latitude, nb_azi=7, nb_zen=4) #light file construction
#light_file = res[4]




## ! node renvoie toujours tuple, meme si une seule sortie (d'ou [0])
#CaribScene = FileCaribuScene(canfile[0], light_file, pattern_file, opt_file)
#CaribScene = addSoil(CaribScene[0])
#visu = Plot_CaribuScene(CaribScene[0])
#res = Caribu(CaribScene[0], True, {'Nz':5, 'Zmax':2, 'keepFF':False, 'SphereDiameter':0.5})
##CaribScene_out, Energy_Dict, status = Caribu(CaribScene[0], True, {'Nz':5, 'Zmax':2, 'keepFF':False, 'SphereDiameter':0.5})
#LIE_val = LIE(res[0], res[1])
#Eabsm2 = selectOutput(res[1], 'Eabsm2')
#vie = ViewMapOnCan(res[0], Eabsm2[0], 0.15)

phyto_dict, visu = caribu_leaf(canfile[0], light_file, pattern_file, opt_file) #!attention caribu leaf peut planter (le ViewMapOnCan en particulier) si pb de paern et feuille qui disparaissent)

#extraction of a set of leaves corresponding to a shoot
#phyto dict = dictionnaire de la forme {id_caribu:[id_caribu, PARabsm2, Surface]}
#id_caribu vine leaves : sp_opt*10**11+num_phyI*10**6+num_phyII*10**3+num_shoot #id par shoot; ref a plante perdue

numshoot = 5
plant_dict = extract_plant(phyto_dict,numshoot)



## A faire ajouter distance a base du rameau dans le phytodict -> faire une fonction qui fait ca



#

##########
## Calcul de photosynthese par feuille
##########
from copy import deepcopy
path_far = r'H:\devel\topvine\topvine\farquhar'
import sys
sys.path.insert(0, path_far)
from compute_an_bis import *



def Na_Prieto(ageTT, PPFD10, aN=-0.0008, bN=3.3, aM=6.471, bM=56.635):
    """ calcuculation of Na (gN.m-2) from Prieto et al. 2012 - deflaut parameter for Montpellier Experiments """
    # PPFD10 en mol.m-2.day-1
    # TT degree.days
    LMA = aM*log(PPFD10+0.0000000001) + bM
    Nmass = aN*ageTT + bN
    Na = LMA*Nmass/100. #a cause d'erreur d'unite ds le papier
    return max(Na, 0.)
    # petit difference d'arrondi sur aN et bN?


def P25_Na(param,Na):
    """ reponse des parametres photosynthetique (Vcmax,Jmax,TPU,Rd) a l'azote - param[0]: pente; param[1]:ordo origine"""
    return param[0]*Na+param[1]


def par_photo_feuille(Na, Vcmax25_N, Jmax25_N, TPU25_N, Rd25_N, par_photodef=None):
    """ construit liste de par_photosynthese par feuille en fonction de liste de teneurs en azote (Nas) et des reponses a l'azote des parametres Vmax,Jmax/TPU/Rd """
    if par_photodef == None: #pas de fichier parametre fourni en entree
        par_photodef = {}
        par_photodef['Vcm25']= 91.31
        par_photodef['Jm25'] = 168.
        par_photodef['TPU25'] = 12.72
        par_photodef['cdr'] = 1.424
        par_photodef['Kc25'] = 27.239
        par_photodef['Ko25'] = 16.582
        par_photodef['Tx25'] = 3.743

        #reponse a la temperature du alpha (Photochemical efficiency or initial quantum yield) ch Shultz 2003 (suppose constant dans Harley et al. 1992 = 0.24)
        par_photodef['alpha']=  [0.2, 0.2, 0.2, 0.2, 0.2, 0.2]#[0.2, 0.2, 0.19, 0.19, 0.14, 0.12]#[0.2, 0.2, 0.19, 0.19, 0.14, 0.12]
        par_photodef['alpha_T_limit']= [15, 20, 25, 30, 34, 50]
        par_photodef['a1'] = 0.98 # Curvature factor to calculate Jp, usually = 0.98 (Collatz et al 1991)
        par_photodef['a2'] = 0.98 # Curvature factor to calculate Ag, = 0.95 (0.98 for our simulations), Collatz et al 1991
        par_photodef['a3'] = 0.98 # Curvature factor to calculate J; not used in the present version

        par_photodef['RespT_Kc'] = {'model':'Ahrenius', 'c':32.67, 'deltaHa':80.99} # Parameters estimated by Sharkey et al 2007, based on Bernacchi et al 2001 and 2003
        par_photodef['RespT_Ko'] = {'model':'Ahrenius', 'c':9.57, 'deltaHa':23.72} # Parameters estimated by Sharkey et al 2007, based on Bernacchi et al 2001 and 2003
        par_photodef['RespT_Vcm'] = {'model':'Ahrenius', 'c':26.35, 'deltaHa':65.33} # Bernacchi et al 2001 and 2003
        par_photodef['RespT_Jm'] = {'model':'Ahrenius', 'c':17.7, 'deltaHa':43.9} # Bernacchi et al 2001 and 2003
        par_photodef['RespT_TPU'] = {'model':'Ahrenius', 'c':21.46, 'deltaHa':53.1} # Bernacchi et al 2001 and 2003
        par_photodef['RespT_Rd'] = {'model':'Ahrenius', 'c':18.72, 'deltaHa':46.39} # Bernacchi et al 2001 and 2003
        par_photodef['RespT_Tx'] = {'model':'Ahrenius', 'c':9.87, 'deltaHa':24.46} # Parameteres estimated by Sharkey et al 2007
        ## to update with parameters for grapevine

    #ls_par_photo = []
    #for Na in Nas:
    #    p = deepcopy(par_photodef)
    #    p['Vcm25'] = P25_Na(Vcmax25_N, Na)
    #    p['Jm25'] = P25_Na(Jmax25_N, Na)
    #    p['TPU25'] = P25_Na(TPU25_N, Na)
    #    p['cdr'] = P25_Na(Rd25_N, Na)
    #    ls_par_photo.append(p)
    p = deepcopy(par_photodef)
    p['Vcm25'] = P25_Na(Vcmax25_N, Na)
    p['Jm25'] = P25_Na(Jmax25_N, Na)
    p['TPU25'] = P25_Na(TPU25_N, Na)
    p['cdr'] = P25_Na(Rd25_N, Na)

    return p#ls_par_photo

def delta_tempAirFeuilHU(HU, PPFD):
    """ Relations empirique delta temp air-feuille de Prieto en fonction du PPFD (These annexe 2)"""
    if HU<=10.:
        p = [0.00144, -0.972979]
    elif HU<=11.:
        p = [0.00149, -0.810811]
    elif HU<=12.:
        p = [0.00149, -1.02703]
    elif HU<=13.:
        p = [0.00159, -1.45946]
    elif HU<=14.:
        p = [0.00244, -1.45946]
    elif HU<=15.:
        p = [0.00161, -1.45946]
    elif HU<=16.:
        p = [0.00113, -1.10541]
    elif HU<=17.:
        p = [0.00134, -1.20805]
    else:
        p = [0.00110, -1.11553]
    
    return  p[1] + p[0]*PPFD
    #delta_tempAirFeuilHU(HU=12, PPFD=array([2000.,1000.,100.,10.]))


#nouveau formet du par_photo
par_photo1 = {}
par_photo1['Vcm25']= 91.31
par_photo1['Jm25'] = 168.
par_photo1['TPU25'] = 12.72
par_photo1['cdr'] = 1.424
par_photo1['Kc25'] = 27.239
par_photo1['Ko25'] = 16.582
par_photo1['Tx25'] = 3.743

#reponse a la temperature du alpha (Photochemical efficiency or initial quantum yield) ch Shultz 2003 (suppose constant dans Harley et al. 1992 = 0.24)
par_photo1['alpha']=  [0.2, 0.2, 0.19, 0.19, 0.14, 0.12]#[0.2, 0.2, 0.2, 0.2, 0.2, 0.2]#[0.2, 0.2, 0.19, 0.19, 0.14, 0.12]#
par_photo1['alpha_T_limit']= [15, 20, 25, 30, 34, 50]
par_photo1['a1'] = 0.98 # Curvature factor to calculate Jp, usually = 0.98 (Collatz et al 1991)
par_photo1['a2'] = 0.98 # Curvature factor to calculate Ag, = 0.95 (0.98 for our simulations), Collatz et al 1991
par_photo1['a3'] = 0.98 # Curvature factor to calculate J; not used in the present version

par_photo1['RespT_Kc'] = {'model':'Ahrenius', 'c':32.67, 'deltaHa':80.99} # Parameters estimated by Sharkey et al 2007, based on Bernacchi et al 2001 and 2003
par_photo1['RespT_Ko'] = {'model':'Ahrenius', 'c':9.57, 'deltaHa':23.72} # Parameters estimated by Sharkey et al 2007, based on Bernacchi et al 2001 and 2003
par_photo1['RespT_Vcm'] = {'model':'Ahrenius', 'c':26.35, 'deltaHa':65.33} # Bernacchi et al 2001 and 2003
par_photo1['RespT_Jm'] = {'model':'Ahrenius', 'c':17.71, 'deltaHa':43.9} # Bernacchi et al 2001 and 2003
par_photo1['RespT_TPU'] = {'model':'Ahrenius', 'c':21.46, 'deltaHa':53.1} # Bernacchi et al 2001 and 2003
par_photo1['RespT_Rd'] = {'model':'Ahrenius', 'c':18.72, 'deltaHa':46.39} # Bernacchi et al 2001 and 2003
par_photo1['RespT_Tx'] = {'model':'Ahrenius', 'c':9.87, 'deltaHa':24.46} # Parameteres estimated by Sharkey et al 2007


## parametres gs
par_gs = {} 
par_gs['model'] = 'BWB_gs'
par_gs['g0'] = None #a garder et rendre actif
par_gs['m'] = None #a remplacer par a1 et D0 de Leuning
#pour le moment parametres gs en dur dans BWB_gs


## meteo
#meteo_dat = met#{'psi': 0.1, 'Pa': 101.3, 'DOY': 176.0, 'hs': 36.0, 'Ca': 360.0, 'HU': 12.0, 'PPFD': 2000., 'Rg': 933.3, 'u': 2.22, 'Tac': 25.5}


## test de An
#An, Cinew, gs, gb, Tlc, E, Rd, id_lim, lsWx, Tx = coupling_Angsci(par_photo1, par_gs, meteo_dat, lat=0.44, alt=0.,LPI=10., alb=0.2, w=0.1, iter=50, delta_Tc=0.1, deltaci=0.0001, Tlc=meteo_dat['Tac'])


#Exemple 1: calcul de An pour chaque feuille de plant_dict (1 rameau)
id_leaves = plant_dict.keys()

res = []
for leaf in id_leaves:
    PPFD_leaf = plant_dict[leaf][1]*2.2*1000000./3600.
    meteo_leaf = deepcopy(met)
    meteo_leaf['PPFD'] = PPFD_leaf
    meteo_leaf['Rg'] = PPFD_leaf/2.2
    dTleaf = delta_tempAirFeuilHU(meteo_leaf['HU'], meteo_leaf['PPFD'])
    An, Cinew, gs, gb, Tlc, E, Rd, id_lim, lsWx, Tx = coupling_Angsci(par_photo1, par_gs, meteo_leaf, latitude, alt=0.,LPI=10., alb=0.2, w=0.1, iter=50, delta_Tc=0.1, deltaci=0.0001, Tlc=met['Tac']+dTleaf)
    res.append(An)
    plant_dict[leaf] = plant_dict[leaf]+[meteo_leaf['DOY'], meteo_leaf['HU'], An, Cinew, gs, Tlc, E, Rd] #add the values to plant dict
   

res



#Exemple 2: calcul de An pour une feuille dont on calcule Na a partir de PPFD10 et ageTT
## parametres pour teneur en azote Prieto et al. 2012
Vcmax25_N = [34.02, -3.13]
Jmax25_N = [78.27, -17.3]
TPU25_N = [6.24, -1.92]
Rd25_N = [0.42, -0.01] #parametrage Rd doivent etre en positif!

ageTT = 1000.
PPFD10 = 20.
Na = Na_Prieto(ageTT, PPFD10, aN=-0.0008, bN=3.3, aM=6.471, bM=56.635)
par_photo_leaf = par_photo_feuille(Na, Vcmax25_N, Jmax25_N, TPU25_N, Rd25_N, par_photodef=par_photo1)
An, Cinew, gs, gb, Tlc, E, Rd, id_lim, lsWx, Tx = coupling_Angsci(par_photo_leaf, par_gs, met, latitude, alt=0.,LPI=10., alb=0.2, w=0.1, iter=50, delta_Tc=0.1, deltaci=0.0001, Tlc=met['Tac'])




## A faire: virer LPI et remplacer par age en TT
