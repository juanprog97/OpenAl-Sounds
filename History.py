# -*- coding: utf-8 -*-
from openal import *
import time
# Form implementation generated from reading ui file 'History.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

global answer ,historia

situaciones = [("Despertarse","Te despiertas, que vas hacer despues?",["Ducharse","Desayunar","Cepillarse"],"./sound/1-amanecer.wav")
               ,("Salir de casa","Sales de la casa y decides:",["Ir a la estacion","Tomar un taxi","Caminar"],"./sound/1-amanecer.wav"),
               ("Afuera del casino","Estas afuera del casino.",[],"./sound/1-amanecer.wav"),
               ("Entrar al casino","Entras al casino que vas hacer:",["Jugar traga monedas","Pedir bebida","Salir"],"./sound/1-amanecer.wav"),
               ("Ir a casa","como te vas a ir a tu casa:",["Ir a la estacion de buses","Pedir un taxi","Ir caminando"],"./sound/1-amanecer.wav"),
               ("fin","Termino el juego",[],"./sound/4-cepillarse.wav"),
               ("Abrir Puerta","Llegas a tu casa y procedes a:",["Dormir"],"./sound/1-amanecer.wav")
              ]
decisiones = [("Ducharse","./sound/2-ducharse.wav","Salir de casa"),
              ("Desayunar","./sound/3-desayuno.wav","Salir de casa"),
              ("Cepillarse","./sound/4-cepillarse.wav","Salir de casa"),
              ("Ir a la estacion","./sound/5-irEstacion.wav","Afuera del casino"),
              ("Tomar un taxi","./sound/6-Taxi.wav","Afuera del casino"),
              ("Caminar","./sound/7-caminar.wav","Afuera del casino"),
              ("Jugar traga monedas","./sound/4-cepillarse.wav","fin"),
              ("Pedir bebida","./sound/4-cepillarse.wav","fin"),
              ("Salir","./sound/4-cepillarse.wav","Ir a casa"),
              ("Esperar en una parada de buses","./sound/5-irEstacion.wav","Abrir Puerta"),
              ("Pedir un taxi","./sound/6-Taxi.wav","Abrir Puerta"),
              ("Ir caminando","./sound/7-caminar.wav","Abrir Puerta"),
              ("Dormir","./sound/4-cepillarse.wav","fin")
              ]

def cargarHistoria():
    global answer, historia
    historia = GrafoDeHistoria()

    #Agregar Vertices
    for i in situaciones:
        situacion = nodoGrafoSituacion(i[0])
        situacion.comentario(i[1])
        for x in i[2]:situacion.agregarDecision(x)
        situacion.agregarSonido(i[3])
        historia.agregarVertice(i[0])
        historia.agregarArco(i[0],situacion)
    for j in decisiones:
        decision = nodoGrafoDecision(j[0])
        decision.agregarSonido(j[1])
        historia.agregarVertice(j[0])
        historia.agregarArco(j[0],decision)
    #Relacionar Vertices

    for i in situaciones:
        for j in i[2]:
            nodo = historia.conseguirArco(i[0])
            nodo.append(j)
    for k in decisiones:
        nodo = historia.conseguirArco(k[0])
        nodo.append(k[2])




    #Importar los sonidos-------------------------------------

    #---------------------------------------------------------

class GrafoDeHistoria:
    def __init__(self):
        self.grafo = {}
    def agregarVertice(self,vertice):
        self.grafo[vertice] = []
    def eliminarVertice(self, vertice):
        try:
            self.grafo.pop(vertice)
        except KeyError:
            print("Error")
    def esVertice(self, vertice):
        try:
            self.grafo[vertice]
            return True
        except KeyError:
            return False

    def agregarArco(self, vertice, arco):
        try:
            self.grafo[vertice].append(arco)
        except KeyError:
            print("Error")

    def eliminarArco(self, vertice, arco):
        try:
            self.grafo[vertice].remove(arco)
        except KeyError:
            print("Error")
        except ValueError:
            print("Error")

    def conseguirArco(self, vertice):
        try:
            return self.grafo[vertice]
        except KeyError:
            print("Error")
    def __str__(self):
        return "grafo{0}".format(self.grafo)


