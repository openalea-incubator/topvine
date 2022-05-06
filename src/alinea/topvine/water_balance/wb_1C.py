## Modele de reservoir d'eau pour la vigne
##
## Ref
## - Lebon E., Dumas V., Pieri P., Schultz H.R., "Modelling the Seasonal
## Dynamics of the Soil Water Balance of Vineyards", in Functional Plant
## Biology, 30, 699-710, 2003
##
## conersion en Python de la version Matlab - Louarn G., Lebon E.
##  15/12/2010

def vine_T_1C(Et0, epsi, FTSW, leafAlbedo=0.15, FTSWThreshold=0.4):
    coeffTV = epsi/ (1-leafAlbedo)   
    potentialVineTranspiration = coeffTV * Et0
    
    if (FTSW > FTSWThreshold):#previousTSW/TTSW
        # la transpiration de la plante est faite a son potentielle
        Ks = 1.
    else:
        # la quantite d'eau presente dans le sol n'est pas suffisante pour
        # que la transpiration de plante se fasse a son maximum   
        Ks = FTSW/FTSWThreshold

    return Ks*potentialVineTranspiration


def soil_EV_1C(Et0, Precip, epsi, previous_state = [0.,0.,0.], leafAlbedo=0.15, U=5., b=0.63):
    """ U: reservoir superficiel = quantite d'eau dans une couche superieure
        b: coeef empirique sans dimension pour l'evaporation du sol"""

    #recup previous state
    previousSES1 = previous_state[0]
    previousSES2 = previous_state[1]
    previousSEP = previous_state[2]

    coeffTV = epsi/ (1.-leafAlbedo)
    potentialSoilEvaporation = (1. - coeffTV) * Et0
    EP = (1. - coeffTV) * Et0
        
    SES1=max(0., previousSES1)
    SES2=max(0.,previousSES2)
    SEP=max(0.,previousSEP)
    
    P = Precip
    P1 = Precip 
    
    if (SES1<U):
        # phase 1
        if (P1>SES1):
            SES1 = 0.
            SES1 = SES1 + EP
        else:
            SES1 = SES1 - P
            SES1 = SES1 + EP
        
        if (SES1>U):
            ER = EP - 0.4*(SES1-U)
            SES2 = 0.6*(SES1-U)
        else:
            ER = EP;
    else:
        # phase 2
        if (P1>SES2):
            SEP = 0
            P1 = P1 - SES2
            SES1 = U - P1
            
            if (P1>U):
                SES1 = EP
            else:
                SES1 = SES1 + EP
            
            if (SES1>U):
                ER = EP - 0.4*(SES1-U)
                SES2 = 0.6*(SES1-U)
            else:
                ER = EP
            
        else:
            SES21 = ((2*b*SEP + b**2)**0.5) - b
            SEP = SEP + EP;
            SES20 = ((2*b*SEP + b**2)**0.5) - b
            ER = SES20 - SES21
            
            if (P>0):
                ESx = 0.8*P
                
                if (ESx<ER):
                    ESx = ER + P
                
                if (ESx>EP):
                    ESx = EP
                
                ER = ESx
                SES2 = SES2 + ER - P
            else:
                if (ER>EP):
                    ER = EP
                    SES2 = SES2 + ER - P
                else:
                    SES2 = SES2 + ER - P

    state = [SES1, SES2, SEP]
    soilEvaporation = ER 
    return soilEvaporation, state

def TSW_1C (previousTSW, P, ES, TV, TSWmax=200.):
    TSW = previousTSW + P - ES - TV
    D=0.
    if TSW>TSWmax:
        D = TSW-TSWmax
        TSW = TSWmax

    return TSW, TSW/TSWmax, [D, P, ES, TV]


#Et0, Precip, epsi = 3., 0., 0.33
#TSWini = 200.
#TSWmax = 200.
#FTSW = TSWini/TSWmax

##first step
#TV = vine_T_1C(Et0, epsi, FTSW, leafAlbedo=0.15, FTSWThreshold=0.4)
#ES, prev = soil_EV_1C(Et0, Precip, epsi, previous_state = [0.,0.,0.], leafAlbedo=0.15, U=5., b=0.63)
#TSW, FTSW, D = TSW_1C (TSWini, Precip, ES, TV, TSWmax=200.)

##loop
#for i in range(100):
#    TV = vine_T_1C(Et0, epsi, FTSW, leafAlbedo=0.15, FTSWThreshold=0.4)
#    ES, prev = soil_EV_1C(Et0, Precip, epsi, previous_state = prev, leafAlbedo=0.15, U=5., b=0.63)
#    TSW, FTSW, D = TSW_1C (TSW, Precip, ES, TV, TSWmax=200.)
#    print TSW, FTSW

##64.173811961 0.320869059805 au bout de 100 iterations
