from __future__ import print_function
class get_vine_caracteristics(object):
    """  Read stand table at rank n and return vine position and shoot number """ 

    def __init__(self):
        pass


    def __call__(self, stand_tab, rank):
        if rank < len(stand_tab):
            return stand_tab[rank][0], stand_tab[rank][1]
        else:
            print('vine not included in stand table')
