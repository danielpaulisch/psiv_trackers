import cv2 as cv
import os
import numpy as np





class Tracker():
    
    def __init__(self, objectes = [], ids = [], max_frame = 5):
        self._objectes = []
        self._ids = []
        self._max_frame = max_frame


    def deteccio(self, objectes_detectats):
        
        if self._objectes == []:
            for i, new_object in enumerate(objectes_detectats):              
                id = len(self._ids) + 1
                new_object._id = id
                
                self._ids.append(id)
                self._objectes.append(new_object)
        
        
        else:
            matriu_distancies = np.zeros( (len(self._objectes), len(objectes_detectats)))
            
            for i, objecte in enumerate(self._objectes):
                for j, objecte_candidat in enumerate(objectes_detectats):
                    matriu_distancies[i,j] = objecte.dist_euclidean(objecte_candidat)
            
            
            valor_maximo = matriu_distancies.sum()
            
            if len(self._objectes) <= len(objectes_detectats):
                for i in range (len(self._objectes)):
                    ix_objectes, ix_detactats = np.where(matriu_distancies == np.min(matriu_distancies))
                    ix_objectes, ix_detactats = ix_objectes[-1], ix_detactats[-1]
                    
                    
                    self._objectes[int(ix_objectes)]._centroide = objectes_detectats[int(ix_detactats)]._centroide
                    self._objectes[int(ix_objectes)]._no_esta = 0
                    
                    matriu_distancies[ix_objectes, :] = valor_maximo
                    matriu_distancies[:, ix_detactats] = valor_maximo
                    
                for i in range(len(objectes_detectats) - len(self._objectes) ):
                    ix_objectes, ix_detactats = np.where(matriu_distancies == np.min(matriu_distancies))
                    
                    new_object = objectes_detectats[int(ix_detactats[-1])]
                    id = len(self._ids) + 1
                    new_object._id = id
                    self._objectes.append(new_object)
                    self._ids.append(id)
                    
                    
                    matriu_distancies[ix_objectes, :] = valor_maximo
                    matriu_distancies[:, ix_detactats] = valor_maximo
                
            
            
            elif len(objectes_detectats) == 0:
                for ob in self._objectes:
                    ob._no_esta += 1
                    if ob._no_esta > self._max_frame:
                        self._objectes.remove(ob)
            
            else:
                for i in range (len(objectes_detectats)):
                    ix_objectes, ix_detactats = np.where(matriu_distancies == np.min(matriu_distancies))
                    ix_objectes, ix_detactats = ix_objectes[-1], ix_detactats[-1]
                    
                    self._objectes[int(ix_objectes)]._centroide = objectes_detectats[int(ix_detactats)]._centroide
                    
                    self._objectes[int(ix_objectes)]._no_esta = 0
                    
                    matriu_distancies[ix_objectes, :] = valor_maximo
                    matriu_distancies[:, ix_detactats] = valor_maximo
                    
                
                for i in range(len(self._objectes) - len(objectes_detectats)):
                    ix_objectes, ix_detactats = np.where(matriu_distancies == np.min(matriu_distancies))
                    
                    
                    
                    if ix_objectes[-1] >= len(objectes_detectats):
                        index_ob = int(ix_objectes[0])
                        
                    else:
                        index_ob  = int(ix_objectes[-1])
                    
                    ob = objectes_detectats[index_ob]
                    ob._no_esta += 1
                    
                    if ob._no_esta > self._max_frame:
                        self._objectes.remove(ob)
                        
                    
                    
                    matriu_distancies[ix_objectes, :] = valor_maximo
                    matriu_distancies[:, ix_detactats] = valor_maximo
                    
                    
                    
                
                       

class Contador():
    def __init__(self, y = 0) :
        self._y = y
        self._sobre = []
        self._per_sota = []
        self._contat = []
        self._contar_baixa = 0
        self._contar_puja = 0
        self._frame_baixa = []
        self._frame_puja = []
        
    
    def contar(self, centroide, nom, frame):
        y_actual = centroide[1]
        
        if nom not in self._contat:
            
            if nom in self._per_sota and self._y > y_actual:
                self._contar_puja += 1
                print('puja:', self._contar_puja, frame)
                self._frame_puja.append(frame)
                self._contat.append(nom)
                
            if nom in self._sobre and self._y < y_actual:
                self._contar_baixa += 1
                print('baiax:', self._contar_baixa, frame)
                self._frame_baixa.append(frame)
                self._contat.append(nom)
            
            if  nom not in self._per_sota and nom not in self._sobre:
                if self._y  > y_actual:
                    
                    self._sobre.append(nom)
                else:
                    self._per_sota.append(nom)
                    
                    
                    
                    
                    
class Objecte():
    
    def __init__(self, centroide = (0,0), id = None):
        self._centroide = centroide
        self._id = id
        self._no_esta = 0
        
        
    
    def dist_euclidean(self, altre_centroide):
        dist = (self._centroide[0] - altre_centroide._centroide[0]) ** 2 + (self._centroide[1] - altre_centroide._centroide[1]) ** 2
        return dist




tracking = Tracker()



capture = cv.VideoCapture('output5.mp4')
fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

tracking = Tracker()
linia = 240
conut = Contador(linia)
num_frame = 0

while ( capture.isOpened()):
    num_frame += 1
    ret, frame = capture.read()
    if (ret == False): break
    
    
    altura, ancho, _ = frame.shape
    
    
    roi = frame[500:, :550]
    
    
    fgmaskMOG = fgbg.apply(roi)
     
    tratada = cv.dilate(fgmaskMOG, np.ones((3,3)), iterations=8)
    tratada = cv.morphologyEx(tratada,cv.MORPH_OPEN, np.ones((30,30)))
    
    
    
    #detectar objeto
    objetetos_detectados = []
    contours, _ = cv.findContours(tratada, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 7000 and area < 35000: 
            
        #Calculate area remove small elements (personas/motos)
            #cv.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv.boundingRect(cnt)
            
            if 0.6 < w/h and   w/h < 1.5:
                cv.rectangle(roi, (x,y), (x + w, y + h), (0, 255, 0), 3)
                
                centroide = (int(x + w/2) ,int(y + h/2))
                
                objecte = Objecte(centroide)
                objetetos_detectados.append(objecte)
            
            tracking.deteccio(objetetos_detectados)
            
            for ob in tracking._objectes:
                
                conut.contar(centroide = ob._centroide, nom =ob._id, frame = num_frame)
                
                cv.putText(roi, str(ob._id), ob._centroide, cv.FONT_HERSHEY_SIMPLEX, 0.5, (2255, 255, 0) )
            
    
    cv.line(roi, (0,linia), (99999, linia) , (0,0,255), 10 )
    cv.imshow('roi', roi)
    cv.imshow('MOG', tratada)
    cv.imshow('frame', frame)
    
    
    if cv.waitKey(1) == ord('q'):
            break
    

capture.release()
cv.destroyAllWindows()