from astropy.io import fits
from PIL import Image, ImageEnhance
import time

startTime=time.time()

imageH=input("Entrez l'image d'hydrogène: ")
imageOx=input("Entrez l'image d'oxygène: ")

def getDataFromFile(file):
    with fits.open(file) as file:
        file.verify('fix')
        data=file[0].data
        parsedData=[]
        for elt in data:
            arr=[]
            for elt2 in elt:
                arr.append(elt2)
            parsedData.append(arr)
    return parsedData


listeH=getDataFromFile(imageH)
listeO=getDataFromFile(imageOx)
listeComparaison=[]

countO=0
countH=0
for i in range(len(listeH)):
    arr=[]
    sslisteH=listeH[i]
    sslisteO=listeO[i]
    for j in range(len(sslisteH)):
        arr.append(sslisteH[j]/sslisteO[j])
        if sslisteH[j]>sslisteO[j]:
            countO+=1
        else: 
            countH+=1
    listeComparaison.append(arr)

with open('comparaison.txt','w') as txt:
    txt.write("{}".format(listeComparaison))

with open("fichier1.txt",'w') as txt:
    txt.write("{}".format(listeH))
    
with open("fichier2.txt",'w') as txt:
    txt.write("{}".format(listeO))  
    
print("Nombre de pixels avec l'oxygène majoritaire : {}".format(countO))
print("Nombre de pixels avec l'hydrogène majoritaire : {}".format(countH))
print("Ratio H/total : {}%".format(100*countH/(countO+countH)))

listeHUnique=[]
listeOUnique=[]

print("Début boucle")
for i in range(2048):
    for j in range(2048):
        listeHUnique.append(listeH[i][j])
        listeOUnique.append(listeO[i][j])
print("Fin boucle")
minListeH=min(listeHUnique)
minListeO=min(listeOUnique)



valeursRgb=[]
print("Début création pixels")
for i in range(2048*2048):
    tup=(  int(255*minListeO/listeOUnique[i]), 0, int(255*minListeH/listeHUnique[i])  )

    valeursRgb.append(tup)
    
print("Fin création pixels")

im= Image.new('RGB', (2048,2048))
im.putdata(valeursRgb)
enhancer = ImageEnhance.Contrast(im)
imCont=enhancer.enhance(15)
im.save('res.png')
imCont.save('resCont.png')
print("Temps d'exécution : ",time.time()-startTime)