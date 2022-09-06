from __future__ import absolute_import
from alinea.topvine import copyvine

def copyvine(obj):
    return copy.deepcopy(obj)
