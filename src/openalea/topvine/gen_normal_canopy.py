from __future__ import absolute_import
from numpy import ndarray
import random
from . import leaf
from . import shoot
from six.moves import range


class gen_normal_canopy(object):
    """  generates a list of normalised shoot objects associationg average topology with geometric features (primary shoot geom, leaf angles, leaf dimensions) """ 

    def __init__(self):
        pass


    def __call__(self, tab_geom, topol, dl_leaf):
        res = []

        for i in range(len(tab_geom)):
            ### topl = generate_rameau(NFI,NFII,LEN, SF, sd, sd)
            p = []
            for j in range(len(tab_geom[i])):
                p.append(shoot.Shoot(tab_geom[i][j], topol, dl_leaf))

            res.append(p)

        return res


def create_normalized_canopy(
        shoot_params: list[list[tuple[int, ndarray, float, float, float, float, float]]],
        topol: tuple[list[list[float]], list[list[float]]],
        dl_leaf: tuple[tuple[str, int, float, float]],
) -> shoot.Shoot_2023:
    """Generates a list of normalised shoot objects associating average topology with geometric features
    (primary shoot geom, leaf angles, leaf dimensions)

    Args:
        shoot_params: values of parameters that define the geometry of the shoot (all included in a list of lists of length=1):
            - (int) shoot order in the plant (dimensionless)
            - (ndarray) bud coordinates, i.e. base of the shoot (m)
            - (float) Mean shoot azimuth angle (degrees, between 0 and 360)
            - (float) Basal shoot elevation angle (initial inclination angle, degrees, between -90 and 90)
            - (float) Curvature (degrees), defined as the difference between basal and distal shoot tangent angle (between -180 and 180)
            - (float) Maximum curvature point fraction (dimensionless), defined as the ratio between the length from the origin of the shoot to the point of maximal curvature and the total length of the shoot (between 0 and 1)
            - (float) Normalized length (dimensionless), defined as the ratio between the actual shoot length and the mean shoot length for the "Cultivar" x "Training system" pair considered
        topol: values of parameters that define the topology of the shoot:
            - list[list[float] leaf area (cm2) of primary (first item) and secondary (remaining items) at each primary internode of the shoot
            - list[list[float] length (cm) of primary internodes (each internode length is set in a list)
        dl_leaf: distribution laws for leaf orientation

    Returns:
        shoot object

    """
    return shoot.Shoot_2023(
        Pgeom=shoot_params[0][0],
        topol=topol,
        law=dl_leaf,
    )