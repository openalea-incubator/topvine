def extract_plant(dict, nump):
    plant_dict = {}
    idp = (3-len(str(nump)))*'0'+str(nump)
    for k in dict.keys():
        if str(k)[0]=='1' and str(k)[-3:] == str(idp):#opt=1 et nump=idp
            plant_dict[k]=dict[k]

    return plant_dict

