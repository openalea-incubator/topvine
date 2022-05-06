####
# G Louarn 26/07/2014
# version reecrite de compute_an de Prieto et al. 2012 pour sortir les parametres de reponse a la temperature
# changement des entrees (par_photo) et ajout de sorties (Wx notamment)

from numpy import *
#from numpy import exp
from meteo_utils import *
from compute_gs import *


################
## ancien Compute_An

def RespT_Ahrenius (Tlk, c, deltaHa): 
    """ cf Harley et al. 1992"""
    R = 0.0083143 # Constante des gaz parfaits kJ K-1
    return exp(c-(deltaHa /(R*Tlk)))

def RespT_Johnson (Tlk, c, deltaHa, deltaS, deltaHd):
    """ cf Harley et al. 1992"""
    R = 0.0083143 # Constante des gaz parfaits kJ K-1
    return exp(c-(deltaHa /(R*Tlk))) / (1 + exp((deltaS*Tlk - deltaHd)/(R*Tlk)))
    #rq: Evers et al. proposent une forme legerement differente ou un terme de devactivation a 25 apparait (p6 appendice)

def RespT_beta(Tlc, Tmin, Tmax, Topt):
    """ Yan et hunt 1999 """
    #return ((Tmax-Tlc)/(Tmax-Topt)) * ((Tlc-Tmin)/(Topt-Tmin))**((Topt-Tmin)/(Tmax-Topt)) #Marie
    return ((Tlc-Tmin)/(Topt-Tmin)) * ((Tmax-Tlc)/(Tmax-Topt))**((Tmax-Topt)/(Topt-Tmin))



def RespT (Tlk, paramRespT):
    """ fonction pour gerer choix de courbe de reponse a Temperature """
    if paramRespT['model'] == 'Ahrenius':
        RespT = RespT_Ahrenius (Tlk, paramRespT['c'], paramRespT['deltaHa'])
    elif paramRespT['model'] == 'Johnson':
        RespT = RespT_Johnson (Tlk, paramRespT['c'], paramRespT['deltaHa'], paramRespT['deltaS'], paramRespT['deltaHd'])

    return RespT

#RespT (20.+273.15, {'model':'Ahrenius', 'c':26.35, 'deltaHa':65.33})
#RespT (20.+273.15, {'model':'Johnson', 'c':26.35, 'deltaHa':65.33, 'deltaS':0.635, 'deltaHd':200.})


def Wc (Vcmax, Ci, O, T, Kc, Ko):
    # limitation par la quantite, l'etat d'activation ou les proprietes cinetiques de la Rubisco(Eq (2) Schultz 2003)
    # The Ci values must be expressed in Pa, so multiplied by 0.1
    Wc_ = (Vcmax*(Ci*0.1013-T))/((Ci*0.1013)+Kc*(1+O/Ko)) 
    return Wc_

def Wj (Jmax, alpha, PPFD, Ci, T):
    # limitation par le taux de regeneration de RuBP lie au taux de transfert des electrons au travers du PSII (Eq (3) Schultz 2003)
    # The Ci values must be expressed in Pa, so multiplied by 0.1
    J = (alpha*PPFD)/((1+((alpha**2*PPFD**2)/(Jmax**2)))**0.5)
    return (J*(Ci*0.1013-T))/(4*((Ci*0.1013)+2.*T))

def Wp (TPU, Ci, T):
    # limitation par triose phosphate - Sharkey 2007
    # The Ci values must be expressed in Pa, so multiplied by 0.1
    return (TPU*3) / (1-T/(Ci*0.1013)) #! dans version anterieure oubli du terme de division!



