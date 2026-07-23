def compute_TT(previoustt, tmoy, tbase=10.0):
    dTT = max(0., tmoy-tbase)
    return previoustt+dTT
