import IOtable

class stand_generator(object):
    """  Doc... """ 

    def __init__(self):
            pass


    def __call__(self, carto_path, CxT, personalise, nbr, nbp):
        if personalise == False:
            f = file(carto_path, 'r')
            tab_carto = IOtable.table_csv(f) 
            f.close()
        else:
            ecart_r, ecart_plante, nbram = 220, 110, 12 # a ajouter en input
            tab_carto = []
            for i in range(nbr):
                for j in range(nbp):
                    tab_carto.append([i*ecart_r, j*ecart_plante, nbram])

        # en attendant de generer les paramtres geometriques (rpy), lecture dans un fichier
        path_geom = r'C:\Documents and Settings\Karine\.openalea\user_pkg\topvine\geom\ex_geom.csv'
        f = file(path_geom, 'r')
        tab_geom = IOtable.table_csv(f) 
        f.close()
        # faire une fonction qui fait le bon nombre de plante / rameaux par plantes
        # appliquer fonction actualise coord0        
        return tab_geom

    def actualise_coord(self, tab_carto, tab_geom):
        return tab_geom
