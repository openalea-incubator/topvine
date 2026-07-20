from __future__ import absolute_import
from numpy import exp
from six.moves import range

# Modified on 16/11/2010 to compute An from Vc, Jmax and TPU

def Jmax_nik(Tlc, Jm25, R=0.0083143, Hd=200, S=0.637, c_J=17.71, deltaH_J=43.9): #   c_J=29.2, deltaH_J=62.6,
    #c, deltaH, Hd and S estimated from data by Bernacchi et al 2003 -> temperature optimum de 33.98   
    Tak = Tlc + 273.16
    # Jmax = (((exp((c_J-(deltaH_J /(R*Tak)))))/(1+exp(((S*Tak)-Hd)/(R*Tak))))/50.9)*Jm25
    Jmax = Jm25*(exp((c_J-(deltaH_J /(R*Tak)))))
    return Jmax
    
def Vmax_nik(Tlc, Vm25, R=0.0083143, Hd=200, S=0.635, c_V=26.35, deltaH_V=65.33): # c_V=34.63, deltaH_V=74.6,
    #R, S, H, E estimated from data by Bernacchi et al 2001 -> temperature optimum vers 33  
    Tak = Tlc + 273.16
    # Vmax = (((exp((c_V-(deltaH_V /(R*Tak)))))/(1+exp(((S*Tak)-Hd)/(R*Tak))))/92.09)*Vm25
    Vmax = Vm25*(exp((c_V-(deltaH_V /(R*Tak)))))
    return Vmax

def TPU_nik(Tlc, TPU25, R=0.0083143, c_TP=21.46, deltaH_TP=53.1, deltaD_TP=201.8):
    # c, deltaH, D, estimated from Sharkey et al 2007
    Tak= Tlc + 273.16 
    TPU = TPU25*(exp((c_TP-(deltaH_TP /(R*Tak)))))
    return TPU
    

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
    #c_Kc = par_photo['c_Kc'] 
    #deltaHa_Kc = par_photo['deltaHa_Kc']
    #c_Ko = par_photo['c_Ko']
    #deltaHa_Ko = par_photo['deltaHa_Ko']
    
    Vcm25 = par_photo['Vcm25']
    Jm25 = par_photo['Jm25']
    TPU25 = par_photo['TPU25']
    cdr = par_photo['cdr']      # Rd at 25° measured or calculated from Na content
    a1 = par_photo['a1']        # Curvature factor to calculate Jp, usually = 0.98 (Collatz et al 1991)
    a2 = par_photo['a2']        # Curvature factor to calculate Ag, = 0.95 (0.98 for our simulations), Collatz et al 1991
    a3 = par_photo['a3']        # Curvature factor to calculate J; not used in the present version
    alpha = par_photo['alpha'][0]
    for i in range(1,len(par_photo['alpha'])):
        if par_photo['alpha_T_limit'][i-1]< Tlc < par_photo['alpha_T_limit'][i]:
            alpha = par_photo['alpha'][i]
    
    ##Calculation of net photosynthesis
    Kc = 27.239*((exp(32.67-(80.99 /(R*Tlk))))) # Parameters estimated by Sharkey et al 2007, based on Bernacchi et al 2001 and 2003
    Ko = 16.582*((exp(9.57-(23.72 /(R*Tlk)))))
    
    Vcmax = Vmax_nik(Tlc, Vcm25) # Taux de carboxylation maximal en fonction de la temperature de la feuille
    Jmax = Jmax_nik(Tlc, Jm25)   # Flux maximal d'electrons en fonction de la temperature de la feuille
    TPU = TPU_nik(Tlc, TPU25)    # ajouté le 15/11 selon sharkey 07

    # cdr is the dark respiration at 25°C, it can be calculated through the Na relationship or directly introduced in "Param_Photo"   
    Rd = cdr*((exp(18.7145-(46.39 /(R*Tlk))))) # Parameteres estimated by Bernacchi (2001) and Sharkey et al 2007, must add Na relationship
    T = 3.743*((exp(9.87-(24.46 /(R*Tlk)))))   # Parameteres estimated by Sharkey et al 2007
    J = (alpha*PPFD)/((1+((alpha**2*PPFD**2)/(Jmax**2)))**0.5)  # Flux d'electrons en fonction de la temperature de la feuille et du niveau d'eclairement
    
    
    # The Ci values must be expressed in Pa, so multiplied by 0.1
    Wc = (Vcmax*(Ci*0.1013-T))/((Ci*0.1013)+Kc*(1+O/Ko))         # limitation par la quantite, l'etat d'activation ou les proprietes cinetiques de la Rubisco(Eq (2) Schultz 2003)
    Wj = (J*(Ci*0.1013-T))/(4*((Ci*0.1013)+2.*T))                # limitation par le taux de regeneration de RuBP lie au taux de transfert des electrons au travers du PSII (Eq (3) Schultz 2003)  
    Wp = (TPU*3)                                                 # Sharkey 2007
    # Classical solution:
    Vc = min([Wc, Wj, Wp]) # Taux de carboxylation - #rq: Wp de shultz bug - prends formule de Nikolov, amis qui est un peu "raide" selon eric
    An = Vc*(1-T/(Ci*0.1013))-Rd 

    # Option by Collatz et al (1991): a cuadratic solution is introduced to calculate An and the transition between Wc and Wj. If used, a1 and a2 must be set to 0.98 in "Param_Photo" (values calculated by Collatz 1991)
    # Jp = (Wc + Wj - ((Wc+Wj)**2-(4*Wc*Wj*a1))**0.5)/(2*a1)       # Transition between Wc and Wj; Jp is an intermediate factor between these two limitations (Collatz et al 1991)
    # Ag = (Jp + Wp - ((Jp+Wp)**2-(4*Jp*Wp*a2))**0.5)/(2*a2)       # Transition between Jp and Wp to calculat Ag (gross photosynthesis, Collatz et al 1991)
    # An = Ag - Rd    

    return An
    
def compute_Rd(par_photo, Tlc):

    R = 0.00831 # Constante des gaz parfaits kJ K-1
    # cdr is the dark respiration at 25dC, it can be calculated through the Na relationship or directly introduced in "Param_Photo"   
    cdr = par_photo['cdr']      ## Rd at 25° measured or calculated from Na content
    Tlk = Tlc + 273.15  ## Conversion temperature degreC -> degreK

    Rd = cdr*((exp(18.7145-(46.39 /(R*Tlk))))) # Parameteres estimated by Bernacchi (2001) and Sharkey et al 2007, must add Na relationship

    return Rd  #An + Rd = photosynthese brute



