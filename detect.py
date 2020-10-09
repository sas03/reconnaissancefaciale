#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dlib
import cv2
from imutils import face_utils
from threading import Thread
#import threading
import os
import shutil
import time 
import glob
from os.path import basename, splitext
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from PIL import  Image,ImageTk


# In[2]:


####################################################
###                 classes                    #####
####################################################

class CIndex:
    def __init__(self,i):
        self.id=i
        pass
    def UpdateId(self):
        self.id+=1
    def setId(self,i):
        self.id=self.id+i


class CSave:
    
    def __init__(self):
        self.counter = 1
        
    def InitFil(self,FileName):
        os.mkdir(self.path+FileName)
        
        
class CTxt:
    
    def __init__(self,path,FileName):
        self.path =path
        self.FileName = FileName
        
    def __init__(self,FileName):
        self.path="" 
        self.FileName = FileName
        
    def SaveTxt (self,Id):
        f = open(self.path+self.FileName, 'w')
        f.write(str(Id))
        f.close()
        
    def ReadTxt (self):
        f = open(self.path+self.FileName, 'r')
        a = int(f.read())
        f.close()
        return a
    
    
class CSaveCsv(CSave):
    
    def __init__ (self,path,FileLastID):
        CSave.__init__(self)
        self.DataFile=""
        self.path=path
        self.ID = CTxt(FileLastID)
        
    def CsvExist(self):
        return (self.ID.ReadTxt())
    def SaveLastID(self,id):
        self.ID.SaveTxt(id)       
       
    def CreateFileCsv (self,Label='Data',entetes = ['Id','Nom','Prenom','Age','Niveau','Classe']):
        self.DataFile = self.path+Label+'.csv'
        f = open(self.DataFile, 'a')
        ligneEntete = ";".join(entetes) + "\n"
        f.write(ligneEntete)
        f.close()
        print("Le fichier de donnee a ete cree")
        
    def AddDataCsv(self,data):
       
        if (len(self.DataFile)==0):
            valeurs = [data['Id'],data['Nom'], data['Prenom'], data['Age'], data['Niveau'], data['Classe']]
            filepath = glob.glob(self.path+'*.csv')[0]
            DataFile = self.path+splitext(basename(filepath))[0]+'.csv'
            f = open(DataFile, 'a')
            ligne = ";".join(valeurs) + "\n"
            f.write(ligne)
            f.close()
            self.Label = data['Id']
            print("les donnees sont ajoutees")
        else:
            valeurs = [data['Id'],data['Nom'], data['Prenom'], data['Age'], data['Niveau'], data['Classe']]
            f = open(self.DataFile, 'a')
            ligne = ";".join(valeurs) + "\n"
            f.write(ligne)
            f.close()
            self.Label = data['Id']
            print("les donnees sont ajoutees")
            
class CSavePicture(CSave):
    def __init__(self,path):
        CSave.__init__(self)
        self.path=path
        
    def SaveImageSq(self,frame,v,Lab):
        LabIm = Lab+"_"+str(self.counter)
        cv2.imwrite(self.path+LabIm+".jpg",frame[v[2]:v[2]+v[4],v[1]:v[1] + v[3]])
        print (LabIm)
        self.counter +=1
        
    def SaveImageCam(self,frame,Lab):
        LabIm = Lab+"_"+str(self.counter)
        cv2.imwrite(self.path+LabIm+".jpg",frame)
        print (LabIm)
        self.counter +=1
            

class Camera:
    
    def __init__(self):
        print("creation de la camera")
        self.cap = cv2.VideoCapture(0)
  
    def CaptureFrame(self):
        self.ret, self.frame = self.cap.read()
        if self.ret==False:
            print("verifier votre camera")
        else: 
            return self.frame
        
    def Display(self,title='Video Capture'):
        cv2.imshow(title,self.frame)
        
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        

class Detection: 
    
    def __init__(self):
        print("creation de l'objet detection")
        self.detector = dlib.get_frontal_face_detector()
        pass
    
    def LoadPredictor(self,data): 
        self.predictor = dlib.shape_predictor(data)
        
    def DetectFaces(self,frame):
        self.vect=[]
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.detector(self.gray, 1)
        for (i, rect) in enumerate(self.rects):
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if (i==0):
                self.vect = [x,y,w,h]
                
    def DetectFace(self,frame):
        self.vect=[]
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.detector(self.gray, 1)
        if (len(self.rects) !=0):
            (x, y, w, h) = face_utils.rect_to_bb(self.rects[0])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            self.vect = [1,x,y,w,h]
        else:
            cv2.putText(frame, 'Visage non reconnu',(200,200) ,cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 255, 0))
            self.vect = [0]
            
    def Detectlandmarks(self,frame,dots_size=5):
        self.vect=[]
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.detector(self.gray, 1)
        for (i, rect) in enumerate(self.rects):
            shape = self.predictor(self.gray, rect)
            shape = face_utils.shape_to_np(shape)
            for (x, y) in shape:
                cv2.circle(frame, (x, y), dots_size, (0, 255, 0), -1)
            if (i==0):
                self.vect = [x,y,w,h]
                
    def DetectlandmarksRectrectangle(self,frame,dots_size=5):
        self.vect=[]
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.detector(self.gray, 1)
        for (i, rect) in enumerate(self.rects):
            shape = self.predictor(self.gray, rect)
            shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            for (x, y) in shape:
                cv2.circle(frame, (x, y), dots_size, (0, 255, 0), -1)
            if (i==0):
                self.vect = [x,y,w,h]
     


