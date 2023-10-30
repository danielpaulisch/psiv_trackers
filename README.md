# SEGUIMENT D'OBJECTES (TRACKER)

## INTRODUCCIÓ

El seguiment d'objectes (tracking) en la visió artificial representa una tasca de gran rellevància. Sobretot en aplicacions de processament d'imatges, encarregades d'analitzar el flux de vídeo provinent de càmeres.

El tracking es basa en el monitoratge continu d'elements, com ara, persones, cotxes, motos, en imatges, o seqüència d'imatges en moviment.El monitoratge també pot emprar-se a temps real. 

El procés del tracking és el següent:
Primer és diferenciar l'objecte que detectarem, tenint en compte outliers com ara, variabilitat d'il·luminació, canvis de fons, i distraccions d'aquest, ambigüitat, obstacles en la seqüència...
Un cop ja tenim controlades totes les dificultats que es presenten, fem un seguiment precís i fiable.En el nostre cas, per dur a terme el repte, farem un seguiment i monitoratge dels cotxes que estan en moviment en una seqüència de frames, és a dir, un vídeo.

Addicionalment, examinarem detalladament l'ús del seguiment d'objectes amb la biblioteca OpenCV, ja que és l'eina que més s'utilitza en aquests casos, gràcies a l'eficiència i efectivitat que mostra.Per altra banda, OpenCV també posa a les nostres mans, trackers ja implementats i integrats com ara, OOSTING, MIL, KCF, CSRT, MedianFlow, TLD, MOSSE i GOTURN.

## OBJECTIUS

L'objectiu d'aquest repte és saber quants cotxes es mouen en cada un dels carrils d'entrada i de sortida, és a dir, fer un comptador dels cotxes que pugen i baixen. Fer un programa com aquest fa que puguem monitorar i controlar el flux de sortida i d'entrada i el grau d'ocupació del pàrquing.

## DISTRIBUCIÓ

El GitHub l'hem distribuït de la següent manera:
- directori vídeos: conté el vídeo en el qual vam fer proves.
- tracker.py: fitxer Python que conté el codi final del programa tracker.
- proves.ipynb: fitxer Jupyter que conté els resultats reals de tots els vídeos i que serveix per fer la validació
- outputX resultados.txt: els 5 fixters que són txt són fixters text que contenen els resultats reals de cada vídeo.


## BASE DE DADES

La base de dades que hem utilitzat han estat uns vídeos que els hem extret del Campus Virtual. Específicament el vídeo "Seqüència Short",  "Seqüència middle",  "Seqüència shadow",  "Seqüència long 1" i  "Seqüència long 2".
Els hem separat en Train i Test. 
Com a Train hem utilitzat "Seqüència Short" i "Seqüència shadow" i com a Test la resta. 


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

Aquesta part l'hem separat en classes. Primerament, hem fet la classe Objecte, on cada instància representa un cotxe de l'escena.
Per cada instància d'objecte, té inicialitzat un centroide, l'identificador i una etiqueta per saber si està o no a l'escena. Aquesta classe té la funcionalitat de calcular la distància euclidiana entre el centroide de l'objecte actual amb el centroide que se li passa per paràmetre.
Que la utilitzarem més endavant a la classe Tracker, per trobar els centroides i trackejar el cotxe en els diferents frames.

