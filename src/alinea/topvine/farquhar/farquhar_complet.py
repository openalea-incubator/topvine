from math import *
from numpy import exp
import copy

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
    return gb
    #computeBoundaryLayerConductance(2.)


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

def BWB_gs(An, ea, Tac, Ca, m=118.69, g0=15.23, Pa = 101.3):
    '''    Ball Woodrow & Berry stomatal conductance model
    '''
    """ compute stomatal conductance = f(An, ea, Tac, Ca, gb, psi) after ball and Berry (1987)
    An : net photosynthesis  (micromol m2 s-1)
    ea : vapor pressure in the ambiant air (kPa)
    Tac : air temperature (degre celsius)
    Ca : CO2 atmospheric concentration (pa)
    gb : boundary layer conductance (mol m2 s-1) """

    
    es_a = s_avpd(Tac) #% saturated vapor pressure in the ambiant air (kPa)#saturated vapor pressure in the ambiant air (kPa)
    hs = HR(ea, es_a)  # Relative humidity (pourcent)
    gs = (g0+m*An*hs/Ca)/1000. # BWB model, stomatal conductance for water transport (mol m2 s-1) Attention, Ca a remplacer par Cs!
    if gs<g0/1000.:
       gs=g0/1000.

    return gs
    #BWB_gs(15.0,2.,25.,360.)
    #avec deficit hydrique
    #psi=0.1
    #BWB_gs(15.0,2.,30.,360., BWB_m(psi), BWB_g0(psi))


def Jarvis_gs(PPFD, hs, Tac, psi, gsmax = 0.330,  K1= 133, K2 = 0.26 , K3 = 0.004, K4 = 1.85 , psi0 = 0.37 , To = 30):
    '''    compute stomatal conductance = f( PAR, VPD, Tac, psi) after Winckel & Rambal (1990), Jarvis model
    PPFD : Photosynthetic Photon Flux Density (micromol m2 s-1)
    Tac : air temperature (degres celsius)
    hs : relative humidity (pourcent)
    psi : predawn leaf water potential (-MPa)
    gsmax : maximal stomatal conductance (mol m2 s-1)
    K1 : parameter for PPFD response(micromol m2 s-1)
    K2 : parameter for VPD response(kPa-1)
    K3 : parameter for Tac response (degres C-2)
    To : optimal temperature for stomatal openning
    K4 : parameter for psi response (#)
    Psio : value require to reduce maximum gs by half (-MPa)
    '''
    
    es_a = 0.611*exp(17.27*Tac/(237.3+Tac)) # saturated vapor pressure in the ambiant air (kPa)
    ea=es_a*hs/100 # actual vapor pressure at air temperature (kPa)
    D = es_a - ea # vapor pressure deficit at air temperature (kPa)
    g_PPFD = 1.-exp(-PPFD/K1) #PPFD response (micromol photon m2 s-1)
    g_D = exp(-K2*D) #VPD response(kPa-1)
    if ((Tac-To)**2)<1./K3: # Tac response (degres C)
       g_Tac=1.-K3*(Tac-To)**2.
    else:
       g_Tac=0.

       
    g_psi = 1./(1.+(psi/psi0)**K4) # psi response (Mpa)
    gs=gsmax*g_PPFD*g_D*g_Tac*g_psi # (stomatal conductance mol m2 s-1)
    return gs

def compute_gs(par_gs, Tac, hs, An=0, PPFD=0, psi=0.10000000000000001, Ca=360, Pa=101.3):
    '''    compute gs according model and parameters defined in param_gs
    '''
    es_a = s_avpd(Tac) #% saturated vapor pressure in the ambiant air (kPa)#saturated vapor pressure in the ambiant air (kPa)
    ea = es_a*hs/100 #% vapor pressure in the ambiant air (kPa)
    if par_gs['model'] == 'BWB_gs':
        return BWB_gs(An, ea, Tac, Ca, par_gs['m'], par_gs['g0'], Pa)
    elif par_gs['model'] == 'BWB_gs_psi':
        m = BWB_m(psi, par_gs['m0_gs'], par_gs['psi0_gs'], par_gs['n_gs'])
        g0 = BWB_g0(psi, par_gs['psi0_cut'], par_gs['m0_cut'],  par_gs['n_cut'])
        return BWB_gs(An, ea, Tac, Ca, m, g0, Pa)
    elif par_gs['model'] == 'Jarvis_gs':
        return Jarvis_gs(PPFD, hs, Tac, psi, par_gs['gsmax'],  par_gs['K1'], par_gs['K2'] , par_gs['K3'], par_gs['K4'] , par_gs['psi0_jar'] , par_gs['T0'])



