from __future__ import absolute_import
from numpy import array
from numpy.random import multivariate_normal, seed
import random
from six.moves import range


class gen_shoot_param(object):
    """  Generates shoot parameters for a vine of n shoots """ 

    def __init__(self):
        pass
    
    
    def __call__(self, n, spurs0, dspurs, f_azi, shoot_param, graine=0):
        random.seed(graine)
        seed(graine)
        tab_geom = self.gen_spurs(n, spurs0, dspurs)
        for i in range(len(tab_geom)):
            geom = self.gen_shoot(f_azi, shoot_param)
            tab_geom[i] = tab_geom[i] + geom

        return tab_geom

   
    def gen_spurs(self, n, spurs0, dspurs):
        """ """
        #genere liste de numero de rang de courson longue de n
        #   6 premiers sur coursons differents dans ordre aleatoire
        #   6 suivants aleatoirement a distance dspurs des 6 premiers
        #   n-12 suivants : tirage de rang aleatoire + position avec spurs0
        if n<=6:
            order = [[random.uniform(0.,1.),1], [random.uniform(0.,1.), 2], [random.uniform(0.,1.), 3], [random.uniform(0.,1.), 4], [random.uniform(0.,1.), 5], [random.uniform(0.,1.), 6]]
            order.sort()
            seq = order[0:n]
        elif n<=12:
            seq = [[random.uniform(0.,1.),1], [random.uniform(0.,1.), 2], [random.uniform(0.,1.), 3], [random.uniform(0.,1.), 4], [random.uniform(0.,1.), 5], [random.uniform(0.,1.), 6]]
            order = [[random.uniform(0.,1.),1], [random.uniform(0.,1.), 2], [random.uniform(0.,1.), 3], [random.uniform(0.,1.), 4], [random.uniform(0.,1.), 5], [random.uniform(0.,1.), 6]]
            order.sort()
            seq = seq + order[0:n-6]
        else:
            seq = [[random.uniform(0.,1.),1], [random.uniform(0.,1.), 2], [random.uniform(0.,1.), 3], [random.uniform(0.,1.), 4], [random.uniform(0.,1.), 5], [random.uniform(0.,1.), 6]]
            seq = seq + [[random.uniform(0.,1.),1], [random.uniform(0.,1.), 2], [random.uniform(0.,1.), 3], [random.uniform(0.,1.), 4], [random.uniform(0.,1.), 5], [random.uniform(0.,1.), 6]]
            for i in range(12, n):
                seq = seq + [[0., int(round(random.uniform(1.,6.), decimals=0))]]
    
        
        #tirage des coord x,y,z des coursons en fonction de leur rang (r)
        if n<=6:
            for i in range(n):
                r = seq[i][1]-1
                x, y , z = random.gauss(spurs0[r][0][0], spurs0[r][0][1]), random.gauss(spurs0[r][1][0], spurs0[r][1][1]),random.gauss(spurs0[r][2][0], spurs0[r][2][1])
                seq[i].append(array([x,y,z]))
        elif n<=12:
            for i in range(6):
                r = seq[i][1]-1
                x, y , z = random.gauss(spurs0[r][0][0], spurs0[r][0][1]), random.gauss(spurs0[r][1][0], spurs0[r][1][1]),random.gauss(spurs0[r][2][0], spurs0[r][2][1])
                seq[i].append(array([x,y,z]))
    
            for i in range(6,n):
                r = seq[i][1]-1
                dx, dy, dz = random.gauss(dspurs[0][0], dspurs[0][1]), random.gauss(dspurs[1][0], dspurs[1][1]),random.gauss(dspurs[2][0], dspurs[2][1])
                coord = seq[r][2] + array([dx, dy, dz])
                seq[i].append(coord)
        else:
            for i in range(6):
                r = seq[i][1]-1
                x, y , z = random.gauss(spurs0[r][0][0], spurs0[r][0][1]), random.gauss(spurs0[r][1][0], spurs0[r][1][1]),random.gauss(spurs0[r][2][0], spurs0[r][2][1])
                seq[i].append(array([x,y,z]))
    
            for i in range(6,12):
                r = seq[i][1]-1
                dx, dy, dz = random.gauss(dspurs[0][0], dspurs[0][1]), random.gauss(dspurs[1][0], dspurs[1][1]),random.gauss(dspurs[2][0], dspurs[2][1])
                coord = seq[r][2] + array([dx, dy, dz])
                seq[i].append(coord)
    
            for i in range(12,n):
                r = seq[i][1]-1
                x, y , z = random.gauss(spurs0[r][0][0], spurs0[r][0][1]), random.gauss(spurs0[r][1][0], spurs0[r][1][1]),random.gauss(spurs0[r][2][0], spurs0[r][2][1])
                seq[i].append(array([x,y,z]))
    
        #retire les seeds et range les coursous dans l'ordre
        for i in range(len(seq)):
            seq[i]=seq[i][1:]
    
        seq = sorted(seq, key=lambda elt: elt[0])
    
        return seq


    def gen_shoot(self, f_azi, shoot_param):
        """ """
        # definir borne  azimut
        b2 = f_azi[0] + f_azi[1]
        b3 = b2 + f_azi[2]
        b4 = b3 + f_azi[3]
        b = [f_azi[0], b2, b3, b4]
        # tirage azimut et autres parametres avec loi normale multivariee
        razi = random.uniform(0., 1.)
        if razi<= b[0]:#-20 20
            azi = [random.uniform(-20, 20)]
            sh = multivariate_normal(shoot_param[0][0], shoot_param[0][1])
        elif razi>b[0] and razi<= b[1]:#20 160
            azi = [random.uniform(20, 160)]
            sh = multivariate_normal(shoot_param[1][0], shoot_param[1][1])
        elif razi>b[1] and razi<= b[2]:#160 200
            azi = [random.uniform(160, 200)]
            sh = multivariate_normal(shoot_param[2][0], shoot_param[2][1])
        else :#200 340
            azi = [random.uniform(200, 340)]
            sh = multivariate_normal(shoot_param[3][0], shoot_param[3][1])
    
        sh = sh.tolist()
        return azi + sh
    


