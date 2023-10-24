# SEGUIMENT D'OBJECTES (TRACKER)

## INTRODUCCIÓ

El seguiment d'objectes (tracking) en la visió artificial representa una tasca de gran rellevància. Sobretot en aplicacions de processament d'imatges, encarregades d'analitzar el flux de vídeo provinent de càmeres.

El tracking es basa en el monitoratge continu d'elements, com ara, persones, cotxes, motos, en imatges, o seqüència d'imatges en moviment.El monitoratge també pot emprar-se a temps real. 

El procés del tracking és el següent:
Primer és diferenciar l'objecte que detectarem, tenint en compte outliers com ara, variabilitat d'il·luminació, canvis de fons, i distraccions d'aquest, ambigüitat, obstacles en la seqüència...
Un cop ja tenim controlades totes les dificultats que es presenten, fem un seguiment precís i fiable.En el nostre cas, per dur a terme el repte, farem un seguiment i monitoratge dels cotxes que estan en moviment en una seqüència de frames, és a dir, un vídeo.

Addicionalment, examinarem detalladament l'ús del seguiment d'objectes amb la biblioteca OpenCV, ja que és l'eina que més s'utilitza en aquests casos, gràcies a l'eficiència i efectivitat que mostra.Per altra banda, OpenCV també posa a les nostres mans, trackers ja implementats i integrats com ara, OOSTING, MIL, KCF, CSRT, MedianFlow, TLD, MOSSE i GOTURN.

## OBJECTES

L'objectiu d'aquest repte és saber quants cotxes es mouen en cada un dels carrils d'entrada i de sortida, és a dir, fer un comptador dels cotxes que pugen i baixen. Fer un programa com aquest fa que puguem monitorar i controlar el flux de sortida i d'entrada i el grau d'ocupació del pàrquing.

## DISTRIBUCIÓ

El GitHub l'hem distribuït de la següent manera:
- directori vídeos: conté el vídeo en el qual vam fer proves.
- tracker1.py: fitxer Python que conté el codi final del programa tracker.


## BASE DE DADES

La base de dades que hem utilitzat ha estat un vídeo que l'hem extret del Campus Virtual. Específicament el vídeo "Seqüència Short".


## PROCEDIMENT

### DETECCIÓ COTXES

Aquesta part del codi és la primera que es fa i està al principi del codi principal, no està inclòs en cap classe.
Primer de tot comencem fent una subtracció del fons del vídeo, amb la funció createBackgroundSubtractorMOG de la lliberira cv2, ja que és una funció bastant eficaç i senzilla que es basa en mescles gaussianes.
Específicament apliquem la funció createBackgroundSubtractorMOG, per a cada frame.
Un cop hem tret el fons reduim l'àrea dels frames, és a dir, tallem la imatge per tal de quedar-nos amb l'entrada i la sortida del pàrquing, per això acabem tallant tota la part de dalt del vídeo i deixant la part final per sota del pas de zebra del final.

Seguidament, apliquem les funcions morfològiques dilate de la llibreria cv2, aquí, un element de píxel és '1' si almenys un píxel sota el nucli és '1'. Per tant, augmenta la regió blanca a la imatge o augmenta la mida de l'objecte en primer pla.

Una altra funció que utilitzem és la morphologyEx, aquesta es basa a aplicar l'erosió seguida de dilatació. És útil per eliminar el soroll que queda.

Un cop hem acabat d'aplicar les funcions morfològiques a tots els frames i ens queden els cotxes en moviment com una taca blanca i el fons negre, apliquem la funció de la llibreria cv2 findContour(), aquesta ajuda a extraure els contorns d'aquestes taques.

Per cada contorn detectat, mirem la seva àrea, i sempre que sigui més gran a 4000, el tenim en compte, ja que l'etiquetem com a cotxe. En cas que sigui més petita l'àrea vol dir que estem detectant alguna moto o alguna persona i en aquest cas no ens interessa, així doncs el descartem.

Finalment per facilitar la visualització hem dibuixat uns rectangles que envoltenels cotxes, per tal de graficar millor el tracking dels automòbils.
Per rectangular els cotxes només hem hagut d'afegir una condició, la relació amplada i llargada ha d'estar entre 0,6 i 1,5, no inclosos.



### COMPTADOR ENTRADA I SORTIDA PÀRQUING

Aquesta part l'hem separat en classes. Primerament hem fet la classe Objecte, on cada instància representa un cotxe de l'escena. 
Per cada instància d'objecte, té inicialitzat un centroide, l'identificador i una etiqueta per saber si està o no a l'escena. Aquesta classe té la funcionalitat de calcular la distància euclidiana entre el cetroide de l'objecte actual amb el centroide que se li passa per paràmetre. 
Que la utilitzarem més endavant a la classe Tracker, per trobar els centroides i trackejar el cotxe en els diferents frames. 

Un cop acabada la classe Objecte, creem la classe Tracker; aquesta s'encarrega de fer el procés de tracking del programa. 
Aquest codi defineix una classe anomenada `Tracker`. Aquí hi ha un resum dels seus components:
El tracker conté una llista d'objectes, que serà un conjunt de instàncies de la classe Objecte que faran referència als cotxes de l'escena, una llista d'identificadors dels cotxes i max_frame que fa referència al número màxim de frames que es necessita per tal de desvincular l'identificador d'un cotxe, ja que aquest no està en el frame actual.
Aquesta classe té una funcionalitat, la de detecció, que pren com a paràmetre objectes_detectats i fa el seguiment d'aquesta objectes. 
Primer mira si hi ha objectes, en cas que no s'hi hagi s'assigna un identificador a cada objecte detectat i s'afegeix a la llista; en cas que hi hagi objectes a la llista calcula una matriu de distàncies amb la distància euclidiana entre els objectes existents i els detectats, i es fa una assignació dels objectes detectats al existents o en crea un de nou si no en troba. 
Si no es detecten objectes, es posa com a 1 l'etiqueta de la classe Objecte i s'elimina els objectes que s'hagin excedit el límit de max_frame. 
En cas que hi hagin més objectes existents que objectes detectats, s'assigenen els objectes detectats als objectes existents segons el criteri de distàncies mínimes; i si hi ha més objectes detectats que existents, s'assignen els objectes existents als objectes detectats segons el mateix criteri i s'eliminen els objectes que s'han passat el límit de max_frame. 

Per últim hem creat la classe Contador

## RESULTATS

He pogut detectar tots els cotxes sense cap anomalia i abordant tots els possibles outliers.
També hem fet el comptador sense cap problema, concretament hi ha __ cotxes que entren al pàrquing i __ cotxes que en surten.

La comprovació la volíem haver fet amb una intel·ligència artificial, no obstant això, vam acabar decidint fer-ho de manera manual, ja que el vídeo no era molt llarg.

## CONCLUSIÓ

Com bé ja hem comentat abans a l'apartat de resultats, no hi ha hagut cap problema per fer aquest repte, en comparació amb el repte passat.
La detecció dels cotxes l'hem fet sense cap problema i la part de detecció també.
Només hem tingut un problema que és la part de la subtracció del fonns, ja que si es para passa a formar part del fons i s'elimina, no obstant això ene l nostre cas això no suposa un problema.
