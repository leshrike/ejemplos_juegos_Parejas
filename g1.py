from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from functools import partial
from PySide6.QtSql import *
import sys
import random
from time import *

class Carta(QPushButton):
    def __init__(self,img):
        super().__init__()
        self.img=img
        self.mostrar=False
        self.timer=QTimer(self)

        self.setIcon(QIcon("carta.jpeg"))
        self.setIconSize(QSize(300,150))
        

    def cambiar(self):
        if not self.mostrar:
            self.setIcon(QIcon(self.img))
            self.mostrar=True
            self.timer.timeout.connect(self.esconder)
            self.timer.start(800)
            return self

    def mantener(self):
        self.timer.stop()
        self.setIcon(QIcon(self.img))
        self.mostrar=True

    def esconder(self):
        self.timer.stop()
        self.setIcon(QIcon("carta.jpeg"))
        self.mostrar=False

class Tablero(QMainWindow):
    def __init__(self):
        super().__init__()

        self.img1=Carta("")
        self.img2=Carta("")
        self.puntuacion=0
        self.label=QLabel("Puntuación: " + str(self.puntuacion))

        layout=QVBoxLayout()

        tablero=QGridLayout()

        imagen=["alcaraz.jpeg", "biden.jpeg", "channel.jpeg", "putin.jpeg", "reinaIsabel.jpeg", "tamara.jpeg", "willsmith.jpeg", "zelenski.jpeg","alcaraz.jpeg", "biden.jpeg", "channel.jpeg", "putin.jpeg", "reinaIsabel.jpeg", "tamara.jpeg", "willsmith.jpeg", "zelenski.jpeg"]

        for i in range(4):
            for x in range(4):
                num=random.randint(0,15)
                img=imagen[num]
                while (img == ""):
                    num=random.randint(0,15)
                    img=imagen[num]
                imagen[num] = ""

                boto=Carta(img)
                boto.clicked.connect(partial(self.cambiarBoto, boto))
                tablero.addWidget(boto,i,x)   

        layout.addLayout(tablero)
        layout.addWidget(self.label)

        contenedor=QWidget()
        contenedor.setLayout(layout)

        self.setCentralWidget(contenedor)    

    def cambiarBoto(self, boto):
        if not boto.mostrar:
            if self.img1.img=="":
                self.img1=boto.cambiar()
            else:
                self.img2=boto.cambiar()
                self.comprobar()

    def comprobar(self):
        if self.img1.img==self.img2.img:
            self.puntuacion+=1
            self.img1.mantener()
            self.img2.mantener()
        else:
            self.puntuacion-=1
        self.aumentarPuntuacion()
        self.img1=Carta("")
        self.img2=Carta("")
    
    def aumentarPuntuacion(self):
        self.label.setText("Puntuación: " + str(self.puntuacion))


if __name__ == "__main__":
    app=QApplication()
    tablero=Tablero()
    tablero.show()
    app.exec()