def compute_an(par_photo, PPFD, Tlc, Ci, LPI=None):
    '''    compute photosynthesis according to farquhar model
    '''
    """ Fonction which computePhotosynthesis - Farquhar model for grapevine from Schultz FPB 2003 & Nikolov 1995
    """
    # rq: pas besoin de par_gs: donne 1 Ci!

    ##constantes
    O = 21. # pression partielle en oxygene kPa
    R = 0.0083143 # Constante des gaz parfaits kJ K-1

    ## Conversion temperature degreC -> degreK 
    Tlk = Tlc + 273.15

    ## determination of alpha
    a1 = par_photo['a1']        # Curvature factor to calculate Jp, usually = 0.98 (Collatz et al 1991)
    a2 = par_photo['a2']        # Curvature factor to calculate Ag, = 0.95 (0.98 for our simulations), Collatz et al 1991
    a3 = par_photo['a3']        # Curvature factor to calculate J; not used in the present version
    alpha = par_photo['alpha'][0]
    for i in range(1,len(par_photo['alpha'])):
        if par_photo['alpha_T_limit'][i-1]< Tlc < par_photo['alpha_T_limit'][i]:
            alpha = par_photo['alpha'][i]
    
    ## Temperature effects
    Kc = par_photo['Kc25'] * RespT (Tlk, par_photo['RespT_Kc']) # Parameters estimated by Sharkey et al 2007, based on Bernacchi et al 2001 and 2003
    Ko = par_photo['Ko25'] * RespT (Tlk, par_photo['RespT_Ko'])
    
    Vcmax = par_photo['Vcm25'] * RespT (Tlk, par_photo['RespT_Vcm']) # Taux de carboxylation maximal en fonction de la temperature de la feuille
    Jmax = par_photo['Jm25'] * RespT (Tlk, par_photo['RespT_Jm'])   # Flux maximal d'electrons en fonction de la temperature de la feuille
    TPU = par_photo['TPU25'] * RespT (Tlk, par_photo['RespT_TPU'])    # ajoute le 15/11 selon sharkey 07

    # cdr is the dark respiration at 25dC, it can be calculated through the Na relationship or directly introduced in "Param_Photo"   
    Rd = par_photo['cdr'] * RespT (Tlk, par_photo['RespT_Rd'])# Parameteres estimated by Bernacchi (2001) and Sharkey et al 2007, must add Na relationship
    T = par_photo['Tx25'] * RespT (Tlk, par_photo['RespT_Tx'])# Parameteres estimated by Sharkey et al 2007

    ##Calculation of net photosynthesis
    Wc_ = Wc (Vcmax, Ci, O, T, Kc, Ko)
    Wj_ = Wj (Jmax, alpha, PPFD, Ci, T)
    Wp_ = Wp (TPU, Ci, T)

    # Classical solution:
    lsW = [Wc_, Wj_, Wp_]
    Vc = min(lsW) # Taux de carboxylation - #rq: Wp de shultz bug - prends formule de Nikolov, amis qui est un peu "raide" selon eric
    id_lim = lsW.index(Vc) #pour savoir lequel est limitant (0: WC, 1, Wj, 2: Wp)
    An = Vc*(1-T/(Ci*0.1013))-Rd 

    return An, Rd, id_lim, lsW, T#An


def compute_Rd(par_photo, Tlc):
    Tlk = Tlc + 273.15  ## Conversion temperature degreC -> degreK
    Rd = par_photo['cdr'] * RespT (Tlk, par_photo['RespT_Rd'])
    return Rd  #An + Rd = photosynthese brute

def computeAn_Wx( lsW, Ci, Rd, Tx):
    """ recalcul des An par Wx"""
    Wc_, Wj_, Wp_ = lsW[0], lsW[1], lsW[2]
    AnWc = Wc_*(1-Tx/(Ci*0.1013))-Rd
    AnWj = Wj_*(1-Tx/(Ci*0.1013))-Rd
    AnWp = Wp_*(1-Tx/(Ci*0.1013))-Rd
    return AnWc, AnWj, AnWp


################
## ancien Compute_AnCi

def incrementCi(Ca, A, gs, gb): # 22/06/2011: sacar el meteo_dat, ea, es_l del parentesis y del parentesis de la linea 44
    '''    increment Ci Value
    '''
    # Tac = meteo_dat['Tac']
    # Pa = meteo_dat['Pa']
    # hs = meteo_dat['hs']
    # This formulation can be used to account for the effect of H2O transpired in the Ci concentration inside the chamber
    # gva = gb *1.4 # todo esto es nuevo; atencion (22/06/2011)
    # gv = (0.5*(gs*gva)/(gs+gva))
    # es_l = 0.611*exp((17.27*Tac)/(237.3+Tac))
    # ea = es_l*hs/100    
    # E = gv*((es_l-ea)/Pa)
    # Ci_new= (((gv-(E/2))*Ca)-A)/(gv+(E/2))


    Ci_new=Ca-A*(1.6/gs+1.37/gb)
    return Ci_new


def coupling_Anci(par_photo, par_gs, meteo_dat, LPI, w=0.1, iter=50, deltaci=0.0001, Tlc=None):
    Tac = meteo_dat['Tac']
    PPFD = meteo_dat['PPFD'] 
    Rg = meteo_dat['Rg'] 
    hs = meteo_dat['hs'] 
    psi = meteo_dat['psi'] 
    u = meteo_dat['u'] 
    Ca = meteo_dat['Ca'] 
    Pa = meteo_dat['Pa']

    i = 0
    Ci = Ca*0.7
    if Tlc==None:#sinon prend Tlc fournie en entree
        Tlc = Tac

    while i<iter :
        An, Rd, id_lim, lsWx, Tx = compute_an(par_photo, PPFD, Tlc, Ci, LPI)
        gb = computeBoundaryLayerConductance(meteo_dat['u'], w)
        es_l = 0.611*exp((17.27*Tac)/(237.3+Tac)) # sacar (22/06/2011)
        ea = es_l*hs/100 # sacar (22/06/2011)
        gs = BWB_gs(An, ea, Tac, Ca, gb, m=par_gs['m'], g0=par_gs['g0'], Pa=Pa)#compute_gs(par_gs, Tlc, hs, An, PPFD, psi, Ca, Pa) #man que parametre gb ds compute_gs , introduit par Jorge?

        Cinew = incrementCi(Ca, An, gs, gb)
        #print i, An, Cinew
        if abs(Cinew-Ci) < deltaci :   
            #print 'nb iteration Ci_'+ str(i)
            Ci = Cinew
            break 
        else:
            Ci = Cinew
            if i>iter-2:
                print 'warning ! Ci calculation does not converge to a solution'   
                                      
        i=i+1

    return An, Cinew, gs, gb, Rd, id_lim, lsWx, Tx
    #coupling_Anci(par_photo_sun, par_gs, meteo_dat, LPI=10., w=0.1, iter=50, deltaci=0.0001)



