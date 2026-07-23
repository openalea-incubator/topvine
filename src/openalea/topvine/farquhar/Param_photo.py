def param_photo(c_kc, deltaha_kc, c_ko, deltaha_ko, e1, e2, b1, b2, d1, d2, vcm25, jm25, tpu25, a1, a2, a3, alpha_T_limit, alpha_val, cdr):
    '''    Parameters for Farquhar model
    '''

    par_photo = {}

    #Kc Michaelis-mentens constant for carboxylation (PaCO2)
    par_photo['c_Kc'] = c_kc 
    par_photo['deltaHa_Kc'] = deltaha_kc
    #Ko  Michaelis-mentens constant for oxygenation (kpaO2)
    par_photo['c_Ko'] = c_ko 
    par_photo['deltaHa_Ko'] = deltaha_ko
    #T CO2 comensation point in the absence of dark respiration (PaCO2)
    par_photo['e1'] = e1 
    par_photo['e2'] = e2
    # Point de compensation fonction de l'age : pourcent parametres d'ajustement pour T*(LPI) : empirique Schultz
    par_photo['b1'] = b1
    par_photo['b2'] = b2
    #Rd rate of CO2 evolution in the light (day respiration) resulting from other process than photorespiration (micromol CO2 m-2 s-1)
    par_photo['d1'] = d1 
    par_photo['d2'] = d2
    # Rd: fonction de l'age 
    # parametre d ajustement pour Rd(LPI) : empirique Schultz
    par_photo['a1'] = a1
    par_photo['a2'] = a2
    par_photo['a3'] = a3
    par_photo['cdr'] = cdr #0.015 in Nikolov: general formulation - coupling Rd with maximum carboxylation rate
    #Vcmax maximum rate of carboxylation (micromol CO2 m-2 s-1)
    par_photo['Vcm25'] = vcm25
    #par_photo['c_Vcmax'] = 32.64 
    #par_photo['deltaHa_Vcmax'] = 71.23
    #par_photo['deltaHd_Vcmax'] = 200. 
    #par_photo['deltaS_Vcmax'] = 0.643
    #Jmax % maximum light-saturaed rate of electron transport(micromol electrons m-2 s-1)
    par_photo['Jm25'] = jm25
    #par_photo['c_Jmax'] = 70.53 
    #par_photo['deltaHa_Jmax'] = 161.21
    #par_photo['deltaHd_Jmax'] = 200. 
    #par_photo['deltaS_Jmax'] = 0.672
    #TPU % rate of triose phosphate utilisation (micromol CO2 m-2 s-1)
    par_photo['TPU25'] = tpu25 #rq: calcule en ajustant sur fonction Jmax_nik
    #par_photo['c_TPU'] = 6.66 
    #par_photo['deltaHa_TPU'] = 11.51
    #par_photo['deltaHd_TPU'] = 200. 
    #par_photo['deltaS_TPU'] = 0.636
    #alpha % efficience of light conversion related to incident light (mol electrons per mol photons)
    par_photo['alpha_T_limit'] = alpha_T_limit##discrete temp interval (upper limit)
    par_photo['alpha'] = alpha_val ##corresponding alpha value
    ##rq: si pas de reponse a Temp de alpha: mettre borne haute + 1 valeur d'alpha
    return par_photo
