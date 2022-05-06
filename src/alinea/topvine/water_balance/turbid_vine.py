from __future__ import absolute_import
from __future__ import print_function
from openalea.plantgl.all import *
from numpy import sqrt, arccos, array, cos, sin, pi, ceil, exp
import random

#path_ = r'H:\devel\grassland\grassland\luzerne'
#import sys
#sys.path.insert(0, path_)
import os
#from os.path import join
from openalea.core.pkgmanager import PackageManager
from six.moves import range
pm = PackageManager()
pkg = pm.get('alinea.topvine') 
path_topvine = ''
if pkg :
    path_topvine = pkg.path

import sys
sys.path.insert(0, path_topvine)

from Obj3Dutils import *


#feuille carre de dim 1
fc = quadform([-0.5,0.,0.], [-0.5,1.,0.], [0.5,1.,0.], [0.5,0.,0.])

def luz_label(sp_opt, num_phyI, num_shoot, num_plant, num_phyII=0):
    num_phy = num_phyI*10**2 + num_phyII
    lab = str(int(sp_opt*10**11+num_phy*10**6+num_shoot*10**3+num_plant))
    return (12-len(lab))*'0'+lab

def turbid_vineVSP(TT, LADini, LAImax, Hmax, Largmax,  Hpied, dazi=[0., 60.], dincli=[45., 0.], dsize = 0.001, seed=0):
    fsized = transformation(fc, sqrt(dsize),sqrt(dsize),sqrt(dsize),0,0,0,0,0,0)
    
    #LAI = min(TT/500.*LAImax, LAImax)
    b, c = 445, 110
    LAI = LAImax/(1+exp(-(TT-b)/c))
    surf = LAI*1.8#interrang recalcule a partir du pattern
    dH = Hmax-Hpied
    larg_calc = sqrt(surf/(LADini*dH/Largmax))
    larg = min(larg_calc, Largmax)
    H = dH*larg/Largmax
    vol = larg*H
    LAD = surf/vol

    #vol =Hmax*Largmax*1
    #surf = LADini*vol
    n1 = surf/dsize
    sd = random.seed(seed)
    print(LAI, LAD, surf, n1, larg, H, larg_calc, 'LAI, LAD, surf, n1, larg, H, larg_calc')

    MaScene = Scene()
    for i in range (int(n1)):
        x,y = random.uniform(-0.5, 0.5), random.uniform(-larg/2., larg/2.) 
        z = random.uniform(Hpied, Hpied+H)

        if y>0:
            azi = random.gauss(dazi[0], dazi[1])
        else:
            azi = random.gauss(dazi[0]+180., dazi[1])

        lf = transformation(fsized, 1,1,1,azi*pi/180.,random.gauss(dincli[0], dincli[1])*pi/180.,0,x,y,z)
        id1 = luz_label(1, 0, 0, 1, 0)#luz_label(1, i, 0, 1, 0)
        lf.setName(id1)
        MaScene.add(Shape(lf, Material(Color3(44,195,48))))

    #tronc
    en = Cylinder(1,1,True,6)
    tc = transformation(en, 0.035,0.035,Hpied,0.,0.,0,0,0,0)
    id1 = luz_label(1, 0, 0, 1, 0)#luz_label(1, i, 0, 1, 0)
    tc.setName(id1)
    MaScene.add(Shape(tc, Material(Color3(202,106,27))))

    return MaScene

#Monviewer=Viewer
#MaScene = turbid_vineVSP(350., 4., 2., 1.9, 0.3, 0.5, dazi=[90., 0.], dincli=[45., 0.], dsize = 0.001, seed=0)
#Monviewer.display(MaScene)

def turbid_vineCyl(TT, LADini, LAImax, Hmax, Hpied, ouverture=270., dazi=[0., 60.], dincli=[45., 0.], dsize = 0.001, seed=0):
    fsized = transformation(fc, sqrt(dsize),sqrt(dsize),sqrt(dsize),0,0,0,0,0,0)
    
    #LAI = min(TT/500.*LAImax, LAImax)
    b, c = 445, 110
    LAI = LAImax/(1+exp(-(TT-b)/c))
    surf = LAI*1.8#interrang recalcule a partir du pattern
    rmax = Hmax-Hpied
    r_calc = sqrt(surf/(LADini*pi*ouverture/360.))
    r = min(r_calc, rmax)
    vol = pi*r*r*ouverture/360.
    LAD = surf/vol
    n1 = surf/dsize
    sd = random.seed(seed)
    print(LAI, LAD, surf, n1, r, r_calc, 'LAI, LAD, surf, n1, larg, H, larg_calc')

    MaScene = Scene()
    for i in range (int(n1)):
        x = random.uniform(-0.5, 0.5)  
        ry, teta = random.uniform(0., r), random.uniform(-ouverture*pi/360.+pi/2, ouverture*pi/(360.)+pi/2)
        y,z = cos(teta)*ry, sin(teta)*ry+Hpied

        if y>0:
            azi = random.gauss(dazi[0], dazi[1])
        else:
            azi = random.gauss(dazi[0]+180., dazi[1])

        lf = transformation(fsized, 1,1,1,azi*pi/180.,random.gauss(dincli[0], dincli[1])*pi/180.,0,x,y,z)
        id1 = luz_label(1, 0, 0, 1, 0)#luz_label(1, i, 0, 1, 0)
        lf.setName(id1)
        MaScene.add(Shape(lf, Material(Color3(44,195,48))))

    #tronc
    en = Cylinder(1,1,True,6)
    tc = transformation(en, 0.035,0.035,Hpied,0.,0.,0,0,0,0)
    id1 = luz_label(1, 0, 0, 1, 0)#luz_label(1, i, 0, 1, 0)
    tc.setName(id1)
    MaScene.add(Shape(tc, Material(Color3(202,106,27))))

    return MaScene

#Monviewer=Viewer
#MaScene = turbid_vineCyl(350., 4., 2., 1.5, 0.5, ouverture=270., dazi=[90., 0.], dincli=[45., 0.], dsize = 0.001, seed=0)
#Monviewer.display(MaScene)
