from alinea.topvine.caribu.caribu import illuminate, getfromid
from alinea.topvine.topvine_2023 import topvine

import pandas as pd

def simulate(**kwargs):
    scene = topvine(branches=False, trunk=False, display=False, **kwargs)[0]
    cs, raw, agg = illuminate(scene)
    thekeys = {s.id: s.name for s in scene}
    theresult = pd.DataFrame(agg)

    thenewcolumn = []

    for key in theresult.index:
        thenewcolumn.append(thekeys[key])

    theresult['id'] = thenewcolumn

    for key in theresult.index:
        if theresult.loc[key]['id'] != thekeys[key]:
            print('error in ' + key)
    return theresult

class Simgenorder(object):

    def __init__(self):
        self.list=[]

    def add(self, couple):
        errline = "Error: simulation order is a list of pair of genotype and number"
        if len(couple) != 2 or not isinstance(couple[0],Genotype) or not isinstance(couple[1],int):
            print(errline)
        self.list.append(couple)

def multisim(orders):
    if not isinstance(orders,Simgenorder):
        errline = "Error: simulation order must be a Simgenorder object"
        print(errline)
        return

    resultlist=[]
    ornum=0
    for order in orders.list:
        ornum=ornum+1
        print("serving order "+str(ornum))

        for simno in range(order[1]):
            if simno%10 == 0:
                print("sim "+ str(simno+1)+ " of " + str(order[1]) )
            resultlist.append(simulate(gen=order[0]))

    return resultlist


