from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
import os
import json
import numpy as np


windowx = 800
windowy = 800
gridsize = 3




class bildimage(QLabel):
    def __init__(self,a,b,c):
        super().__init__()
        self.pfad = a
        self.breite = b
        self.daten = c
        self.setScaledContents(True)
        self.bild = QPixmap(self.pfad).scaledToHeight(int(windowy/self.breite))
        self.setPixmap(self.bild)
        self.buttontoggle = 1


    def mousePressEvent(self,e):
        if e.buttons() :
            if self.buttontoggle == 1 :
                x = self.frameGeometry().width()
                y = self.frameGeometry().height()
                self.setFixedSize(x,y)
                if self.pfad != "" :
                    self.setText("Name : " + self.daten.get("Name") +"\n"+
                    "Adresse : " + self.daten.get("Adresse") + "\n" +
                    "Flag : " + self.daten.get("Flags") + "\n" +
                    "Notiz : " + self.daten.get("Notizen") + "\n" +
                    "Bewertung : " + self.daten.get("Notizen") + "\n")
                self.buttontoggle = 0
            else :
                self.buttontogle = 1
                self.setScaledContents(True)
                self.bild = QPixmap(self.pfad).scaledToHeight(int(windowy/self.breite))
                self.setPixmap(self.bild)
                self.buttontoggle = 1
                









class Startwindow(QMainWindow):

#QCOMPLETER UM TAGS ZU VERVOLLSTAENDIGEN


    def __init__(self,a):
        super().__init__() #was macht diese zeile
        self.windowstate = 0
        self.checklist = os.listdir("bilder")
        self.imglist = [[]]
        self.flaglist = {}
        self.flaginput = ""
        self.flags = []
        if a == "[]":
            self.addlist = []
        else :
            self.addlist = a
        self.imglistmanage()
        self.setWindowTitle('Pinboard/archive')
        self.setFixedSize(windowx,windowy)
        self.statechanger(self.windowstate,-1)

    #Anfangsbildschirm
    def hscreen(self) :
        self.alay= QHBoxLayout()
        self.abutton = QPushButton("Add",self)
        self.abutton.setCheckable(True)
        self.abutton.clicked.connect(lambda:self.statechanger(1,0))
        self.abutton.setFixedSize(200,200)
        self.bbutton = QPushButton("See",self)
        self.bbutton.setCheckable(True)
        self.bbutton.clicked.connect(lambda:self.statechanger(2,0))
        self.bbutton.setFixedSize(200,200)
        self.alay.addWidget(self.abutton)
        self.alay.addWidget(self.bbutton)
        #print(self.windowstate)
        mains = QWidget()
        mains.setLayout(self.alay)
        self.setCentralWidget(mains )


    #Bildschirm zum hinzufuegen von Bildern
    def addscreen(self):
            #Eingabe / Addscreen
            self.windowstate = 1
            addscreen = QWidget()
            self.blay = QFormLayout()
            nameline = QLineEdit(self)
            adrline = QLineEdit(self)
            adrcomplete = QCompleter(self.checklist)
            adrline.setCompleter(adrcomplete)
            # es so aendern sodass man alle flags angezeigt bekommt
            flagline = QLineEdit(self)
            notine = QLineEdit(self)
            bewertline = QLineEdit(self)
            addbutton = QPushButton("Einfuegen",self)
            addbutton.setCheckable(True)
            endbutton = QPushButton("Zurueck",self)
            endbutton.setCheckable(True)
            endbutton.clicked.connect(lambda:self.statechanger(0,1))
            res = addbutton.clicked.connect(lambda:self.diccollect(nameline.text(),adrline.text(),flagline.text(),notine.text(),bewertline.text()))
          #  if res != {} :
          #      print("valid")
            self.blay.addRow("Name",nameline) 
            self.blay.addRow("Adressse",adrline)
            self.blay.addRow("Flag",notine)
            self.blay.addRow("Notiz",flagline)
            self.blay.addRow("Bewertung",bewertline)
            self.blay.addRow(addbutton)
            self.blay.addRow(endbutton)
            addscreen.setLayout(self.blay)
            self.setCentralWidget(addscreen)

    #Funktion zum wechseln des Bildschirmstatus, Bildschirmstatus = welcher Bildschirm es ist
    def statechanger(self,zu,von):
        if von == 1 :
            self.imglistmanage()
        self.windowstate = zu
        self.windowswitch(self.windowstate)

    #fuellt die Flag liste mit den gewuenschten Flags auf und aktualisiert das Bild
    def flagsearch(self,lineinput:str):
        self.flags = []
        self.flaginput = lineinput.split()
        for x in self.flaginput :
            if  x in list(self.flaglist.keys()) :
                self.flags.append(x)
        self.pinboardscreen(0,self.flags)
       # print(self.flags)




    #Dictionary,welches die Bilder nach Flags sortiert
    def flagfill(self,a):
        s = a.get("Flags").split()
        for x in s :
            if x  in self.flaglist :
                if a not in self.flaglist[x] :
                    self.flaglist[x].append(a)
            else :
                self.flaglist[x] = [a]

    #Imglist beinhaltet die Json Informationen der Bilder und wird zum darstellen der Bilder benutzt
    def imglistmanage(self) :
        self.imglist = [[]]
        checked = []
        nextl = 0
        currents = 0
        for x in self.addlist :
            if x.get("Adresse") in self.checklist and x.get("Adresse") not in checked :
                checked.append(x.get("Adresse"))
