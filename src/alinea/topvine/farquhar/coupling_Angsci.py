from meteo_utils import *
from compute_gs import *
from compute_an import *
from coupling_Anci import *


def Transpiration_rate(Tac, Tlc, ea, gs, gb, Pa = 101.3, epsilon = 0.97):
    ## Declaration des constantes
    #lambda_ = 44.0 # latent heat of vaporization at 25degreC (kJmol-1)
    sigma = 0.0000000567 # Stefan-Boltzmann constant per surface area (W m-2 K-4)
    Cp = 29.3 # specific heat of air (J mol-1 degreC-1)

    #**********************************************************
    #calculation of leaf temperature
    #**********************************************************
    gva = gb*1.4 # boundary layer conductance for water transport (mol m2 s-1) COMENTARIO 6/6/2011: se saca la formula 1.4 *gb para el calculo de pl entera
    gv = 1/((2/gva)+(1/gs)) # Formulation by Pearcy 1989, used for simulations

    # gv = (0.5*(gs*gva)/(gs+gva))  # total water vapour conductance per surface leaf area; THIS Formulation IS NOT TOTALLY RIGHT
    gha = (1.4*0.135*gb/0.147)  # boundary layer conductance for heat (mol m2 s-1)
    gr = (4*epsilon*sigma*(Tlc+273)**3)/Cp # radiative conductance (mol m2 s-1)
    ghr = gha+gr # convective radiative conductance (mol m2 s-1)
    es_l = 0.611*exp((17.27*Tlc)/(237.3+Tlc))  # saturated vapor pressure at leaf surface (kPa) and LEAF TEMPERATURE. Original: s_avpd(Tlc)
    es_a = s_avpd(Tac)#0.611*exp(17.27*Tac/(237.3+Tac))  # saturated vapor pressure in the ambiant air (kPa)
    #Y = (ghr/gv)*0.000666  # psychrometer constante (degreC-1)
    
    E = gv*((es_l-ea)/Pa) # Transpiration rate (mol m-2 s-1) 
    return E

def increment_leafT(Tac, Tlc, ea, Rabs, gs, gb, Pa = 101.3, epsilon = 0.97):
    """ % Calcul LeafTemperature=f(Tac, Tlc, ea, Rabs, gs, gb, Pa = 101.3, epsilon = 0.97)
    % Hypothese a modifier : hs=ha
    epsilon  : leaf thermal emissivity
    Pa : atmospheric pressure kPa  """

    ## Declaration des constantes
    lambda_ = 44.0 # latent heat of vaporization at 25degreC (kJmol-1)
    sigma = 0.0000000567 # Stefan-Boltzmann constant per surface area (W m-2 K-4)
    Cp = 29.3 # specific heat of air (J mol-1 degreC-1)

    #**********************************************************
    #calculation of leaf temperature
    #**********************************************************
    gva = 1.4*gb # boundary layer conductance for water transport (mol m2 s-1)
    gv = (0.5*(gs*gva)/(gs+gva))  # total water vapour conductance per surface leaf area
    gha = (1.4*0.135*gb/0.147)  # boundary layer conductance for heat (mol m2 s-1)
    gr = (4*epsilon*sigma*(Tlc+273)**3)/Cp # radiative conductance (mol m2 s-1)
    ghr = gha+gr # convective radiative conductance (mol m2 s-1)
    es_l = s_avpd(Tlc) #0.611*exp((17.27*Tlc)/(237.3+Tlc))  # saturated vapor pressure at leaf surface (kPa)
    es_a = s_avpd(Tac) #0.611*exp(17.27*Tac/(237.3+Tac))  # saturated vapor pressure in the ambiant air (kPa)
    Y = (ghr/gv)*0.000666  # psychrometer constante (degreC-1)
    E = 2*gv*((es_l-ea)/Pa) # Transpiration rate (mol m-2 s-1)
    delta = (4098*ea)/(Tac+237.3)**2 # slope of vapor pressure curve (kPa degre K-1)
    hs=(ea/es_a)*100  # Relative humidity
    D = es_a-ea # vapor pressure deficit (kPa)
    Tlcnew = Tac+(Y/(delta/Pa+Y)*(((Rabs-epsilon*sigma*(Tac+273)**4)/((ghr*Cp))-(D/(Pa*Y))))) # leaf temperature degreC
    Tlc=Tlcnew

    return Tlcnew,E
    #increment_leafT(25., 25., 2.5, 600, 0.3, 1.2)


def coupling_Angsci(par_photo, par_gs, meteo_dat, lat=0.44, alt=0.,LPI=10., alb=0.2, w=0.1, iter=50, delta_Tc=0.1, deltaci=0.0001, Tlc=None):
    '''    compute farquar model coupling An gs and leaf temperature
    '''

    Tac = meteo_dat['Tac'] 
    PPFD = meteo_dat['PPFD'] 
    Rg = meteo_dat['Rg'] 
    hs = meteo_dat['hs'] 
    psi = meteo_dat['psi'] 
    u = meteo_dat['u'] 
    Ca = meteo_dat['Ca'] 
    Pa = meteo_dat['Pa']
    Vcm25 = par_photo['Vcm25']
    Jm25 = par_photo['Jm25']
    cdr = par_photo['cdr']
    
    es_a = s_avpd(Tac) #% saturated vapor pressure in the ambiant air (kPa)#saturated vapor pressure in the ambiant air (kPa)
    ea = es_a*hs/100 #% vapor pressure in the ambiant air (kPa)
    D = es_a-ea #% Vapor pressure deficit at air temperature (Kpa)

    ## initialisation Tlc, ci
    if Tlc == None or type(Tlc)==type('a'):
        Tlc = Tac
        tlc_input = 0
    else:
        tlc_input = 1

    Ci = 0.7*Ca #% CO2 substomatal concentration (pa)

    ## optimisation loop : Ci et Tlc
    j=1
    while j<iter:#loop Tlc
        # Ci loop
        An, Cinew, gs, gb = coupling_Anci(par_photo, par_gs, meteo_dat, LPI, w, iter, deltaci, Tlc)

        if tlc_input == 1: #temperature de feuille fournie
            E = Transpiration_rate(Tac, Tlc, ea, gs, gb, Pa = 101.3, epsilon = 0.97)
            break
        else:
            # leaf temperature calculation loop
            Rabs = computeRabs(Rg, Tac, meteo_dat['DOY'], meteo_dat['HU'], lat, alt, alb)#% absorbed radiation short wave radiations (W m-2)
            Tlcnew, E = increment_leafT(Tac, Tlc, ea, Rabs, gs, gb) 
            print Rabs, Tlcnew
            if  abs(Tlcnew-Tlc) < delta_Tc :
                Tlc = Tlcnew
                print 'nb iteration Tl_'+str(j)
                break #% to the end of Tlc loop
            else :
                Tlc = Tlcnew
                Ci = 0.7*Ca # reinitialisation of Ci
                print 'nb iteration Tl_'+str(j)       
            
            if j>iter-2:
                print 'warning !!! Tlc calculation does not converge to a solution' 
           
        j=j+1  

    return An, Cinew, gs, gb, Tlc, E, Vcm25, Jm25, cdr

