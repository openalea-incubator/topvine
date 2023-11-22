from alinea.caribu.CaribuScene import CaribuScene
from alinea.topvine.topvine_2023 import topvine

import pandas as pd

# %gui qt5

scene, tab_shoot = topvine(branches=False, trunk=False)
cs = CaribuScene(scene, scene_unit='cm')
raw, agg = cs.run(direct=True, simplify=True)

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


for key in theresult.index:
    aid = theresult.loc[key]['id']
    pl = getfromid(aid, 'plant')
    shoot = getfromid(aid, 'ram')
    leafid = getfromid(aid, 'phy')
    leafnum1 = int(leafid/100)-1
    leafnum2 = leafid - int(leafid/100)*100
    print(aid)
    tab_shoot[pl][shoot].topo[leafnum1][leafnum2].Ei = theresult.loc[key]['Ei']