class nodoGrafoSituacion:
    def __init__(self,nom):
        self.nombre = nom
        self.comentario
        self.decisiones= []
        self.Nm = ['A)','B)','C)','D)']
        self.audio =""
        self.bloq = [True,True,True,True]
        self.nodoHoja = False
    def comentario(self,comentarioSituacion):
        self.comentario = comentarioSituacion
    def agregarDecision(self,decision):
        self.decisiones.append(decision)
    def nodoFinal(self):
        self.nodoHoja = True
    def nombre(self):
        return self.nombre
    def decision(self):
        return self.decisiones
    def agregarSonido(self,sonido):
        self.audio= sonido
    def reproducirSonido(self):
        try:
            source = oalOpen(self.audio)
            source.play()
            while source.get_state() == AL_PLAYING:
                   ui.label_2.setEnabled(True)
                   time.sleep(0)

            ui.label_2.setEnabled(False)
            oalQuit()
        except KeyError:
            print("Error")
    def expoUi(self):
        dec = ""
        for i in range(len(self.decisiones)):
            dec += self.Nm[i] + self.decisiones[i]+".\n"
        print(dec)
        ui.label.setText(self.comentario+"\n\n"+dec)
        if(len(self.decisiones)!=0):
            for i in range(4):
                if(i<len(self.decisiones)):
                    self.bloq[i] = True
                else:
                    self.bloq[i] = False
            ui.pushButton.setEnabled(self.bloq[0])
            ui.pushButton_2.setEnabled(self.bloq[1])
            ui.pushButton_3.setEnabled(self.bloq[2])
            ui.pushButton_4.setEnabled(self.bloq[3])
            ui.pushButton_5.setEnabled(False)
        else:
            ui.pushButton.setEnabled(False)
            ui.pushButton_2.setEnabled(False)
            ui.pushButton_3.setEnabled(False)
            ui.pushButton_4.setEnabled(False)
            ui.pushButton_5.setEnabled(True)



class nodoGrafoDecision:
    def __init__(self,nom):
        self.nombre = nom
        self.audio = ""
    def agregarSonido(self,sonido):
        self.audio= sonido
    def nombre(self):
        return self.nombre
    def reproducirSonido(self):
        try:
            source = oalOpen(self.audio)
            source.play()
            while source.get_state() == AL_PLAYING:
                   ui.label_2.setEnabled(True)
                   time.sleep(0)

            ui.label_2.setEnabled(False)
            oalQuit()
        except KeyError:
            print("Error")



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(454, 346)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 30, 231, 281))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(0, 20, 4000, 101))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setEnabled(False)
        self.label_2.setGeometry(QtCore.QRect(320, 230, 51, 41))
        self.label_2.setMaximumSize(QtCore.QSize(10000000, 16777215))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("epa.jpg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(260, 80, 191, 78))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(310, 180, 80, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(330, 60, 57, 15))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Message:"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton.setText(_translate("MainWindow", "A"))
        self.pushButton_2.setText(_translate("MainWindow", "B"))
        self.pushButton_3.setText(_translate("MainWindow", "C"))
        self.pushButton_4.setText(_translate("MainWindow", "D"))
        self.pushButton_5.setText(_translate("MainWindow", "Continuar"))
        self.label_3.setText(_translate("MainWindow", "Opcion:"))

def botonA():
    global answer, historia,nodoActual
    answer = 1
    deci = nodoActual[answer]
    nodoActual = historia.conseguirArco(deci)
    nodoActual[0].reproducirSonido()
    update(nodoActual[1])
def botonB():
    global answer, historia, nodoActual
    answer = 2
    deci = nodoActual[answer]
    nodoActual = historia.conseguirArco(deci)
    nodoActual[0].reproducirSonido()
    update(nodoActual[1])
def botonC():
    global answer, historia,nodoActual
    answer = 3
    deci = nodoActual[answer]
    nodoActual = historia.conseguirArco(deci)
    nodoActual[0].reproducirSonido()
    update(nodoActual[1])
def botonD():
    global answer, historia,nodoActual
    answer = 4
    deci = nodoActual.decision()
    nodoActual = historia.conseguirArco(deci[answer])
    nodoActual[0].reproducirSonido()
    update(nodoActual[1])
def continuar():
    global answer, historia, nodoActual
    answer = ''
    deci = nodoActual.decision()
    nodoActual = historia.conseguirArco(deci[answer])
    update(nodoActual[1])


def update(name):
    global answer, historia, nodoActual
    nodoActual = historia.conseguirArco(name)
    nodoActual[0].reproducirSonido()
    nodoActual[0].expoUi()



if __name__ == "__main__":
    import sys
    global answer, historia
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.pushButton.clicked.connect(botonA)
    ui.pushButton_2.clicked.connect(botonB)
    ui.pushButton_3.clicked.connect(botonC)
    ui.pushButton_4.clicked.connect(botonD)

    ##Seccion se llena el arbol con la historia
    cargarHistoria()
    update("Despertarse")


    #while Historia.end() != True:


    sys.exit(app.exec_())