Un cop acabada la classe Objecte, creem la classe Tracker; aquesta s'encarrega de fer el procés de tracking del programa.
El tracker conté una llista d'objectes, que serà un conjunt de instàncies de la classe Objecte que faran referència als cotxes de l'escena, una llista d'identificadors dels cotxes i max_frame que fa referència al número màxim de frames que es necessita per tal de desvincular l'identificador d'un cotxe, ja que aquest no està en el frame actual.
Aquesta classe té una funcionalitat, la de detecció, que pren com a paràmetre objectes_detectats i fa el seguiment d'aquests objectes.
Primer mira si hi ha objectes, en cas que no n'hi hagi s'assigna un identificador a cada objecte detectat i s'afegeix a la llista; en cas que hi hagi objectes a la llista calcula una matriu de distàncies amb la distància euclidiana entre els objectes existents i els detectats, i es fa una assignació dels objectes detectats als existents o en crea un de nou si no en troba.
Si no es detecten objectes, es posa com a 1 l'etiqueta de la classe Objecte i s'elimina els objectes que s'hagin excedit el límit de max_frame.
En cas que hi hagi més objectes existents que objectes detectats, s'assignen els objectes detectats als objectes existents segons el criteri de distàncies mínimes; i si hi ha més objectes detectats que existents, s'assignen els objectes existents als objectes detectats segons el mateix criteri i s'eliminen els objectes que s'han passat el límit de max_frame.

Finalment, hem creat la classe Contador que s'encarrega de fer el comptatge dels cotxes que entren i surten del pàrquing.
Aquesta classe conté l'atribut _y que fa referència al centroide de la classe Objecte, _sobre i _sota són llistes que contenen els identificadors dels cotxes que està per sobre o per sota de la línia que hem creat per separar entre els cotxes que pugen i baixen, _contat una llista que fa referència als cotxes que s'han comptat i per últim _contar_baixa i _contar_puja que són comptadors dels cotxes que entre i surten del pàrquing.
Aquesta classe té una funcionalitat, "contar", que rep com a paràmetres centroide i nom. Primer valida que nom no estigui a la llista de _contat, en cas que es compleixi, mirem si nom està a la llista _per_sota i el valor de _y sigui major al valor de y del centroide, si es compleix aquesta condició augmentem el comptador _contar_puja i s'afegeix com a comptat aquest objecte.
Si el nom està a la llista _sobre i el valor de y és més petit que el valor de y del centroide, augmentem el comptador de _contar_baixa i s'afegeix com a comptat aquest objecte.
Per acabar, si nom no està a les llistes _per_sota i _sobre comparem el valor de y amb el de y del centroide i s'afegeix a la llista de _sobre si _y és major que y del centroide i, per consegüent, si _y és més petit que la y del centroide s'afegeix a la llista _per_sota.



## RESULTATS

### PROVES

El fitxer proves.ipynb agafa els resultats de l'execució i un groundtruth manual, compara aquests i imprimeix mesures de com de bons són els resultats.

En el propi fitxer trobem el groundtruth, la veritat sobre la qual validem el nostre programa. Consisteix en cinc variables tipus llista amb tuples que contenen el temps mínim de detecció, el temps màxim de detecció i si el cotxe puja o baixa.

Aquest groundtruth l'hem creat manualment seguint els següents criteris:

-Les motos no les contem.

-Hi ha un marge de temps entre 5 i 10 segons.

-Només contem els que passin per sota del pas de vianants.

-Furgonetes i camions les contem, però parlem d'elles com cotxes.

Després d'aquestes variables trobem una funció que ens passa frames a temps en format int. Això podria ser un problema però degut a que només fem comparacions i mai restem ni sumem aquest "error" de format no ens perjudica (de fet facilita molt les coses).
Seguidament, tenim la part del codi que canviem en base al vídeo que volem que ens validi. Llegim d'un arxiu .txt el resultat del codi comptador de cotxes i el posem en format semblant al del groundtruth.
Per últim, tenim la part del codi que compara. Primer mira quants pugen i quants baixen per totes dues llistes, i després mira quantes de les deteccions es troben realment en el vídeo segons el groundtruth. A partir d'aquí treu les estadístiques, aquestes són:

*trobats*: percentatge de cotxes reals que el codi ha aconseguit detectar.

*n_trobats*: nombre de cotxes reals que el codi ha aconseguit detectar.

*n_fantasmes*: nombre de cotxes detectats que el codi s'ha inventat (no es troben al groundtruth).

