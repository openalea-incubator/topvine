
from __future__ import absolute_import
from . import IOtable
from pandas import DataFrame

#add a step to check file format : write a specific procedure
class topologise(object):
    """ topologise rammoy files """ 

    def __call__(self, path):
        #check file format
        ram_moy = open(path, 'r')
        tab_rammoy = IOtable.table_csv(ram_moy) 
        ram_moy.close()
        topo = []
        for i in range(1,len(tab_rammoy)):#primary leaves
            topo.append([tab_rammoy[i][1]])

        for i in range(1,len(tab_rammoy)):#secondary leaves
            n = int(tab_rammoy[i][0])
            if n>0:
                for j in range(n):
                    topo[i-1].append(tab_rammoy[i][2])

        return topo

    def check_format (self, tab_rammoy):
        pass


def toponthefly_2023(
        shoot_specs: DataFrame,
) -> tuple[list[list[float]], list[list[float]]]:
    """Calculates the total leaf area and internode lengths.

    Args:
        shoot_specs: DataFrame including the shoot specifications. Each row represents data for one primary internode.
            The specs are resumed by the following columns:
            - "SF_I" (float): (cm2) surface area of the primary leaf (float, >=0)
            - "SF_II_mean" (float): (cm2) average surface area of secondary leaves (float, >=0)
            - "number_of_phytomers" (int): number of secondary internodes connected to the current primary internode
            - "IN_I_length" (float): (cm) length of the primary internode (float, >=0)

    Returns:
            - leaf area: List of lists, where each sublist represents the surface area of all primary and secondary leaves at each primary internode.
            - primary internode lengths: List of lists, where each sublist contains the length of each primary internode.

    """
    leaf_area: list[list[float]] = shoot_specs.apply(
        lambda x: [float(x["SF_I"])] + ([float(x["SF_II_mean"])] * int(x["number_of_phytomers"])),
        axis=1,
    ).tolist()

    primary_internode_length: list[list[float]] = [[float(v)] for v in shoot_specs["IN_I_length"]]

    if is_legacy_header_row := (
            shoot_specs.iloc[0].to_dict() == {
        k: ((shoot_specs.shape[0] - 1) if k == "number_of_phytomers" else 0)
        for k in shoot_specs.columns
    }):
        leaf_area.pop(0)
        primary_internode_length.pop(0)

    return leaf_area, primary_internode_length
