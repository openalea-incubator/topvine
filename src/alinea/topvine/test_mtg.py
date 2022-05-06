from __future__ import absolute_import
import openalea.mtg as mtg
from six.moves import range


#print len(g)
#print g.nb_vertices()
#print g.nb_scales()

#root = g.root
#print g.scale(root)
n=100


g = mtg.MTG()
plant1 = g.add_component(g.root, label='Plant')
# Edit the tree at scale 1 by adding one children (plant)
axe1 = g.add_component(plant1, label='Axe')
# Edit the tree at scale 2 by adding one children (shoot)
v = g.add_component(axe1, label='Phytomer')
# Edit the tree at scale 2 by adding one children (phytomer) -> n digitized leaves
for i in range(n-1):
    v = g.add_child(v, edge_type='<', label='Phytomer')

g = mtg.fat_mtg(g)

#add properties?
g.add_property("geometry")
geometry = g.get_property('geometry')

for v in g.vertices(scale=3):
     geometry[v] = Sphere()
#    g.property("geometry").update(....)
