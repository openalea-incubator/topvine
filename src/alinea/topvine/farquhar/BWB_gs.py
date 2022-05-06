from __future__ import absolute_import
from numpy import exp
from .meteo_utils import *

def BWB_m(psi, m0=129.30000000000001, psi0=0.37, n_gs=1.85):
    '''    compute BWB m parameter according to soil water status
    '''
    """psi : predawn leaf water potential (-MPa)
    parameter for stomatal conductance to water vapor calculation(mmol H2O m-2 s-1) after Nikolov (1995) :
    m0_gs, psi0_gs, n_gs  """


    return m0/(1.+(psi/psi0)**n_gs)

def BWB_g0(psi, psi0=0.34999999999999998, m0=41.700000000000003, n_cut=1.1799999999999999):
    '''    compute cuticular conductance according to soil water status
    '''
    """psi : predawn leaf water potential (-MPa)
    parameter for residual cuticular conductance to water vapor calculation(mmol H2O m-2 s-1) after Nikolov (1995) :
    m0_cut, psi0_cut, n_cut
     """

    return m0/(1.+(psi/psi0)**n_cut)

def BWB_gs(An, ea, Tac, Ca, gb, m=118.69, g0=15.23, Pa = 101.3):
    '''    Ball Woodrow & Berry stomatal conductance model
    '''
    """ compute stomatal conductance = f(An, ea, Tac, Ca, gb, psi) after ball and Berry (1987)
    An : net photosynthesis  (micromol m2 s-1)
    ea : vapor pressure in the ambiant air (kPa)
    Tac : air temperature (degre celsius)
    Ca : CO2 atmospheric concentration (pa)
    gb : boundary layer conductance (mol m2 s-1) """

    R = 0.00831 # Constante des gaz parfaits kJ K-1
    T = 3.743*((exp(9.87-(24.46 /(R*(Tac+273.15)))))) # point de compensation de CO2
    es_a = s_avpd(Tac) #% saturated vapor pressure in the ambiant air (kPa)#saturated vapor pressure in the ambiant air (kPa)
    hs = HR(ea, es_a)  # Relative humidity (pourcent)
    Cs = Ca-An*(1.37/gb) # CO2 concentration at the leaf surface, Kim and Lieth 2003
    ##Cs = Ca*Pa*0.001-An*(1.37/gb) # CO2 concentration at the leaf surface, Kim and Lieth 2003   #en Pa, pour lecture en ppm de Ca
    VPD= VPDa(Tac, hs) #Used for Leuning (03-2011)
    gs = (0.02 + ((12.5*An)/((1+(VPD/2.86))*(Cs-10*T)))) # Leuning (1995)  #luzerne
    if gs<0.02:
        gs = 0.02    

    ##gs = (0.017 + ((5.278*An)/((1+(VPD/30))*(Cs-T)))) # Leuning (1995)  #Vigne Prieto avec bug Ca lu en ppm
    ##if gs<0.017:
    ##    gs = 0.017    
    # gs = (g0+m*An*hs/Cs)/1000.  # BWB model, stomatal conductance for water transport (mol m2 s-1) Attention, Ca a remplacer par Cs!
    # if gs<g0/1000.:
    #   gs=g0/1000.

    return gs
    #BWB_gs(15.0,2.,25.,360.)
    #avec deficit hydrique
    #psi=0.1
    #BWB_gs(15.0,2.,30.,360., BWB_m(psi), BWB_g0(psi))

