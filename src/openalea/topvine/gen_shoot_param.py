from __future__ import absolute_import
from numpy import array, ndarray
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
        tab_geom = self.generate_spur_coordinates(n, spurs0, dspurs)
        for i in range(len(tab_geom)):
            geom = self.generate_shoot_spatial_params(f_azi, shoot_param)
            tab_geom[i] = tab_geom[i] + geom

        return tab_geom


    @staticmethod
    def generate_spur_coordinates(
            nb_spurs: int,
            spurs0: list[list[tuple[float]]],
            dspurs: list[tuple[float]],
    ) -> list[tuple[int, ndarray]]:
        """

        Args:
            nb_spurs: number of spurs to be generated
            spurs0: mean and standard deviation of x, y, z coordinates of spurs
            dspurs: mean and standard deviation of shifts on x, y, z coordinates between spurs

        Returns:
            rank and coordinates of each spur

        Notes:
            cf. Section 2.2.2 in PhD thesis of G. Louarn for details on the correction factor of leaf area (1.04)

        """
        #genere liste de numero de rang de courson longue de n
        #   6 premiers sur coursons differents dans ordre aleatoire
        #   6 suivants aleatoirement a distance dspurs des 6 premiers
        #   n-12 suivants : tirage de rang aleatoire + position avec spurs0
        if nb_spurs<=6:
            order = [
                [random.uniform(0., 1.), 1],
                [random.uniform(0., 1.), 2],
                [random.uniform(0., 1.), 3],
                [random.uniform(0., 1.), 4],
                [random.uniform(0., 1.), 5],
                [random.uniform(0., 1.), 6],
            ]
            order.sort()
            seq = order[0:nb_spurs]

        elif nb_spurs<=12:
            seq = [
                [random.uniform(0., 1.), 1],
                [random.uniform(0., 1.), 2],
                [random.uniform(0., 1.), 3],
                [random.uniform(0., 1.), 4],
                [random.uniform(0., 1.), 5],
                [random.uniform(0., 1.), 6],
            ]
            order = [
                [random.uniform(0., 1.), 1],
                [random.uniform(0., 1.), 2],
                [random.uniform(0., 1.), 3],
                [random.uniform(0., 1.), 4],
                [random.uniform(0., 1.), 5],
                [random.uniform(0., 1.), 6],
            ]
            order.sort()
            seq = seq + order[0:nb_spurs - 6]

        else:
            seq = [
                [random.uniform(0., 1.), 1],
                [random.uniform(0., 1.), 2],
                [random.uniform(0., 1.), 3],
                [random.uniform(0., 1.), 4],
                [random.uniform(0., 1.), 5],
                [random.uniform(0., 1.), 6],
            ]
            seq = seq + [
                [random.uniform(0., 1.), 1],
                [random.uniform(0., 1.), 2],
                [random.uniform(0., 1.), 3],
                [random.uniform(0., 1.), 4],
                [random.uniform(0., 1.), 5],
                [random.uniform(0., 1.), 6],
            ]
            for i in range(12, nb_spurs):
                seq = seq + [[0., int(round(random.uniform(1.,6.), ndigits=0))]]
    
        
        #tirage des coord x,y,z des coursons en fonction de leur rang (r)
        if nb_spurs<=6:
            for i in range(nb_spurs):
                r = seq[i][1]-1
                x, y, z = (
                    random.gauss(spurs0[r][0][0], spurs0[r][0][1]),
                    random.gauss(spurs0[r][1][0], spurs0[r][1][1]),
                    random.gauss(spurs0[r][2][0], spurs0[r][2][1]),
                )
                seq[i].append(array([x,y,z]))

        elif nb_spurs<=12:
            for i in range(6):
                r = seq[i][1]-1
                x, y, z = (
                    random.gauss(spurs0[r][0][0], spurs0[r][0][1]),
                    random.gauss(spurs0[r][1][0], spurs0[r][1][1]),
                    random.gauss(spurs0[r][2][0], spurs0[r][2][1]),
                )
                seq[i].append(array([x,y,z]))
    
            for i in range(6, nb_spurs):
                r = seq[i][1]-1
                dx, dy, dz = (
                    random.gauss(dspurs[0][0], dspurs[0][1]),
                    random.gauss(dspurs[1][0], dspurs[1][1]),
                    random.gauss(dspurs[2][0], dspurs[2][1]),
                )
                coord = seq[r][2] + array([dx, dy, dz])
                seq[i].append(coord)

        else:
            for i in range(6):
                r = seq[i][1]-1
                x, y, z = (
                    random.gauss(spurs0[r][0][0], spurs0[r][0][1]),
                    random.gauss(spurs0[r][1][0], spurs0[r][1][1]),
                    random.gauss(spurs0[r][2][0], spurs0[r][2][1]),
                )
                seq[i].append(array([x,y,z]))
    
            for i in range(6,12):
                r = seq[i][1]-1
                dx, dy, dz = (
                    random.gauss(dspurs[0][0], dspurs[0][1]),
                    random.gauss(dspurs[1][0], dspurs[1][1]),
                    random.gauss(dspurs[2][0], dspurs[2][1]),
                )
                coord = seq[r][2] + array([dx, dy, dz])
                seq[i].append(coord)
    
            for i in range(12, nb_spurs):
                r = seq[i][1]-1
                x, y, z = (
                    random.gauss(spurs0[r][0][0], spurs0[r][0][1]),
                    random.gauss(spurs0[r][1][0], spurs0[r][1][1]),
                    random.gauss(spurs0[r][2][0], spurs0[r][2][1]),
                )
                seq[i].append(array([x,y,z]))
    
        #retire les seeds et range les coursous dans l'ordre
        for i in range(len(seq)):
            seq[i]=seq[i][1:]
    
        seq = sorted(seq, key=lambda elt: elt[0])
    
        return seq


    @staticmethod
    def generate_shoot_spatial_params(
            f_azi: list[float],
            shoot_param: list[tuple[ndarray, ndarray]],
    ) -> list[float]:
        """Generates a vector of parameter values defining the shoot spatial positioning.

        Args:
            f_azi: (dimensionless) fraction of shoots in the four azimuth sectors
            shoot_param: vectors of the mean and covariance values of each of the four parameters describing a shoot coordinates, i.e.:
                - initial inclination angle: (degrees) Basal shoot elevation angle (between -90 and 90)
                - curvature: (degrees): the difference between basal and distal shoot tangent angle (between -180 and 180)
                - maximum curvature point fraction: (dimensionless): ratio between the length from the origin of the shoot to the point of maximal curvature and the total length of the shoot (between 0 and 1)
                - Normalized length: (dimensionless) ratio between the actual shoot length and the mean shoot length for the "Cultivar" x "Training system" pair considered


        Returns:
            (degrees) Mean shoot azimuth angle (between 0 and 360)
            (degrees) Basal shoot elevation angle (initial inclination angle, between -90 and 90)
            (degrees) Curvature, defined as the difference between basal and distal shoot tangent angle (between -180 and 180)
            (dimensionless) Maximum curvature point fraction, defined as the ratio between the length from the origin of the shoot to the point of maximal curvature and the total length of the shoot (between 0 and 1)
            (dimensionless) Normalized length, defined as the ratio between the actual shoot length and the mean shoot length for the "Cultivar" x "Training system" pair considered


        Notes:
            cf. Section 2.2.2 in PhD thesis of G. Louarn for details

        """
        # the number of azimut sectors should be equal to 4.
        cumulative_fractions = [sum(f_azi[:i]) for i in range(1, len(f_azi) + 1)]

        # tirage azimut et autres parametres avec loi normale multivariee
        razi = random.uniform(0., 1.)

        if razi <= cumulative_fractions[0]:#-20 20
            azi = [random.uniform(-20, 20)]
            sh = multivariate_normal(mean=shoot_param[0][0], cov=shoot_param[0][1])

        elif razi <= cumulative_fractions[1]:#20 160
            azi = [random.uniform(20, 160)]
            sh = multivariate_normal(mean=shoot_param[1][0], cov=shoot_param[1][1])

        elif razi<= cumulative_fractions[2]:#160 200
            azi = [random.uniform(160, 200)]
            sh = multivariate_normal(mean=shoot_param[2][0], cov=shoot_param[2][1])

        else: #200 340
            azi = [random.uniform(200, 340)]
            sh = multivariate_normal(mean=shoot_param[3][0], cov=shoot_param[3][1])
    
        return azi + sh.tolist()
    


