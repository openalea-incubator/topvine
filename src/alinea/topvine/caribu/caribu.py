from alinea.caribu.CaribuScene import CaribuScene
from alinea.topvine.topvine_2023 import topvine

import pandas as pd

from alinea.astk.sun_and_sky import sun_sky_sources, sky_sources
from alinea.caribu.light import light_sources

#from alinea.topvine.genodata import *

# %gui qt5


def illuminate(scene, sky=None, sun=None, pattern=None):
    if sky is None and sun is None:
        sun,sky = sun_sky_sources()
    elif sky == 'uoc':
        sky = sky_sources()
    light = []
    if sky is not None:
        light += light_sources(*sky)
    if sun is not None:
        light += light_sources(*sun)
    infinite = False
    if pattern is not None:
        infinite = True
    cs = CaribuScene(scene, light=light, scene_unit='m', pattern=pattern)
    raw, agg = cs.run(direct=True, simplify=True, infinite=infinite)
    return cs, raw, agg


def getfromid(aidee, what):
    if what == 'type':
        return aidee.partition(what)[0]
    elif what == 'phy':
        return int(aidee.partition('type')[2].partition(what)[0])
    elif what == 'ram':
        return int(aidee.partition('type')[2].partition('phy')[2].partition(what)[0])
    elif what == 'plant':
        return int(aidee.partition('type')[2].partition('phy')[2].partition('ram')[2].partition(what)[0])
    else:
        print('wrong keyword')

def topvineANDcaribu(*args,**kwargs):

    scene, tab_shoot = topvine(*args,**kwargs)
    cs, raw, agg = illuminate(scene)

    cs.plot(agg['Ei'])

    thekeys = {s.id: s.name for s in scene}
    theresult = pd.DataFrame(agg)

    thenewcolumn = []

    for key in theresult.index:
        thenewcolumn.append(thekeys[key])

    theresult['id'] = thenewcolumn

    for key in theresult.index:
        if theresult.loc[key]['id'] != thekeys[key]:
            print('error in ' + key)

    for key in theresult.index:
        aid = theresult.loc[key]['id']
        pl = getfromid(aid, 'plant')
        shoot = getfromid(aid, 'ram')
        leafid = getfromid(aid, 'phy')
        leafnum1 = int(leafid / 100) - 1
        leafnum2 = leafid - int(leafid / 100) * 100
        tab_shoot[pl][shoot].topo[leafnum1][leafnum2].Ei = theresult.loc[key]['Ei']

    return scene, tab_shoot,theresult


if __name__ == '__main__':
    scene, tab_shoot = topvine(branches=False, trunk=False, display=False)

    cs, raw, agg = illuminate(scene)

    cs.plot(agg['Ei'])

    thekeys = {s.id: s.name for s in scene}
    theresult = pd.DataFrame(agg)

    thenewcolumn = []

    for key in theresult.index:
        thenewcolumn.append(thekeys[key])

    theresult['id'] = thenewcolumn

    for key in theresult.index:
        if theresult.loc[key]['id'] != thekeys[key]:
            print('error in ' + key)

    for key in theresult.index:
        aid = theresult.loc[key]['id']
        pl = getfromid(aid, 'plant')
        shoot = getfromid(aid, 'ram')
        leafid = getfromid(aid, 'phy')
        leafnum1 = int(leafid / 100) - 1
        leafnum2 = leafid - int(leafid / 100) * 100
        print(aid)
        tab_shoot[pl][shoot].topo[leafnum1][leafnum2].Ei = theresult.loc[key]['Ei']


