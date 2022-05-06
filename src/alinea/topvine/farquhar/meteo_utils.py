from __future__ import absolute_import
from math import *
from numpy import exp

def s_avpd(Tac):
    """ saturated vapor pressure in the ambiant air (kPa)"""
    return 0.611*exp(17.27*Tac/(237.3+Tac))
 
def HR(ea, es_a):
    """  compute Relative humidity (pourcent)"""
    return (ea/es_a)*100.

def VPDa(Tac, hs):
    """ compute air  Vapor pressure deficit at air temperature"""
    es_a = s_avpd(Tac) #% saturated vapor pressure in the ambiant air (kPa)#saturated vapor pressure in the ambiant air (kPa)
    ea = es_a*hs/100 #% vapor pressure in the ambiant air (kPa)
    return es_a-ea #% Vapor pressure deficit at air temperature (Kpa)

def DecliSun (DOY):
    """ Declinaison (rad) du soleil en fonction du jour de l'annee """
    alpha=2*3.14*(DOY-1)/365
    return (0.006918-0.399912*cos(alpha)+0.070257*sin(alpha))

def extra (DOY,HU,latitude):
    """ rayonnement extraterrestre horarire """
    hrad=2*3.14/24*(HU-12)
    lat=radians(latitude)
    dec=DecliSun (DOY)
    costheta=sin(lat)*sin(dec)+cos(lat)*cos(dec)*cos(hrad)
    Io=1370*(1+0.033*cos(2*3.14*(DOY-4)/366))#eclairement (w/m2) a la limitte de l'atmosphere dans un plan perpendiculaire aux rayons du soleil, fonction du jour
    So=Io*costheta #eclairement dans un plan parallele a la surface du sol
    return So
    #extra (100,11,44)

def Rs0(Ra, z):
    """ compute clear sky global radiation according to extraterestrial radiation and altitude (m)
    eq 37 - FA056, p 51"""
    return Ra*(3600./1e6)*(0.75 + 2e-5*z) #formule pour Ra en MJ.m-2.h-1
    #Rs0(extra (100,11,44),10.)


def computeLongwaveNetRadiation(Tac, Rs, Rs0):
    """ compute LongwaveNetRadiation = f(Tk_a,Tac_x, ea, Rs,Rs0) after FA0 56 eq #(39)
    Tak  : absolute air temperature (K)
    es_a : saturated vapor pressure in the ambiant air (kPa)
    Rs : measured solar radiation (MJ m2 hour)
    Rs0 : calculated clear-sky solar radiation (MJ m2 hour)"""

    ## Declaration des constantes
    sigma = 2.0412*1e-10 # Stefan-Boltzmann constant per surface area (MJ m-2 K-4 H-1)

    ## Compute longwave net radiation
    es_a = s_avpd(Tac) #% saturated vapor pressure in the ambiant air (kPa)
    Tak = Tac+273.16
    ratio = min(1., Rs/Rs0)
    Rnl= sigma*(Tak**4)*(0.34-0.14*(es_a**0.5))*(1.35*ratio-0.35)
    return Rnl*1e6/3600. #(en w.m-2)
    #computeLongwaveNetRadiation(25., 600.*3600./1e6, Rs0(extra (100,11,44),10.))

def computeRabs(Rg, Tac, DOY, HU, latitude = 0.44, altitude = 0., albedo=0.2):
    """ """
    Rextra = extra (DOY,HU,latitude)
    Rs0_ = Rs0(Rextra, altitude)
    Rnl = computeLongwaveNetRadiation(Tac, Rg*3600./1e6, Rs0_)
    Rabs=Rg*(1-albedo)-Rnl

    return Rabs
    #computeRabs(600., 25., 100, 11)


def computeBoundaryLayerConductance(u, w=0.1):
    """ compute Boundary layer conductance = f(u, w) after Kim and Lieth (2003)
    u : wind speed m s-1
    w : leaf Characteristic dimension in relation to wind speed (m)"""

    d = 0.72*w # leaf dimension (m)
    gb = 0.147*(u/d)**0.5  # boundary layer conductance (mol m2 s-1)
    # gb = 3.33 #  pour les simulations a niveau de feuille, il faut introduire la valeur de gb du LcPro (rb =0.33 mol m-2 s-1)
    return gb
    #computeBoundaryLayerConductance(2.)
