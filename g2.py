

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from functools import partial
from PySide6.QtSql import *
import os, random, time

directorio = os.path.dirname(__file__)

class Carta(QPushButton):
    def __init__(self, carta, numero):
        super().__init__()
        self.carta = carta
        self.numero = numero
        self.base = QPixmap(directorio+"/img/base.png")
        self.real = QPixmap(directorio+"/img/"+carta)
                
        self.foto = QIcon(self.base)
        self.setIcon(self.foto)
        self.setIconSize(QSize(175, 175))
        self.girado = False
        
    
    def girar(self):
        self.girado = not self.girado
        if(self.girado):
            print("girado")
            self.setIcon(QIcon(self.real))
        else:
            print("vuelta")
            self.setIcon(QIcon(self.base))
    
    def deshabilitar(self):
        self.setDisabled(True)

        self.setIconSize(QSize(175, 175))
        
                

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.acertados = 0
        self.intentos = 10
        self.cartas = QGridLayout()
        self.posiblesCartas = ["foto1.jpg","foto2.jpg","foto3.jpg","foto4.jpg","foto5.jpg","foto6.jpg","foto7.jfif","foto8.jpg", "foto1.jpg","foto2.jpg","foto3.jpg","foto4.jpg","foto5.jpg","foto6.jpg","foto7.jfif","foto8.jpg"]
        random.shuffle(self.posiblesCartas)
        c = 0
        for i in range(4):
            for j in range(4):
                carta = Carta(self.posiblesCartas[c], c)
                carta.clicked.connect(partial(self.pulsar, carta))
                self.cartas.addWidget(carta, i, j)
                c = c + 1
        
        vertical = QVBoxLayout()
        self.qLabelAcertados = QLabel("Acertados: " + str(self.acertados), self)
        self.qLabelIntentos = QLabel("Intentos: " + str(self.intentos), self)
        self.qLabelAcertados.setStyleSheet("color:green;")
        self.qLabelIntentos.setStyleSheet("color:red;")
        
        vertical.addWidget(self.qLabelAcertados)
        vertical.addWidget(self.qLabelIntentos)
        vertical.addLayout(self.cartas)
        
        contenedor = QWidget()
        contenedor.setLayout(vertical)   
        self.setCentralWidget(contenedor)
        self.carta1 = None
        self.carta2 = None
                
    def pulsar(self, carta):
        carta.girar()
        if self.carta1==None:
            self.carta1 = carta
            self.carta1.setEnabled(False)
        elif(self.carta2==None):
            self.carta2 = carta
            self.carta2.setEnabled(False)
            if self.carta1.numero  == self.carta2.numero:
                self.carta2 = None
            elif self.carta1.carta == self.carta2.carta:
                self.carta1.setEnabled(False)
                self.carta2.setEnabled(False)
                self.carta1 = None
                self.carta2 = None
                print("IGUAL")
                self.acertados = self.acertados + 1
                self.qLabelAcertados.setText("Acertados: " + str(self.acertados))
            else:
                QTimer.singleShot(1000, self.carta1.girar)
                QTimer.singleShot(1000, self.carta2.girar)
                self.carta1.setEnabled(True)
                self.carta2.setEnabled(True)
                self.carta1 = None
                self.carta2 = None
                self.intentos = self.intentos - 1
                self.qLabelIntentos.setText("Intentos: " + str(self.intentos))
        else:
            self.carta1.setEnabled(True)
            self.carta2.setEnabled(True)
            self.carta1 = None
            self.carta2 = None
            carta.girar()
        
        if(self.acertados==8):
            print("Has ganado")
            resultado = QMessageBox.information(self, "Terminado", "HAS GANADO")
            self.deshabilitarTablero()
            resultado.Abort
            
        if(self.intentos==0):
            print("SIN INTENTOS")
            resultado = QMessageBox.critical(self, "Error", "Has agotado todos los intentos")
            self.deshabilitarTablero()
            resultado.Abort
    
    def deshabilitarTablero(self):
        for i in range(self.cartas.count()):
            carta = self.cartas.itemAt(i).widget()
            carta.setDisabled(True)
    
if __name__ == "__main__":
    app=QApplication()
    ventana = Principal()
    ventana.show()
    app.exec()
    