# # Interface

# In[3]:


####################################################
###  fonctions pour l interface graphique     #####
####################################################

def click_btn_precedent(cam):
    listeWidgets = window.place_slaves()
    del cam
    FileCsv.SaveLastID(id.id)
    for i in listeWidgets:
            i.destroy()
    btn_Treat_a_new_case.pack(pady=90)
    
    
def click_btn_Add_image(frame,v):
    
    if (v[0]==1):
        Lab = FileCsv.Label
        SaveIm.SaveImageSq(frame,v,Lab)
    
        
              
def click_btn_AddNC(var_nom,var_prenom,var_age,var_NE,var_Classe,ent_nom,ent_prenom,ent_age,ent_NE,ent_Classe) :

    print(id.id)
    PersonalData["Id"] = "Id_"+str(id.id)
    PersonalData["Nom"]  = var_nom.get()
    PersonalData["Prenom"] = var_prenom.get()
    PersonalData["Age"] = var_age.get()
    PersonalData["Niveau"] = var_NE.get()
    PersonalData["Classe"] = var_Classe.get()
    FileCsv.AddDataCsv(PersonalData)

    FileCsv.InitFil(PersonalData["Id"])
    global SaveIm
    id.UpdateId()
    SaveIm = CSavePicture("Data/"+PersonalData["Id"]+"/")
    ent_nom.delete(0,END)
    ent_prenom.delete(0,END)
    ent_age.delete(0,END)
    ent_NE.delete(0,END)
    ent_Classe.delete(0,END)


def StratCam(cam):
    frame = cam.CaptureFrame()
    frame = cv2.resize(frame, (530,400),cv2.INTER_AREA)
    det.DetectFace(frame)
    v=det.vect
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)

    imgtk = ImageTk.PhotoImage(image=img)
    lb_img.imgtk = imgtk
    lb_img.configure(image=imgtk)
    
    btn_startcam = tk.Button(window, text = "Add image", command = lambda:click_btn_Add_image(frame,v))
    btn_startcam.place(x=290, y=455)
    
    lb_img.after(21, lambda: StratCam(cam))
    
    
def Processes(cam):
    btn_create_new_database.pack_forget()
    global FileCsv
    global PersonalData
    
    FileCsv = CSaveCsv("Data/","Id.txt")
    id_ = FileCsv.CsvExist()

    if (id_ == 1):
        FileCsv.CreateFileCsv("DataEcole")
    
    id.setId(id_)

    PersonalData = {}
                
    lb_nom=tk.Label(window,text="Nom:", )
    lb_nom.place(x=10,y=20)
    var_nom=tk.StringVar()
    ent_nom = tk.Entry(window, textvariable=var_nom )
    ent_nom.place(x=100, y=20)
        
            
    lb_prenom = tk.Label(window, text="Prénom: ")
    lb_prenom.place(x=10, y=50)
    var_prenom = tk.StringVar()
    ent_prenom = tk.Entry(window, textvariable=var_prenom )
    ent_prenom.place(x=100, y=50)
       
            
            
            
    lb_age = tk.Label(window, text="Age : ")
    lb_age.place(x=10, y=80)
    var_age = tk.StringVar()
    ent_age = tk.Entry(window, textvariable=var_age )
    ent_age.place(x=100, y=80)
        
            
            
    lb_NE = tk.Label(window, text="Niveau d'etude :")
    lb_NE.place(x=10, y=110)
    var_NE = tk.StringVar()
    ent_NE= tk.Entry(window, textvariable=var_NE )
    ent_NE.place(x=100, y=110)
        
        
    lb_Classe = tk.Label(window, text="Classe :")
    lb_Classe.place(x=10, y=140)
    var_Classe = tk.StringVar()
    ent_Classe = tk.Entry(window, textvariable=var_Classe )
    ent_Classe.place(x=100, y=140)
        
        
        
        
    btn_Ajouter = tk.Button(window, text = "Add",
                            command = lambda:click_btn_AddNC(var_nom,var_prenom,
                                                             var_age,var_NE,var_Classe,ent_nom,
                                                             ent_prenom,ent_age,ent_NE,ent_Classe))
    btn_Ajouter.place(x=100, y=170)
             
    btn_precedent = tk.Button(window, text = "Precedent", command = lambda : click_btn_precedent(cam))
    btn_precedent.place(x=200, y=455)


