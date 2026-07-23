def meteo_data(DOY, h, Tac, hs, Rg, PPFD, psi, u=2., Pa=101.3, Ca=360.):
    '''    meteo data : generate a set of meteo data to run the model '''    meteo_data={}    meteo_data['DOY']=DOY    meteo_data['HU']=h    meteo_data['Tac']=Tac    meteo_data['hs']=hs    meteo_data['Rg']=Rg    meteo_data['PPFD']=PPFD    meteo_data['psi']=psi
    meteo_data['u']=u
    meteo_data['Pa']=Pa
    meteo_data['Ca']=Ca
    return meteo_data