#                print(x.get("Adresse") + "Welcome" )
                if currents == gridsize*gridsize :
#                    print("2")
                    self.flagfill(x)
                    nextl = nextl +1 
                    currents = 1
                    self.imglist.append([])
                    self.imglist[nextl].append(x)
#                    print("2 " + str(len(self.imglist[nextl])))
                else : 
                    self.flagfill(x)
                    currents = currents +1
                    self.imglist[nextl].append(x)
#                    print("1 " + str(len(self.imglist[nextl])))

        
    #Pinboard Bildschirm
    def pinboardscreen(self,seite,flags):
        #self.cshecklist = os.listdir("bilder")
        #print(self.checklist)
        self.imglistmanage()
#        print("asdf\n")
#        print(self.flaglist["11"])
#        print("asdf\n")
#
        seescreen = QWidget()
        pinlayout = QGridLayout()
        knoepfe = QHBoxLayout()
        flagfelder = QHBoxLayout()
        if seite -1 >= 0 :
            prevpagebutton = QPushButton("Seite-1",self)
            prevpagebutton.setFixedSize(60,80)
            prevpagebutton.setCheckable(True)
            prevpagebutton.clicked.connect(lambda:self.pinboardscreen(seite-1,[]))
        if seite +1 < len(self.imglist) :
            nextpagebutton = QPushButton("Seite+1",self)
            nextpagebutton.setFixedSize(60,80)
            nextpagebutton.setCheckable(True)
            nextpagebutton.clicked.connect(lambda:self.pinboardscreen(seite+1,[]))
        returnbutton = QPushButton("Zurueck",self)
        returnbutton.setFixedSize(60,80)
        returnbutton.move(700,800)
        returnbutton.setCheckable(True)
        returnbutton.clicked.connect(lambda:self.statechanger(0,2))
#        print("col " + str(pinlayout.columnCount()))

        if flags != [] :
            print("jo")
            self.imglist = [[]]
            count= 0
            seitenzahl = 0
            for x in flags :
                if count == gridsize*gridsize:
                    count = 0
                    seitenzahl += 1
                    self.imglist.append([])
                    self.imglist[seitenzahl] += self.flaglist[x]
                else :
                    count += 1
                    self.imglist[seitenzahl] += self.flaglist[x]



        if len(self.imglist) % 2 != 0 :
            gridlen = len(self.imglist)+1
        else :
            gridlen = len(self.imglist)
#        print("nich float  " + str(gridlen))
        
        gridx = int(np.sqrt(gridlen)) + 1
        gridy = int(np.sqrt(gridlen)) +1 