def Jmax_nik(Tlc, Jm25, R=8.3143, S=711.36, H=219814, E=81993):
    # R, S, H, E estimated from data by Harley et al 1992 -> temperature optimum de 33.98
    Tak = Tlc + 273.16
    Jmax = Jm25*exp((3.3621*1e-3*Tak-1)*E/(R*Tak))/(1+exp((S*Tak-H)/(R*Tak)))
    return Jmax
    #Jmax_nik(25., 100.05)

def Vmax_nik(Tlc, Vm25, R=8.3143, S=711.36, H=219814, E=81993):
    # R, S, H, E estimated from data by Harley et al 1992 -> temperature optimum vers 40
    Tak = Tlc + 273.16
    Vmax = Vm25*exp(46.9411-116300./(R*Tak))/(1+exp((650.*Tak-202900.)/(R*Tak)))
    return Vmax

def compute_an(par_photo, PPFD, Tlc, Ci, LPI=None):
    '''    compute photosynthesis according to farquhar model
    '''
    """ Fonction which computePhotosynthesis - Farquhar model for grapevine from Schultz FPB 2003 & Nikolov 1995
    """
    # rq: pas besoin de par_gs: donne 1 Ci!

    ##constantes
    O = 21 # pression partielle en oxygene kPa
    R = 0.00831 # Constante des gaz parfaits kJ K-1

    ## Conversion temperature degreC -> degreK 
    Tlk = Tlc + 273.15

    ## reading photosynthesis parameters...
    c_Kc = par_photo['c_Kc'] 
    deltaHa_Kc = par_photo['deltaHa_Kc']
    c_Ko = par_photo['c_Ko']
    deltaHa_Ko = par_photo['deltaHa_Ko']
    e1 =par_photo['e1']
    e2 = par_photo['e2']
    b1 = par_photo['b1']
    b2 = par_photo['b2']
    d1 = par_photo['d1']
    d2 = par_photo['d2']
    Vcm25 = par_photo['Vcm25']
    Jm25 = par_photo['Jm25']
    TPU25 = par_photo['TPU25']
    a1 = par_photo['a1']
    a2 = par_photo['a2']
    a3 = par_photo['a3']
    alpha = par_photo['alpha'][0]
    for i in range(1,len(par_photo['alpha'])):
        if par_photo['alpha_T_limit'][i-1]< Tlc < par_photo['alpha_T_limit'][i]:
            alpha = par_photo['alpha'][i]

    cdr = par_photo['cdr']

    ##Calculation of net photosynthesis
    Kc = (exp(c_Kc-(deltaHa_Kc /(R*Tlk))))
    Ko =( exp(c_Ko-(deltaHa_Ko /(R*Tlk))))
    Vcmax = Vmax_nik(Tlc, Vcm25) # Taux de carboxylation maximal en fonction de la temperature de la feuille
    Jmax = Jmax_nik(Tlc, Jm25) # Flux maximal d'electrons en fonction de la temperature de la feuille
    TPU = Jmax_nik(Tlc, TPU25) # Taux d'utilisation des trioses phosphate en fonction de la temperaude de la feuille 
    ##!!!!(! A remplacer: #utilise empiriquement fonction de temperature de Jmax pour TPU

    #dark respiration Rd fonction de l'age LPI(Schultz, 2003) ou pas (Nikolov, 1995)
    if a1 != None and a2 != None and a3 != None:
        Rd_LPI = a1*exp(a2*LPI)+a3 #relation respiration nocturne LPI (Eq (8) Schultz 2003)
        Rd = Rd_LPI*(1+d1*(Tlk-300.1) + d2*(Tlk-300.1)**2) # reponse de la respiration nocturne a la temperature
    elif a1 == None and cdr!=None:
        #Vm25 = 43.31 #parametre bidon (pin, Nikolov): rq: Nikolov renseigne reponse a la tempereture de Jmax, Vmax.. differemment avec parametre Vm25, Jm25... - ce serait sans doute mieux de renseigner les reponse a la temperature par ces parametres la
        Rd = cdr*Vm25*exp(34.07 - 84450/(R*Tlk)) #eq 16 
    else:
        print 'parameter lacking to compute Rd'

    #point de compensation T fonctions de l'age LPI(Schultz, 2003) ou pas (Nikolov, 1995)
    if b1 != None and b2 != None:
        T_LPI = (b1+b2*LPI) #relation entre point de compensation en l'absence de Rd et LPI (Eq (9) Schultz 2003)
        T = T_LPI+e1*(Tlk-300.1)+e2*(Tlk-300.1)**2 # Reponse du point de compensation en l'absence de Rd a la temperature
    else:
        T = O*(213.88*1e-6 + 8.995*1e-6*(Tlc-25.) + 1.772*1e-7*(Tlc-25.)**2)#eq. 9 Nikolov

    J = (alpha*PPFD)/((1+((alpha**2*PPFD**2)/(Jmax**2)))**0.5)  # Flux d'electrons en fonction de la temperature de la feuille et du niveau d'eclairement


    Wc = (Vcmax*Ci)/(Ci+Kc*(1+O/Ko)) # limitation par la quantite, l'etat d'activation ou les proprietes cinetiques de la Rubisco(Eq (2) Schultz 2003)
    Wj = (J*Ci)/(4.*(Ci+2.*T)) # limitation par le taux de regeneration de RuBP lie au taux de transfert des electrons au travers du PSII (Eq (3) Schultz 2003)  
    Wp = (Vcmax/2.) # Limitation par les disponibilites en phosphate inorganique (Collatz et al 1991)

    Vc = min([Wc, Wj, Wp]) # Taux de carboxylation - #rq: Wp de shultz bug - prends fordumle de Nikolov, amis qui est un peu "raide" selon eric
    An = Vc*(1-T/Ci)-Rd

    return An
    #computePhotosynthesis(600., 23., 260., 15, par_photo_sun)

