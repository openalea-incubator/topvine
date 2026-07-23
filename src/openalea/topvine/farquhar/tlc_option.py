def tlc_option(meteo_dat, tsune, tsunw, tshade):
    """ attribue une temperature de feuille mesuree entre cote Est, Ouest et ombre selon le niveau de rayonnement """
    PPFD = meteo_dat['PPFD']
    HU = meteo_dat['HU']
    Tac = meteo_dat['Tac']
            
    if HU < 10:
        Tlc = Tac
    else:
        if HU == 10:
            Tlc = ((0.001429*PPFD)-0.9567)+Tac
        else:
            if HU == 11:
                Tlc = ((0.00152*PPFD)-0.8771)+Tac
            else:
                if HU==12:
                    Tlc =((0.00128*PPFD)-1.0456)+Tac
                else:
                    if HU==13:
                        Tlc = ((0.00145*PPFD)-1.349)+Tac
                    else:
                        if HU==14:
                            Tlc = ((0.001486*PPFD)-1.359)+Tac
                        else:
                            if HU==15:
                                Tlc=((0.001661*PPFD)-1.5508)+Tac
                            else:
                                if HU==16:
                                    Tlc =((0.00141*PPFD)-1.4354)+Tac
                                else:
                                    if HU==17:
                                        Tlc = ((0.001305*PPFD)-1.2124)+Tac
                                    else:
                                        Tlc = Tac                        
                                
                
                
        
        #Tlc = tshade
    #else:
    #    if PPFD >800.:
    #        Tlc = max(tsune,tsunw)
    #    else:
    #        Tlc = min(tsune,tsunw)
    # Tlc = Tac*0.96 + 0.6
    return Tlc