#        print(str(gridx) + " und " +str(gridy) + " von " + str(gridlen))
        imgindex = 0

        gridx = gridsize
        gridy = gridsize
        for x in range(gridx):
            for y in range(gridy):
                # zuerst einen next page loesung coden
                if imgindex >= len(self.imglist[seite]) :
                    bLabel  = QLabel() 


                else :
                    bildpfad =  "bilder/" + self.imglist[seite][imgindex].get("Adresse")
                    daten = self.imglist[seite][imgindex]
                    bLabel= bildimage(bildpfad,gridx,daten)

                #bLabel= bildimage(bildpfad,gridx,daten)
               # bLabel =  QLabel(self)
               # bLabel.setScaledContents(True)
               # bmap = QPixmap(bildpfad).scaledToHeight(int(windowy/gridx))
                #bmap = bildimage(bildpfad).scaledToHeight(int(windowy/gridx))
                imgindex = imgindex +1 
               # bmap = QPixmap(bildpfad).scaledToHeight(int(windowy/gridx))
                #bmap = bildimage(bildpfad).scaledToHeight(int(windowy/gridx))
               # bLabel.setPixmap(bmap)
                pinlayout.addWidget(bLabel,x+1,y)
          
        mainpinlayout = QVBoxLayout()
        flageeingabe = QLineEdit(self)
        flagbutton = QPushButton("Suche",self)
        flagbutton.clicked.connect(lambda:self.flagsearch(flageeingabe.text()))
        flagfelder.addWidget(flageeingabe)
        flagfelder.addWidget(flagbutton)
        mainpinlayout.addLayout(flagfelder)
        mainpinlayout.addLayout(pinlayout)
        knoepfe.addWidget(returnbutton)
        if seite -1 >= 0:
            knoepfe.addWidget(prevpagebutton)
        if seite +1 < len(self.imglist) :
            knoepfe.addWidget(nextpagebutton)
        mainpinlayout.addLayout(knoepfe)
        seescreen.setLayout(mainpinlayout)
        self.setCentralWidget(seescreen)


    #Funktion zum wechseln zwischen den Bildschirmen
    def windowswitch(self,a):
        #print("von " + str(a))
        if a == 1 :
            self.addscreen()
        elif a== 0 :
            self.hscreen()
        elif a == 2 : 
            self.pinboardscreen(0,[])
#        print(self.windowstate)

    #Json Datei Informationen werden in eine Dictionary gepackt
    def diccreator(self,n: str,ad:str ,f: str,no: str,b: int):
        if n == "" or  len(n) == 0 :
            print("falsche Eingabe name")
            return {}
        #elif f == [] or len(f)== 0 :
        #    print("falsche Eingabe  liste/flags")
        #    return {}
        #elif no == "" or len(no) == 0 :
        #    print("falsche Eingabe  liste/flags")
        #    return {}
      #  elif   len(str(b)) == 0 :
      #      print("falsche Eingabe bewertung")
      #      return {}
        res = { "Name" : n, "Adresse" : ad,"Flags": f, "Notizen": no,  "Bewertung" : b}
        return res


        return dict(name =n, flags = f,notes =no , bewertung = b)

    #Wenn ein neues Bild erstellt wird,diese Funktion durchgefuehrt, sie erstellen das Dictionary und fuegt es zur addliste hinzu
    def diccollect(self,n:str,ad: str ,f: str,no: str,b: int):
        a = self.diccreator(n,ad,f,no,b)
        #print(a)
        if a == {} :
            return
        else :
            self.addlist.append(a)
            #print("added")








try :
    f = open('data.json')
except FileNotFoundError:
    f = open('data.json','w')
    with f:
        f.write("[]")
    jstestring = "[]"
else :
    with f:
        jstestring = json.load(f)



app = QApplication(sys.argv)
window = Startwindow(jstestring);
window.show()
app.exec()

#bzw nur wenn man neues hinzugfuegt wurde
with open("data.json","w") as file:
    json.dump(window.addlist,file)




