from numpy import array


class translate_shoots(object):
    """  translates all shoots params of vector v """ 

    def __init__(self):
        pass


    def __call__(self, shoot_params, v):
        for i in range (len(shoot_params)):
            shoot_params[i][1] = shoot_params[i][1] + v

        return shoot_params
