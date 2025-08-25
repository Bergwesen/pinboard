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

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            new_node = Node(key, value)
            new_node.next = self.table[index]
            self.table[index] = new_node
            self.size += 1

    def search(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(key)

    def remove(self, key):
        index = self._hash(key)

        previous = None
        current = self.table[index]

        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next

        raise KeyError(key)

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            self.search(key)
            return True
        except KeyError:
            return False


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
        self.windowstate = 0 #0 anfang, 1 pinboard 2 hinzufuegen
        self.checklist = os.listdir("bilder")
        self.imglist = [[]]
        self.flaglist = []
        self.addlist = a
        self.hashflag =  HashTable(10)
        self.imglistmanage()
        self.setWindowTitle('Pinboard/archive')
        self.setFixedSize(windowx,windowy)
        self.statechanger(self.windowstate)

    def hscreen(self) :
        self.alay= QHBoxLayout()
        self.abutton = QPushButton("Add",self)
        self.abutton.setCheckable(True)
        self.abutton.clicked.connect(lambda:self.statechanger(1))
        self.abutton.setFixedSize(200,200)
        self.bbutton = QPushButton("See",self)
        self.bbutton.setCheckable(True)
        self.bbutton.clicked.connect(lambda:self.statechanger(2))
        self.bbutton.setFixedSize(200,200)
        self.alay.addWidget(self.abutton)
        self.alay.addWidget(self.bbutton)
        print(self.windowstate)
        mains = QWidget()
        mains.setLayout(self.alay)
        self.setCentralWidget(mains )



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
            endbutton.clicked.connect(lambda:self.statechanger(0))
            res = addbutton.clicked.connect(lambda:self.diccollect(nameline.text(),adrline.text(),flagline.text(),notine.text(),bewertline.text()))
            if res != {} :
                print("valid")
            self.blay.addRow("Name",nameline) 
            self.blay.addRow("Adressse",adrline)
            self.blay.addRow("Flag",notine)
            self.blay.addRow("Notiz",flagline)
            self.blay.addRow("Bewertung",bewertline)
            self.blay.addRow(addbutton)
            self.blay.addRow(endbutton)
            addscreen.setLayout(self.blay)
            self.setCentralWidget(addscreen)

    def statechanger(self,number):
        self.windowstate = number
        self.windowswitch(self.windowstate)

    def flagfill(self,a):
        s = a.get("Flags").split()
        for x in s :
            self.hashflag.insert(x,a)
            if x not in self.flaglist :
                self.flaglist.append(x)

    def imglistmanage(self) :
        self.imglist = [[]]
        checked = []
        nextl = 0
        currents = 0
        for x in self.addlist :
            if x.get("Adresse") in self.checklist and x.get("Adresse") not in checked :
                checked.append(x.get("Adresse"))
                print(x.get("Adresse") + "Welcome" )
                if currents == gridsize*gridsize :
                    print("2")
                    self.flagfill(x)
                    nextl = nextl +1 
                    currents = 1
                    self.imglist.append([])
                    self.imglist[nextl].append(x)
                    print("2 " + str(len(self.imglist[nextl])))
                else : 
                    self.flagfill(x)
                    currents = currents +1
                    self.imglist[nextl].append(x)
                    print("1 " + str(len(self.imglist[nextl])))

        

    def pinboardscreen(self,seite):
        #self.cshecklist = os.listdir("bilder")
        print(self.checklist)
        self.imglistmanage()
        print(self.flaglist)
        seescreen = QWidget()
        pinlayout = QGridLayout()
        knoepfe = QHBoxLayout()
        if seite -1 >= 0 :
            prevpagebutton = QPushButton("Seite-1",self)
            prevpagebutton.setFixedSize(60,80)
            prevpagebutton.setCheckable(True)
            prevpagebutton.clicked.connect(lambda:self.pinboardscreen(seite-1))
        if seite +1 < len(self.imglist) :
            nextpagebutton = QPushButton("Seite+1",self)
            nextpagebutton.setFixedSize(60,80)
            nextpagebutton.setCheckable(True)
            nextpagebutton.clicked.connect(lambda:self.pinboardscreen(seite+1))
        returnbutton = QPushButton("Zurueck",self)
        returnbutton.setFixedSize(60,80)
        returnbutton.move(700,800)
        returnbutton.setCheckable(True)
        returnbutton.clicked.connect(lambda:self.statechanger(0))
       # print("row " + str(pinlayout.rowCount()))
        print("col " + str(pinlayout.columnCount()))


        for y in self.imglist :
            print(str(len(y)) + " size " )
       #eher schlechte version um ein gridlayout zu versichern  muss veraendert werden
        if len(self.imglist) % 2 != 0 :
            gridlen = len(self.imglist)+1
        else :
            gridlen = len(self.imglist)
        print("nich float  " + str(gridlen))
        
        gridx = int(np.sqrt(gridlen)) + 1
        gridy = int(np.sqrt(gridlen)) +1 
        print(str(gridx) + " und " +str(gridy) + " von " + str(gridlen))
        imgindex = 0

        gridx = gridsize
        gridy = gridsize
        for x in range(gridx):
            for y in range(gridy):
                # zuerst einen next page loesung coden
                if imgindex >= len(self.imglist[seite]) :
                    bildpfad =  ""
                else :
                    bildpfad =  "bilder/" + self.imglist[seite][imgindex].get("Adresse")
                    daten = self.imglist[seite][imgindex]

                bLabel= bildimage(bildpfad,gridx,daten)
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
        mainpinlayout.addLayout(pinlayout)
        knoepfe.addWidget(returnbutton)
        if seite -1 >= 0:
            knoepfe.addWidget(prevpagebutton)
        if seite +1 < len(self.imglist) :
            knoepfe.addWidget(nextpagebutton)
        mainpinlayout.addLayout(knoepfe)
        seescreen.setLayout(mainpinlayout)
        self.setCentralWidget(seescreen)

    def windowswitch(self,a):
        print("von " + str(a))
        if a == 1 :
            self.addscreen()
        elif a== 0 :
            self.hscreen()
        elif a == 2 : 
            self.pinboardscreen(0)
        print(self.windowstate)

    def diccreator(self,n: str,ad:str ,f: list,no: str,b: int):
        #add the inputs to a dict which will then be put in to json
        print(self.windowstate) 
        # f muss zu ner liste dafuer .split benutzen und noch in der vorherigen funktion woerter completer coden
        if n == "" or  len(n) == 0 :
            print("falsche Eingabe name")
            return {}
        elif f == [] or len(f)== 0 :
            print("falsche Eingabe  liste/flags")
            return {}
        elif no == "" or len(no) == 0 :
            print("falsche Eingabe  liste/flags")
            return {}
        elif   len(b) == 0 :
            print("falsche Eingabe bewertung")
            return {}
        res = { "Name" : n, "Adresse" : ad,"Flags": f, "Notizen": no,  "Bewertung" : b}
        return res


        return dict(name =n, flags = f,notes =no , bewertung = b)
    def diccollect(self,n:str,ad: str ,f: list,no: str,b: int):
        a = self.diccreator(n,ad,f,no,b)
        print(a)
        if a == {} :
            return
        else :
            self.addlist.append(a)
            print("added")





with open("data.json","r") as file :
    output= json.load(file)

print(output)




#weg ="/home/dumbon/Pictures"
#ls=os.listdir(weg)
with open("data.json") as file:
    jstestring = json.load(file)

#a = diccreator("test",[],"jo",1)
#print(a)


print(len(jstestring))
print(type(jstestring))
app = QApplication(sys.argv)
window = Startwindow(jstestring);
window.show()
app.exec()
print(window.windowstate)
print(window.addlist)

    #bzw nur wenn man neues hinzugfuegt wurde
with open("data.json","w") as file:
    json.dump(window.addlist,file)




