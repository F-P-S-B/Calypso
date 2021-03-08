from astropy.io import fits
from PIL import Image, ImageEnhance
import time
import tkinter as tk
from tkinter import filedialog
import pyfiglet
import threading

print(pyfiglet.figlet_format("Calypso", font = "cosmike"))
print("A Calamar Industries application")

image_first_element = str()
image_second_element = str()

def mainfunction(image_first, image_second):

    startTime=time.time()

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


    liste1=getDataFromFile(image_first)
    liste2=getDataFromFile(image_second)
    listeComparaison=[]

    count2=0
    count1=0
    for i in range(len(liste1)):
        arr=[]
        ssliste1=liste1[i]
        ssliste2=liste2[i]
        for j in range(len(ssliste1)):
            arr.append(ssliste1[j]/ssliste2[j])
            if ssliste1[j]>ssliste2[j]:
                count2+=1
            else: 
                count1+=1
        listeComparaison.append(arr)

    with open('comparaison.txt','w') as txt:
        txt.write("{}".format(listeComparaison))

    with open("fichier1.txt",'w') as txt:
        txt.write("{}".format(liste1))
        
    with open("fichier2.txt",'w') as txt:
        txt.write("{}".format(liste2))  
        
    print("Nombre de pixels avec l'oxygène majoritaire : {}".format(count2))
    print("Nombre de pixels avec l'hydrogène majoritaire : {}".format(count1))
    print("Ratio 1/total : {}%".format(100*count1/(count2+count1)))

    liste1Unique=[]
    liste2Unique=[]

    for i in range(2048):
        for j in range(2048):
            liste1Unique.append(liste1[i][j])
            liste2Unique.append(liste2[i][j])
    minListe1=min(liste1Unique)
    minListe2=min(liste2Unique)



    valeursRgb=[]
    print("Début création pixels")
    for i in range(2048*2048):
        tup=(  int(255*minListe2/liste2Unique[i]), 0, int(255*minListe1/liste1Unique[i])  )

        valeursRgb.append(tup)
        
    print("Fin création pixels")

    im= Image.new('RGB', (2048,2048))
    im.putdata(valeursRgb)
    enhancer = ImageEnhance.Contrast(im)
    imCont=enhancer.enhance(15)
    im.save('res.png')
    imCont.save('resCont.png')
    print("Temps d'exécution : ",time.time()-startTime)

# GUI

root = tk.Tk()
root.title("Calypso")
root.geometry("700x300")
# root.resizable(height="false",width="false")
root.configure(bg="#2f93ba")

def browseFiles(idk):
    if idk =="file1":
        global image_first_element
        image_first_element = filedialog.askopenfilename(initialdir = "/",title = "Select the first file",filetypes = (("FIT file",".fit"),("FITS file",".fits")))
        element1label.configure(text="File selected: "+image_first_element)
    else :
        global image_second_element
        image_second_element = filedialog.askopenfilename(initialdir = "/",title = "Select the first file",filetypes = (("FIT file",".fit"),("FITS file",".fits")))
        element2label.configure(text="File selected: "+image_second_element)


selectlabel= tk.LabelFrame(root, text="File Selection",bg="#2f93ba", font=("Helvetica", 12),relief="solid")
selectlabel.pack(fill="y")

element1button = tk.Button(selectlabel, text = "Select first file",font=("Helvetica", 12),command = lambda: browseFiles("file1")) 
element1button.grid(column = 0, row = 0)

element1label = tk.Label(selectlabel, text = "No file selected",font=("Helvetica", 12))
element1label.grid(column = 1, row = 0)

element2button = tk.Button(selectlabel, text = "Select second file",font=("Helvetica", 12),command = lambda: browseFiles("file2")) 
element2button.grid(column = 0, row = 1)

element2label = tk.Label(selectlabel, text = "No file selected",font=("Helvetica", 12))
element2label.grid(column = 1, row = 1)  

mainbutton = tk.Button(selectlabel, text = "Calculate",font=("Helvetica", 12), command = lambda: threading.Thread(target=mainfunction,args=(image_first_element,image_second_element)).start()) 
mainbutton.grid(column=0, row=2, columnspan= 2)

statlabel= tk.LabelFrame(root, text="Statistics",bg="#2f93ba", font=("Helvetica", 12),relief="solid")
statlabel.pack(fill="y")

pixel1label = tk.Label(statlabel, text="Number of pixel with a majority of element 1")
pixel1label.pack()

pixel2label = tk.Label(statlabel, text="Number of pixel with a majority of element 2")
pixel2label.pack()
root.mainloop()