# In[4]:


def click_btn_create_new_database():
    """ptn creation d'une nouvelle base """
   
    btn_create_new_database.pack_forget()
    btn_add_to_existing_dataset.pack_forget()
    ID = CTxt("Id.txt")
    ID.SaveTxt(1)
    if(os.path.exists("Data_old")):
        shutil.rmtree("Data_old")
    os.rename("Data", "Data_old")
    os.mkdir("Data")
   
    cam= Camera()
    Processes(cam)
    
    global lb_img 
    lb_img = tk.Label(window)
    lb_img.place(x=250, y=20)
    StratCam(cam)

def click_btn_add_to_existing_dataset():
    """ptn add data to existing dataset """
    btn_create_new_database.pack_forget()
    btn_add_to_existing_dataset.pack_forget() 
    cam= Camera()
    Processes(cam)
    global lb_img 
    lb_img = tk.Label(window)
    lb_img.place(x=250, y=20)
    StratCam(cam)


def click_btn_Treat_a_new_case():
    """ptn Treat a new case """
    global btn_create_new_database
    global btn_add_to_existing_dataset
    window.configure(bg="SystemButtonFace")
    
    window.title('Treat a new case')

    btn_Treat_a_new_case.pack_forget()
    
    btn_create_new_database = tk.Button(text='create a new database',bg='#808080', bd=3,width=30,
                                        font=('arial',10), command=click_btn_create_new_database)
    
    btn_add_to_existing_dataset = tk.Button(text='add data to existing dataset',bg='#808080', bd=3,width=30, 
                                            font=('arial',10),command=click_btn_add_to_existing_dataset)
    
    btn_create_new_database.pack()
    btn_add_to_existing_dataset.pack()


# # Programme principal interface

# In[5]:


####################################################
###  Programme principal pour l'interface      #####
####################################################

window = tk.Tk()
window.geometry('800x500+270+100')
window.title("Identify Absent Students")
window.resizable(False,False)
window.iconbitmap('icone.ico')
id = CIndex(0)
det = Detection()
det.LoadPredictor('shape_predictor_68_face_landmarks.dat')

btn_Treat_a_new_case=tk.Button(window,text='Treat a new case',
                    bg='#808080',
                    bd=3,width=30,
                    font=('arial',10),
                    command=click_btn_Treat_a_new_case)
btn_Treat_a_new_case.pack(pady=90)



window.mainloop()


# In[12]:





# # Programme principal sans passer par l'interface graphique 

# In[3]:


##################################################################################
###  Programme principal sans interface "dépendant juste des classes "       #####
##################################################################################

print("Voulez-vous ajouter : \n")
print("Des données au dataset existant : oui sinon non")

while(True):
    rep = input()
    if (rep.lower()=="non"):
        ID = CTxt("Id.txt")
        ID.SaveTxt(1)
        if(os.path.exists("Data_old")):
            shutil.rmtree("Data_old")
        os.rename("Data", "Data_old")
        os.mkdir("Data")
        break
    elif (rep.lower()=="oui"):
        break
    else: 
        print("Exemple d'usage : oui/non..")


FileCsv = CSaveCsv("Data/","Id.txt")
id = FileCsv.CsvExist()
if (id == 1):
    FileCsv.CreateFileCsv("DataEcole")
    
cam = Camera()
det = Detection()
det.LoadPredictor('shape_predictor_68_face_landmarks.dat')

while(True):
    print("Voulez-vous ajouter un nouvel étudiant ? oui/non :")
    rep =input()

    if (rep.lower()=="oui"):
        
        PersonalData = {}
        print("Entrez les données de l'etudiant :")
        PersonalData["Id"] = "Id_"+str(id)
        PersonalData["Nom"] = input("Nom :") 
        PersonalData["Prenom"] = input("Prenom :")
        PersonalData["Age"] = input("Age :")
        PersonalData["Niveau"] = input("Niveau d'etude :")
        PersonalData["Classe"] = input("Classe :")
        
        FileCsv.AddDataCsv(PersonalData)

        FileCsv.InitFil(PersonalData["Id"])
        
        SaveIm = CSavePicture("Data/"+PersonalData["Id"]+"/")
       
        while(True):
            frame = cam.CaptureFrame()
            det.DetectFace(frame)
            v=det.vect
            cam.Display()
            key = cv2.waitKey(10)
            if key & 0xFF == ord('q'):
                break
            if (key & 0xFF == ord('w') and v[0]==1):
                Lab = FileCsv.Label
                SaveIm.SaveImageSq(frame,v,Lab)
        id+=1
    elif(rep.lower()=="non"):
        print("Fin.")
        break
    else:
        print("Exemple d'usage : oui/non..")

del cam

FileCsv.SaveLastID(id)




# 

# In[5]:





# In[14]:





# In[12]:





# In[10]:




