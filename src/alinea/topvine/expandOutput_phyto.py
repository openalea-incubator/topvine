from six.moves import range
def expandOutput_phyto(caribu_dict, keys, values):
    '''    
    '''

    photo_dict = {}
    for i in range(len(keys)):
        photo_dict[keys[i]] = values[i]

    caribu_dict['photo'] = []
    #add the average into the av column
    for i in range(len(caribu_dict['id'])):
        caribu_dict['photo'].append(photo_dict[caribu_dict['id'][i]])

    return caribu_dict, photo_dict