def incrementCi(Ca, A, gs, gb):
    '''    increment Ci Value
    '''
    Ci_new=Ca-A*(1.6/gs+1.37/gb)
    return Ci_new


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
    es_l = s_avpd(Tlc)#0.611*exp((17.27*Tlc)/(237.3+Tlc))  # saturated vapor pressure at leaf surface (kPa)
    es_a = s_avpd(Tac)#0.611*exp(17.27*Tac/(237.3+Tac))  # saturated vapor pressure in the ambiant air (kPa)
    Y = (ghr/gv)*0.000666  # psychrometer constante (degreC-1)
    E = 2*gv*((es_l-ea)/Pa) # Transpiration rate (mol m-2 s-1)
    delta = (4098*ea)/(Tac+237.3)**2 # slope of vapor pressure curve (kPa degre K-1)
    hs=(ea/es_a)*100  # Relative humidity
    D = es_a-ea # vapor pressure deficit (kPa)
    Tlcnew = Tac+(Y/(delta/Pa+Y)*(((Rabs-epsilon*sigma*(Tac+273)**4)/((ghr*Cp))-(D/(Pa*Y))))) # leaf temperature degreC
    Tlc=Tlcnew

    return Tlcnew,E
    #increment_leafT(25., 25., 2.5, 600, 0.3, 1.2)


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
        An = compute_an(par_photo, PPFD, Tlc, Ci, LPI)
        gb = computeBoundaryLayerConductance(meteo_dat['u'], w)
        gs = compute_gs(par_gs, Tlc, hs, An, PPFD, psi, Ca, Pa)
        Cinew = incrementCi(Ca, An, gs, gb)
        #print i, An, Cinew
        if abs(Cinew-Ci) < deltaci :   
            print 'nb iteration Ci_'+ str(i)
            Ci = Cinew
            break 
        else:
            Ci = Cinew
            if i>iter-2:
                print 'warning ! Ci calculation does not converge to a solution'   
                                      
        i=i+1

    return An, Cinew, gs, gb
    #coupling_Anci(par_photo_sun, par_gs, meteo_dat, LPI=10., w=0.1, iter=50, deltaci=0.0001)


