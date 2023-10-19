
import cv2 as cv
import numpy as np


class Tracker():
    
    def __inint__(self):
        self._objectes = []
        self._ids = []


    def deteccio(self, objectes_detectats):
        
        if self._objectes == []:
            for i, new_object in enumerate(objectes_detectats):              
                id = len(self._id) + 1
                new_object._id = id
                
                self._ids.append(id)
                self._objectes.append(new_object)
        
        
        else:
            matriu_distancies = np.zeros(len(objectes_detectats), len(self._objectes))
            
            for i, objecte in enumerate(self._objectes):
                for j, objecte_candidat in enumerate(objectes_detectats):
                    matriu_distancies[i,j] = objecte.dist_euclidean(objecte_candidat)
            
            
            valor_maximo = matriu_distancies.sum()
            
            if len(self._objectes) <= len(objectes_detectats):
                for i in range (len(self._objectes)):
                    ix_objectes, ix_detactats = np.where(matriu_distancies == np.min(matriu_distancies))
                    self._objectes[ix_objectes]._centroide = objectes_detectats[ix_detactats]._centroide
                    
                    matriu_distancies[ix_objectes, :] = valor_maximo
                    matriu_distancies[:, ix_detactats] = valor_maximo
                    
                for i in range(len(objectes_detectats) - len(self._objectes) ):
                    ix_objectes, ix_detactats = np.where(matriu_distancies == np.min(matriu_distancies))
                    
                    new_object = objectes_detectats[ix_detactats]
                    id = len(self._ids) + 1
                    new_object._id = id
                    self._objectes.append(new_object)
                    self._ids.append(id)
                    
                    matriu_distancies[ix_objectes, :] = valor_maximo
                    matriu_distancies[:, ix_detactats] = valor_maximo
            
                
            
            
            


class objecte():
    
    def __init__(self, x, y, id):
        self._centroide = (x, y)
        self._id = id
        
    
    def dist_euclidean(self, altre_centroide):
        dist = (self._centroide[0] - altre_centroide[0]) ** 2 + (self._centroide[1] - altre_centroide[1]) ** 2
        return dist




