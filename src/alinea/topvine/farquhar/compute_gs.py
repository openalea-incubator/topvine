from __future__ import absolute_import
from .BWB_gs import *
from .Jarvis_gs import *
from .meteo_utils import s_avpd

def compute_gs(par_gs, Tac, hs, An=0, PPFD=0, psi=0.10000000000000001, Ca=360, Pa=101.3):
    '''    compute gs according model and parameters defined in param_gs
    '''
    es_a = s_avpd(Tac) #% saturated vapor pressure in the ambiant air (kPa)#saturated vapor pressure in the ambiant air (kPa)
    ea = es_a*hs/100 #% vapor pressure in the ambiant air (kPa)
    if par_gs['model'] == 'BWB_gs':
        return BWB_gs(An, ea, Tac, Ca, par_gs['m'], par_gs['g0'], Pa) #rq: Bug!!! manque gs rajoute par Jorge!!
    elif par_gs['model'] == 'BWB_gs_psi':
        m = BWB_m(psi, par_gs['m0_gs'], par_gs['psi0_gs'], par_gs['n_gs'])
        g0 = BWB_g0(psi, par_gs['psi0_cut'], par_gs['m0_cut'],  par_gs['n_cut'])
        return BWB_gs(An, ea, Tac, Ca, m, g0, Pa)
    elif par_gs['model'] == 'Jarvis_gs':
        return Jarvis_gs(PPFD, hs, Tac, psi, par_gs['gsmax'],  par_gs['K1'], par_gs['K2'] , par_gs['K3'], par_gs['K4'] , par_gs['psi0_jar'] , par_gs['T0'])