################
## ancien Compute_AngsCi


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
        An, Cinew, gs, gb, Rd, id_lim, lsWx, Tx = coupling_Anci(par_photo, par_gs, meteo_dat, LPI, w, iter, deltaci, Tlc)

        if tlc_input == 1: #temperature de feuille fournie
            E = Transpiration_rate(Tac, Tlc, ea, gs, gb, Pa = 101.3, epsilon = 0.97)
            break
        else:
            # leaf temperature calculation loop
            Rabs = computeRabs(Rg, Tac, meteo_dat['DOY'], meteo_dat['HU'], lat, alt, alb)#% absorbed radiation short wave radiations (W m-2)
            Tlcnew, E = increment_leafT(Tac, Tlc, ea, Rabs, gs, gb) 
            #print Rabs, Tlcnew
            if  abs(Tlcnew-Tlc) < delta_Tc :
                Tlc = Tlcnew
                ##print 'nb iteration Tl_'+str(j)
                break #% to the end of Tlc loop
            else :
                Tlc = Tlcnew
                Ci = 0.7*Ca # reinitialisation of Ci
                ##print 'nb iteration Tl_'+str(j)       
            
            if j>iter-2:
                print 'warning !!! Tlc calculation does not converge to a solution' 
           
        j=j+1  

    ## rajout a evaluer pour gerer cas des temperature gelive!
    if Tlc<0.: 
        An = 0

    return An, Cinew, gs, gb, Tlc, E, Rd, id_lim, lsWx, Tx



## nouveau format du par_photo
#par_photo1 = {}
#par_photo1['Vcm25']= 91.31
#par_photo1['Jm25'] = 168.
#par_photo1['TPU25'] = 12.72
#par_photo1['cdr'] = 1.424
##reponse a la temperature du alpha (Photochemical efficiency or initial quantum yield) ch Shultz 2003 (suppose constant dans Harley et al. 1992 = 0.24)
#par_photo1['alpha']=  [0.2, 0.2, 0.2, 0.2, 0.2, 0.2]#[0.2, 0.2, 0.19, 0.19, 0.14, 0.12]#[0.2, 0.2, 0.19, 0.19, 0.14, 0.12]
#par_photo1['alpha_T_limit']= [15, 20, 25, 30, 34, 50]
#par_photo1['a1'] = 0.98 # Curvature factor to calculate Jp, usually = 0.98 (Collatz et al 1991)
#par_photo1['a2'] = 0.98 # Curvature factor to calculate Ag, = 0.95 (0.98 for our simulations), Collatz et al 1991
#par_photo1['a3'] = 0.98 # Curvature factor to calculate J; not used in the present version

#par_photo1['Kc25'] = 27.239
#par_photo1['Ko25'] = 16.582
#par_photo1['Tx25'] = 3.743

#par_photo1['RespT_Kc'] = {'model':'Ahrenius', 'c':32.67, 'deltaHa':80.99} # Parameters estimated by Sharkey et al 2007, based on Bernacchi et al 2001 and 2003
#par_photo1['RespT_Ko'] = {'model':'Ahrenius', 'c':9.57, 'deltaHa':23.72} # Parameters estimated by Sharkey et al 2007, based on Bernacchi et al 2001 and 2003

#par_photo1['RespT_Vcm'] = {'model':'Ahrenius', 'c':26.35, 'deltaHa':65.33} # Bernacchi et al 2001 and 2003
#par_photo1['RespT_Jm'] = {'model':'Ahrenius', 'c':17.71, 'deltaHa':43.9} # Bernacchi et al 2001 and 2003
#par_photo1['RespT_TPU'] = {'model':'Ahrenius', 'c':21.46, 'deltaHa':53.1} # Bernacchi et al 2001 and 2003
#par_photo1['RespT_Rd'] = {'model':'Ahrenius', 'c':18.72, 'deltaHa':46.39} # Bernacchi et al 2001 and 2003
#par_photo1['RespT_Tx'] = {'model':'Ahrenius', 'c':9.87, 'deltaHa':24.46} # Parameteres estimated by Sharkey et al 2007


