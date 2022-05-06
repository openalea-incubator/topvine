from __future__ import absolute_import
import openalea.plantgl.all as pgl

def mesh(geometry):
    d = pgl.Discretizer()
    geometry.apply(d)
    return d.result
    
def mesh_to_can(self, geometry, label):
    """ 
    Returns a string iterator with triangles and labels.
    """
    p = geometry.pointList
    index = geometry.indexList
    def line(ind, label):
        return "p 2 %s 9 3 %s"%(str(label), ' '.join(str(x) for i in ind for x in p[i]))

    return (line(ind, label) for ind in index)
    