def cougling_Angsci(par_photo, par_gs, meteo_dat, lat=0.44, alt=0.,LPI=10., alb=0.2, w=0.1, iter=50, delta_Tc=0.1, deltaci=0.0001):

    Tac = meteo_dat['Tac'] 
    PPFD = meteo_dat['PPFD'] 
    Rg = meteo_dat['Rg'] 
    hs = meteo_dat['hs'] 
    psi = meteo_dat['psi'] 
    u = meteo_dat['u'] 
    Ca = meteo_dat['Ca'] 
    Pa = meteo_dat['Pa']

    es_a = s_avpd(Tac) #% saturated vapor pressure in the ambiant air (kPa)#saturated vapor pressure in the ambiant air (kPa)
    ea = es_a*hs/100 #% vapor pressure in the ambiant air (kPa)
    D = es_a-ea #% Vapor pressure deficit at air temperature (Kpa)

    ## initialisation
    Tlc = Tac
    Ci = 0.7*Ca #% CO2 substomatal concentration (pa)
    #Rabs = 600  - A CALCULER!!!! fonction???
    ## optimisation loop of Ci et Tlc
    j=1
    while j<iter:#loop Tlc
        # Ci loop
        An, Cinew, gs, gb = coupling_Anci(par_photo_sun, par_gs, meteo_dat, LPI, w, iter, deltaci, Tlc)

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

    return An, Cinew, gs, gb, Tlc


#sun parameters
par_photo_sun = {}

#Kc % Michaelis-mentens constant for carboxylation (PaCO2)
par_photo_sun['c_Kc'] = 35.79 
par_photo_sun['deltaHa_Kc'] = 80.47
#Ko  % Michaelis-mentens constant for oxygenation (kpaO2)
par_photo_sun['c_Ko'] = 9.59 
par_photo_sun['deltaHa_Ko'] = 14.51
#T CO2 comensation point in the absence of dark respiration (PaCO2)
par_photo_sun['e1'] = 1.88 
par_photo_sun['e2'] = 0.036
# Point de compensation fonction de l'age : % parametres d'ajustement pour T*(LPI) : empirique Schultz
par_photo_sun['b1'] = 3.698
par_photo_sun['b2'] = 0.00793
#Rd % rate of CO2 evolution in the light (day respiration) resulting from other process than photorespiration (�mol CO2 m-2 s-1)
par_photo_sun['d1'] = 0.0822 
par_photo_sun['d2'] = 0.00222
# Rd: fonction de l'age 
# % parametre d ajustement pour Rd(LPI) : empirique Schultz
par_photo_sun['a1'] = 0.7863
par_photo_sun['a2'] = -0.31111
par_photo_sun['a3'] = 0.2318
par_photo_sun['cdr'] = None #0.015 in Nikolov: general formulation - coupling Rd with maximum carboxylation rate
#Vcmax % maximum rate of carboxylation (�mol CO2 m-2 s-1)
par_photo_sun['Vcm25'] = 21.96
par_photo_sun['c_Vcmax'] = 32.64 
par_photo_sun['deltaHa_Vcmax'] = 71.23
par_photo_sun['deltaHd_Vcmax'] = 200. 
par_photo_sun['deltaS_Vcmax'] = 0.643
#Jmax % maximum light-saturaed rate of electron transport(�mol electrons m-2 s-1)
par_photo_sun['Jm25'] = 76.59
par_photo_sun['c_Jmax'] = 70.53 
par_photo_sun['deltaHa_Jmax'] = 161.21
par_photo_sun['deltaHd_Jmax'] = 200. 
par_photo_sun['deltaS_Jmax'] = 0.672
#TPU % rate of triose phosphate utilisation (�mol CO2 m-2 s-1)
par_photo_sun['TPU25'] = 4.67 #rq: calcule en ajustant sur fonction Jmax_nik
par_photo_sun['c_TPU'] = 6.66 
par_photo_sun['deltaHa_TPU'] = 11.51
par_photo_sun['deltaHd_TPU'] = 200. 
par_photo_sun['deltaS_TPU'] = 0.636
#alpha % efficience of light conversion related to incident light (mol electrons per mol photons)
par_photo_sun['alpha_T_limit'] = [15,20,25,30, 34, 50] ##discrete temp interval (upper limit)
par_photo_sun['alpha'] = [0.2,0.2,0.19,0.19, 0.14, 0.12] ##corresponding alpha value
##rq: si pas de reponse a Temp de alpha: mettre borne haute + 1 valeur d'alpha

