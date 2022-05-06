from __future__ import absolute_import
from . import IOtable
from numpy import array
from six.moves import range


class get_dl_shoot(object):
    """ get distribution laws of spurs and shoot parameters from a csv file """
    
    def __init__(self):
        pass

    def __call__(self, path):
        f = open(path)
        tab = IOtable.table_csv_str(f)
        f.close()

        #converti en float
        for i in range(len(tab)):
            for j in range(1,len(tab[i])):
                if tab[i][j] != '':
                    tab[i][j] = float(tab[i][j])

        spurs0, dspurs, f_azi, shoot = self.get_shoot_param(tab)
        return spurs0, dspurs, f_azi, shoot

    def get_shoot_param(self, t):
        """ recupere loi distribution des coursons et des parametre de rameau """
        
        #distribution (x,y,z) of spurs 1 to 6
        spurs0 = [[(t[0][1],t[0][2]),(t[6][1],t[6][2]),(t[12][1],t[12][2])], [(t[1][1],t[1][2]),(t[7][1],t[7][2]),(t[12][1],t[12][2])], [(t[2][1],t[2][2]),(t[8][1],t[8][2]),(t[12][1],t[12][2])], [(t[3][1],t[3][2]),(t[9][1],t[9][2]),(t[12][1],t[12][2])], [(t[4][1],t[4][2]),(t[10][1],t[10][2]),(t[12][1],t[12][2])], [(t[5][1],t[5][2]),(t[11][1],t[11][2]),(t[12][1],t[12][2])]]
        
        #distribution for the distance beteween the two buds on a spur
        dspurs = [(t[13][1],t[13][2]),(t[14][1],t[14][2]),(t[15][1],t[15][2])]
        
        #shoot proportion in azi sectors
        f_azi = t[17][1:5]
        
        #mean vector [alpha, phi, Ls, MX] and covariance matrix for multivarita distribution
        x1, x2, x3, x4 = array(t[18][1:5]), array(t[19][1:5]), array(t[20][1:5]), array(t[21][1:5])
        S1  = array([t[22][1:5], t[23][1:5], t[24][1:5], t[25][1:5]])
        S2  = array([t[26][1:5], t[27][1:5], t[28][1:5], t[29][1:5]])
        S3  = array([t[30][1:5], t[31][1:5], t[31][1:5], t[33][1:5]])
        S4  = array([t[34][1:5], t[35][1:5], t[36][1:5], t[37][1:5]])
        
        shoot = [(x1, S1), (x2, S2), (x3, S3), (x4, S4)]
        
        return spurs0, dspurs, f_azi, shoot

