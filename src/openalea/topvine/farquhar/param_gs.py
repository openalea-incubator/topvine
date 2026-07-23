def param_gs(model, m, g0, m0_gs, psi0_gs, n_gs, m0_cut, psi0_cut, n_cut, gsmax, k1, k2, k3, k4, psi0_jar, t0):
    '''    generate a gui to choose the gs model and define its parameters
    '''
    par_gs = {}
    par_gs['model'] = model
    
    if model == 'BWB_gs':
        #BWB_gs
        par_gs['m'] = m
        par_gs['g0'] = g0
    elif model == 'BWB_gs_psi':
        #BWB_gs_psi
        par_gs['m0_gs'] = m0_gs
        par_gs['psi0_gs'] = psi0_gs
        par_gs['n_gs'] = n_gs
        par_gs['m0_cut'] = m0_cut
        par_gs['psi0_cut'] = psi0_cut
        par_gs['n_cut'] = n_cut
    elif model == 'Jarvis_gs':
        #Jarvis_gs
        par_gs['gsmax'] = gsmax
        par_gs['K1'] = k1
        par_gs['K2'] = k2
        par_gs['K3'] = k3
        par_gs['K4'] = k4
        par_gs['psi0_jar'] = psi0_jar
        par_gs['T0'] = t0

    return par_gs
