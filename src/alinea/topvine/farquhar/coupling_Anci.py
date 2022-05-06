from meteo_utils import *
from compute_gs import *
from compute_an import *

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
        An = compute_an(par_photo, PPFD, Tlc, Ci, LPI)
        gb = computeBoundaryLayerConductance(meteo_dat['u'], w)
        es_l = 0.611*exp((17.27*Tac)/(237.3+Tac)) # sacar (22/06/2011)
        ea = es_l*hs/100 # sacar (22/06/2011)
        gs = BWB_gs(An, ea, Tac, Ca, gb, m=par_gs['m'], g0=par_gs['g0'], Pa=Pa)#compute_gs(par_gs, Tlc, hs, An, PPFD, psi, Ca, Pa) #man que parametre gb ds compute_gs , introduit par Jorge?

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