*fantasmes*: percentatge de cotxes detectats que el codi s'ha inventat.

*diferència*: la diferència entre el nombre de cotxes que el codi es pensa que hi ha al pàrquing i el nombre de cotxes que realment hi ha. Si la variable és positiva vol dir que el nombre de cotxes dintre del pàrquing és menor al detectat. Si es negativa vol dir que el nombre de cotxes dintre del pàrquing és major al detectat. Busquem per tant en aquesta variable el 0.


Un cop hem comprovat els nostres resultats amb el script de proves.ipynb hem obtingut els següents resultats.

#### output2: seqüencia middle
- detectat: 3 que pugen i  8 que baixen 
- real:     5 que pugen i  7 que baixen
- trobats:   0.8333333333333334
- n_trobats:   10  cotxes detectats en el vídeo
- n_fantasmes: 1 cotxe inventat
- fantasmes: 0.09090909090909091 
- hi ha 3 de cotxes de més respecte la ocupació real


#### output3: seqüencia shadow
- detectat: 3 que pugen i 10 que baixen
- real:     3 que pugen i 10 que baixen
- trobats:   1.0
- n_trobats:   13 cotxes detectats en el vídeo
- n_fantasmes: 0
- fantasmes: 0.0
- Aquest cas és perfecte



#### output5: seqüencia long 1
- detectat: 19 que pugen i 56 que baixen
- real:     11 que pugen i 25 que baixen
- trobats:   0.8611111111111112
- n_trobats:   31 cotxes detectats en el vídeo
- n_fantasmes: 44 cotxes inventats
- fantasmes: 0.5866666666666667
- hi ha 23 de cotxes respecte la ocupació real


#### output6: sequencia long 2
- detectat: 10 que pugen i 133 que baixen
- real:     9 pugen i 138 que baixen
- trobats:   0.9183673469387755
- n_trobats:   135 cotxes detectats en el vídeo
- n_fantasmes: 8 cotxes inventats
- fantasmes: 0.055944055944055944
- hi ha 6 cotxes menys respecte l'ocupacio real  


#### output7: seqüencia short
- detectat: 6 que pugen i 2 que baixen 
- real:     6 que pugen i 2 que baixen
- trobats:   1.0
- n_trobats:   8  cotxes detectats en el vídeo
- n_fantasmes: 0  cotxes inventats
- fantasmes: 0.0
- Aquest cas és perfecte

Seqüència short: hi ha 2 cotxes que entren al pàrquing i 6 cotxes que en surten.

Seqüència middle: hi ha 8 cotxes que entren al pàrquing i 3 cotxes que en surten.

Seqüència shadow: hi ha 10 cotxes que entren al pàrquing i 3 cotxes que en surten.

Seqüència long 1: hi ha 56 cotxes que entren al pàrquing i 19 cotxes que en surten.

Seqüència long 2: hi ha 133 cotxes que entren al pàrquing i 10 cotxes que en surten.

Hem pogut abordar la majoria d'anomalies i outliers possibles en tots els vídeos, però hi ha casos que no sempre van del tot bé.

La comprovació la volíem haver fet amb una intel·ligència artificial, no obstant això, vam acabar decidint fer-ho de manera manual, ja que els vídeos no són massa llargs i se'ns era més fàcil.


## CONCLUSIÓ


Després de la comprovació que hem fet, hem pogut corrobar que els resultats la majoria són correctes i el programa és bastant robust, ja que funciona correctament amb la majoria de casos. 
No obstant això, hi ha hagut alguns problemes a l'hora de fer el repte, el primer punt a destacar seria el tema del camions molt grans, ja que com que ocupen tota l'escena i es van movent i es van parant, els detecta com si fossin molts cotxes
Per altra banda tenim el problema de substitució, en el que quan un cotxe que baixa desapareix de l'escena i apareix un que puja, el nostre progrma ael detecta com el mateix. 
Aquesta problema només passa un cop. 
