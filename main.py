from astropy.io import fits
from PIL import Image, ImageEnhance
import time
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import pyfiglet
import threading
import os

print(pyfiglet.figlet_format("Calypso", font = "cosmike"))
print("A Calamar Industries application")

image_first_element = str()
image_second_element = str()

def mainfunction(image_first, image_second):
    
    progress['value'] = 10
    root.update_idletasks()
    statlabel.configure(text="State : Analyzing")
    startTime=time.time()

    progress['value'] = 20
    root.update_idletasks()
    statlabel.configure(text="State : Decomposing .fits or .fit")
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
    progress['value'] = 30
    root.update_idletasks()
    statlabel.configure(text="State : Comparing pixels values between both files")
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

    pixel1label.configure(text="Number of pixel with a majority of element 1 : {}".format(count1))
    pixel2label.configure(text="Number of pixel with a majority of element 2 : {}".format(count2))
    tempslabel.configure(text="Processing time : {} seconds".format(round(time.time()-startTime,2)))
    element1ratio.configure(text="Ratio of element 1 : {}%".format(round(100*count1/(count2+count1),5)))
    element2ratio.configure(text="Ratio of element 2 : {}%".format(round(100*count2/(count2+count1),5)))

    progress['value'] = 40
    root.update_idletasks()
    statlabel.configure(text="State : Saving .txt")
    with open('comparaison.txt','w') as txt:
        txt.write("{}".format(listeComparaison))

    with open("fichier1.txt",'w') as txt:
        txt.write("{}".format(liste1))
        
    with open("fichier2.txt",'w') as txt:
        txt.write("{}".format(liste2))        

    liste1Unique=[]
    liste2Unique=[]
    progress['value'] = 50
    statlabel.configure(text="State : Creating list")
    root.update_idletasks()
    
    for i in range(2048):
        for j in range(2048):
            liste1Unique.append(liste1[i][j])
            liste2Unique.append(liste2[i][j])
    minListe1=min(liste1Unique)
    minListe2=min(liste2Unique)

    valeursRgb=[]
    progress['value'] = 60
    root.update_idletasks()
    statlabel.configure(text="State : Creating images ...")
    for i in range(2048*2048):
        tup=(  int(255*minListe2/liste2Unique[i]), 0, int(255*minListe1/liste1Unique[i])  )

        valeursRgb.append(tup)

    im= Image.new('RGB', (2048,2048))
    im.putdata(valeursRgb)
    enhancer = ImageEnhance.Contrast(im)
    imCont=enhancer.enhance(15)
    
    progress['value'] = 90
    root.update_idletasks()
    statlabel.configure(text="State : Saving")
    im.save('res.png')
    imCont.save('resCont.png')
    
    os.system("start res.png")
    os.system("start resCont.png")

    
    progress['value'] = 100
    root.update_idletasks()
    statlabel.configure(text="State : Ended")

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
        element1label.configure(text="File selected: "+image_first_element,bg="#2f93ba", font=("Helvetica", 12))
    else :
        global image_second_element
        image_second_element = filedialog.askopenfilename(initialdir = "/",title = "Select the first file",filetypes = (("FIT file",".fit"),("FITS file",".fits")))
        element2label.configure(text="File selected: "+image_second_element,bg="#2f93ba", font=("Helvetica", 12))


selectlabel= tk.LabelFrame(root, text="File Selection",bg="#2f93ba", font=("Helvetica", 12),relief="solid")
selectlabel.pack(ipadx=10,ipady=5)

element1button = tk.Button(selectlabel, text = "Select first file",font=("Helvetica", 12),command = lambda: browseFiles("file1"),bg="#2f93ba", width=15) 
element1button.grid(column = 0, row = 0)

element1label = tk.Label(selectlabel, text = "No file selected",font=("Helvetica", 12),bg="#2f93ba")
element1label.grid(column = 1, row = 0)

element2button = tk.Button(selectlabel, text = "Select second file",font=("Helvetica", 12),command = lambda: browseFiles("file2"),bg="#2f93ba",width=15) 
element2button.grid(column = 0, row = 1)

element2label = tk.Label(selectlabel, text = "No file selected",font=("Helvetica", 12),bg="#2f93ba")
element2label.grid(column = 1, row = 1)  

mainbutton = tk.Button(selectlabel, text = "Calculate",bg="#2f93ba",font=("Helvetica", 12), command = lambda: threading.Thread(target=mainfunction,args=(image_first_element,image_second_element)).start()) 
mainbutton.grid(column=0, row=2, columnspan= 2)

statlabel= tk.LabelFrame(root, text="Statistics",bg="#2f93ba", font=("Helvetica", 12),relief="solid")
statlabel.pack(ipadx=5,ipady=5)

pixel1label = tk.Label(statlabel, text="Number of pixel with a majority of element 1 :",bg="#2f93ba", font=("Helvetica", 12))
pixel1label.pack()

pixel2label = tk.Label(statlabel, text="Number of pixel with a majority of element 2 :",bg="#2f93ba", font=("Helvetica", 12))
pixel2label.pack()

element1ratio = tk.Label(statlabel, text="Ratio of element 1 :",bg="#2f93ba", font=("Helvetica", 12))
element1ratio.pack()

element2ratio = tk.Label(statlabel, text="Ratio of element 2 :",bg="#2f93ba", font=("Helvetica", 12))
element2ratio.pack()

tempslabel = tk.Label(statlabel, text="Executing time :",bg="#2f93ba", font=("Helvetica", 12))
tempslabel.pack()

statlabel = tk.Label(statlabel, text="State :",bg="#2f93ba", font=("Helvetica", 12))
statlabel.pack()

progress = Progressbar(statlabel, orient = tk.HORIZONTAL, 
            length = 250, mode = 'determinate')
progress.pack()

root.mainloop()