#shade parameters
par_photo_shade = copy.deepcopy(par_photo_sun)
par_photo_shade['a1'] = 0.6262
par_photo_shade['a2'] = -0.349
par_photo_shade['a3'] = 0.1447

par_photo_shade['Vcm25'] = 14.68179206146349
par_photo_shade['c_Vcmax'] = 34.73 
par_photo_shade['deltaHa_Vcmax'] = 76.65
par_photo_shade['deltaHd_Vcmax'] = 200. 
par_photo_shade['deltaS_Vcmax'] = 0.655

par_photo_shade['Jm25'] = 42.84
par_photo_shade['c_Jmax'] = 38.85 
par_photo_shade['deltaHa_Jmax'] = 85.43
par_photo_shade['deltaHd_Jmax'] = 200. 
par_photo_shade['deltaS_Jmax'] = 0.659

par_photo_shade['TPU25'] = 3.017#rq: calcule en ajustant sur fonction Jmax_nik
par_photo_shade['c_TPU'] = 36.93 
par_photo_shade['deltaHa_TPU'] = 87.22
par_photo_shade['deltaHd_TPU'] = 200. 
par_photo_shade['deltaS_TPU'] = 0.659

par_photo_shade['alpha'] = [0.24,0.24,0.22,0.22, 0.16, 0.15] 


#example of formated meteorological data
meteo_dat = {}
meteo_dat['Tac'] = 25.
meteo_dat['PPFD'] = 1500.
meteo_dat['Rg'] = meteo_dat['PPFD']/2.02 #2.02: conesersion �mol.m-2.s-1 de PAR -> W.m-2 de Global
meteo_dat['hs'] = 40.
meteo_dat['psi'] = 0.1
meteo_dat['u'] = 2.
meteo_dat['Ca'] = 360.
meteo_dat['Pa'] = 101.3
meteo_dat['DOY'] = 100
meteo_dat['HU'] = 11.



#example of gs parameters
par_gs = {}
par_gs['model'] = 'BWB_gs_psi' #'BWB_gs', 'Jarvis_gs'
#BWB_gs
par_gs['m'] = 118.69
par_gs['g0'] = 15.23
#BWB_gs_psi
par_gs['m0_gs'] = 129.3
par_gs['psi0_gs'] = 0.37
par_gs['n_gs'] = 1.85
par_gs['m0_cut'] = 41.7
par_gs['psi0_cut'] = 0.35
par_gs['n_cut'] = 1.18
#Jarvis_gs
par_gs['gsmax'] = 0.330
par_gs['K1'] = 133
par_gs['K2'] = 0.26
par_gs['K3'] = 0.004
par_gs['K4'] = 1.85
par_gs['psi0_jar'] = 0.37
par_gs['T0'] = 30.



### Test du module
An = compute_an(par_photo_sun, meteo_dat['PPFD'], 25., 260., LPI=10.)
An, Cinew, gs, gb, Tlc = cougling_Angsci(par_photo_sun, par_gs, meteo_dat, lat=0.44, alt=0.,LPI=10., alb=0.2, w=0.1, iter=50, delta_Tc=0.1, deltaci=0.0001)



#visualisation des courbes de reponse au PPFD
from rpy import r

# reponse a PPFD
v_par, v_An_sun, v_An_shade = [], [], []
temp = 25.
Ci = 260.
for i in range(1,201):
    par =i*10.
    v_par.append(par)
    v_An_sun.append(compute_an(par_photo_sun, par, temp,Ci, LPI=10.))
    v_An_shade.append(compute_an(par_photo_shade, par, temp, Ci, LPI=10.))

r.plot(v_par, v_An_sun, xlab='PAR', ylab='An', main = 'T = '+str(temp)+' Ci = '+str(Ci), col=1)
r.points(v_par, v_An_shade, col=3)


# reponse a T
v_T, v_An_sun, v_An_shade = [], [], []
par = 800
Ci = 260.
for i in range(1,41):
    temp =i
    v_T.append(temp)
    v_An_sun.append(compute_an(par_photo_sun, par, temp,Ci, LPI=10.))
    v_An_shade.append(compute_an(par_photo_shade, par, temp,Ci, LPI=10.))

r.plot(v_T, v_An_sun, xlab='PAR', ylab='T', main = 'PAR = '+str(par)+' Ci = '+str(Ci), col=1)
r.points(v_T, v_An_shade, col=3)
