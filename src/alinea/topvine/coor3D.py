### set de fonctions utiles pour manipuler les coordonnees 3D dans l'espace

from __future__ import absolute_import
from __future__ import print_function
import numpy

def XyzToPol (coordxy) :
    """ converti les coordonnees carthesiennes d'un point (x,y,z) en coordonnees polaires (r,azi,incli)"""
    x,y,z = coordxy[0], coordxy[1], coordxy[2]
    r = numpy.sqrt(x*x+y*y+z*z)
    if r==0 :
        incli =0
    else :
        incli = numpy.arcsin(z/r)
    if (x==0 and y==0):
        azi = 0
    elif (y>=0) :
        azi = numpy.arccos(x/numpy.sqrt(x*x+y*y))
    else :
        azi = -numpy.arccos(x/numpy.sqrt(x*x+y*y))
    return numpy.array([r,azi,incli])


def PolToXyz (coordpol) :
    """ converti les coordonnees polaires (r,azi,incli) d'un point en coordonnees carthesiennes(x,y,z)"""
    r,azi,incli = coordpol[0], coordpol[1], coordpol[2]
    z = r * numpy.sin(incli)
    l = numpy.sqrt (r*r-z*z)
    x = l * numpy.cos(azi)
    y = l * numpy.sin (azi)
    return numpy.array([x, y, z])

def RotateAxis (coordxy, r_azi, r_incli):
    """ calcule les nouvelles coord d'un point apres rotation autour des axes y (r_incli en radians) et z (r_azi en radians)"""
    #incli d'abord = rotation autour de y
    Pol_ini = XyzToPol (numpy.array([coordxy[0], coordxy[2], -coordxy[1]]))
    xyz_r = PolToXyz (numpy.array([Pol_ini[0],Pol_ini[1]+r_incli,Pol_ini[2]]))
    #azi ensuite = rotation autour de z
    Pol_sec = XyzToPol (numpy.array([xyz_r[0],-xyz_r[2],xyz_r[1]]))
    xyz_r2 = PolToXyz (numpy.array([Pol_sec[0],Pol_sec[1]+r_azi,Pol_sec[2]]))
    return xyz_r2

def Translate (coordxy, t):
    """ calcule les nouvelles coord d'un point apres trnaslation de t """
    if len(coordxy)==len(t):
        return coordxy + t
    else:
        print('vector lengths do not match')

## test
#c=numpy.array([1.2,1,0.9])
#XyzToPol (c)
#PolToXyz (XyzToPol (c))
#RotateAxis (c, numpy.pi, numpy.pi)
#Translate (c, numpy.array([1.,1.,1.]))

