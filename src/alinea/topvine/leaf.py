import numpy
import random

class Leaf:
    def __init__(self, coord=[0.,0.,0.], rand='none', lawf='none', len=0, id='0000'):
        """ initialize leaf object with normalised values """
        if rand == 'Box':#random coord in a box
            coord = [random.uniform(0.,1.), random.uniform(0.,1.), random.uniform(0.,1.)]
        elif rand == 'Cyl':#random coord in a cylinder
            coord = self.random_cyl()

        self.coord = numpy.array(coord)
        self.len = len
        self.id = id

        if lawf == 'none':#no CxT pair defined
            angle = [0.,0.]
        else:
            paramelv = self.getparams(lawf,'elv')
            paramazi = self.getparams(lawf,'azi')
            angle = [self.random_anglesF (paramelv[0], paramelv[1], paramelv[2]), self.random_anglesF (paramazi[0], paramazi[1], paramazi[2])]

        self.angle=angle


    def __str__(self): #appeler quand 'print obj'
        return 'coord: '+str(self.coord)+' elev: '+str(self.angle[0])+' azim: '+str(self.angle[1])+' length: '+str(self.len)+' id: '+self.id


    def random_cyl(self,r=1.,h=1.): 
        d = r*r +1
        while d > r*r :
            rx= random.uniform(-r,r) 
            ry= random.uniform(-r,r) 
            rz= random.uniform(0,h)
            d = rx*rx + ry*ry   

        return [rx,ry,rz]


    def random_anglesF (self, typel, param1, param2) :
        """tirage d'angles de feuilles selon les parametres specifies dans le fichier Loi de distribution"""
        if typel == 1 :
            angle = random.gauss(param1, param2) 
        elif typel == 2 :
            angle = random.uniform(param1, param2) 
    
        return angle


    def getparams(self, lawf, typea):
        """ recupere les parametres de la loi de distribution du CxT pair en question """
        # besoin de connaitre la position definitive de la feuille pour connaitre quelle loi utiliser! tire seulement valeur normalisees pour les lois normales
        if typea == 'elv':
            return [1, 0., 1.]
        elif typea == 'azi':
            if lawf[2][1] == 2 :
                return [2, -180., 180.] #azimut uniforme pour ces deux CxT
            else:
                return [1, 0., 1.]


    def set_anglesF (self, lawf, NSstatus):
        """ return actual leaf angles according to measured distribution laws and canopy side """
        if NSstatus == 1:#N
            melv, sdelv = lawf[1][2], lawf[1][3]
            mazi, sdazi, typel = lawf[3][2], lawf[3][3], lawf[3][1]
        else:#S
            melv, sdelv = lawf[0][2], lawf[0][3]
            mazi, sdazi, typel = lawf[2][2], lawf[2][3], lawf[2][1]

        if typel == 1:#normal law
            res = [melv+self.angle[0]*sdelv, mazi+self.angle[1]*sdazi]
        elif typel == 2:# law
            res = [melv+self.angle[0]*sdelv, self.angle[1]]

        return res


    def set_coord0(self, Lin, Lb, omega):
        """ return actual leaf coordinates in a SOR defined by the parrallelogram (Lin, Lb, omega); omega in radians """
        coord = [self.coord[0]*Lb*numpy.cos(omega), self.coord[1]*Lb*numpy.cos(omega), self.coord[2]*Lin]
        d = coord[0]**2 + coord[1]**2
        return numpy.array([coord[0], coord[1], coord[2]+numpy.tan(omega)*numpy.sqrt(d)])


    def test(self):
        l = Leaf()
        print(l)
        l = Leaf(rand='Cyl', id='0100')
        print(l)
        law = [['elvS', 1, 45., 20.], ['elvN', 1, 45., 20.], ['aziS', 1, 180., 60.], ['aziN', 1, 0., 60.]]
        l = Leaf(rand='Cyl', id='0100',lawf=law)
        print(l)
        l.set_anglesF (law,1)
        print(l)
        l = Leaf(rand='Cyl', lawf=law,id='0100',len=100)
        print(l)
        l.set_coord0(3.,5., numpy.pi/4)
        print(l)

