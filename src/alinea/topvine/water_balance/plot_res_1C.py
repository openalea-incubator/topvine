from __future__ import absolute_import
from rpy import r
from six.moves import range

def as_matrix(tab):
    """ converts a list of list or a python array into an R matrix Robj """
    r.rbind.local_mode(0)
    r.c.local_mode(0)
    x = r.c(tab[0])
    for i in range (1,len(tab)):
        x = r.rbind(x, r.c(tab[i]))

    return x

def plot_res_1C(tab, opt='DOY'):
    """ n step de simul dans une table organise selon:
        [[TSW, FTSW, [D,P,ES,TV],[-,-,-]] , DOY, TT, [Eto, epsi] ]"""
    ## mef des donnees de simul
    TSW, FTSW, D, P, ES, TV, DOY, TT, Eto, epsi = [], [], [], [], [], [], [], [], [], []
    for i in range(1, len(tab)-1, 1):
        DOY.append(tab[i][1])
        TT.append(tab[i][2])
        Eto.append(tab[i][3][0])
        epsi.append(tab[i][3][1])
        TSW.append(tab[i][0][0])
        FTSW.append(tab[i][0][1])
        D.append(tab[i][0][2][0])
        P.append(tab[i][0][2][1])
        ES.append(tab[i][0][2][2])
        TV.append(tab[i][0][2][3])

    ## figure avec r
    r.layout(as_matrix([[1,2,3],[4,5,6]]))#, [3],[4],[5],[6]
    if opt=='DOY':
        x = DOY
        xlab_='DOY'
    else:
        x = TT
        xlab_='TT'

    r.plot(x,Eto, xlab = xlab_, ylab = 'Eto (mm)', type='b')
    r.plot(x,P, xlab = xlab_, ylab = 'Precipitations + Irrigation (mm)', type='b')
    r.plot(x,epsi, xlab = xlab_, ylab = 'Epsilon i', type='l')
    r.plot(x,TV, xlab = xlab_, ylab = 'TV ES',ylim=[0.,5.], col=1, type='l')
    r.points(x,ES, col=2, type='l')
    r.plot(x,TSW, xlab = xlab_, ylab = 'TSW', type='l')
    r.plot(x,FTSW, xlab = xlab_, ylab = 'FTSW', type='l')

    return None
