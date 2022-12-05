from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtSql import *
from PySide6 import QtTest
import pathlib
import random



class Finestra(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Juego')

        self.path = pathlib.Path(__file__).parent.resolve()
        
        self.tablero = QGridLayout()

        self.fotos =  dict({
         1:  [str(self.path) + "/imagenes/imagenes/alcaraz.jpeg", 1],
         2:  [str(self.path) + "/imagenes/imagenes/biden",2],
         3:  [str(self.path) + "/imagenes/imagenes/zelenski",3],
         4:  [str(self.path) + "/imagenes/imagenes/putin",4],
         5:  [str(self.path) + "/imagenes/imagenes/reinaIsabel", 5],
         6:  [str(self.path) + "/imagenes/imagenes/willsmith",6]}) 
        
        self.elementos = []

        self.crearCartas()

        reiniciar = QPushButton("Reiniciar")
        reiniciar.clicked.connect(self.crearCartas)

        main = QVBoxLayout()
        main.addLayout(self.tablero)
        main.addWidget(reiniciar)
        
        contenedor = QWidget()
        contenedor.setLayout(main)

        self.setCentralWidget(contenedor)


    def crearCartas(self):

        posiciones = []

       # depende del numero de pueden aparecer mas parejas tiene que ser un numero par
        for i in range(2):
            for x in range(6):
                posiciones.append([i,x])
               

        x = 0
        for i in range(len(posiciones)):
            aleatorio = random.choice(posiciones)
            
            carta = Carta(self.fotos.get(x+1)[0], self.fotos.get(x+1)[1], self)
        
            self.tablero.addWidget(carta, aleatorio[0], aleatorio[1])
           
            posiciones.remove(aleatorio)
            self.elementos.append(carta)
            x += 1
            if x == 6:
                x = 0

        self.girarTodas()


    def check(self):
        cont = 0
        cartas = [] 

        for i in self.elementos:
            if i.getEstado():
                cont += 1
                cartas.append(i)

        if cont >= 2:
            if cartas[0].id == cartas[1].id:
                self.elementos.remove(cartas[0]) 
                self.elementos.remove(cartas[1])
            else:
                self.desabilitar()
                QtTest.QTest.qWait(500)
                self.girarTodas()
        
        if len(self.elementos) == 0:
            self.victoria = Victoria()
            self.victoria.show()


    def desabilitar(self):
        for i in self.elementos:
            i.setEnabled(False)

    def girarTodas(self):
        for a in self.elementos:
            a.girar()
            a.setEnabled(True)
            
            

class Carta(QPushButton):
    def __init__(self, imagen, id, finestra):
        super().__init__()
        
        self.id = id
        self.finestra = finestra

        self.path = pathlib.Path(__file__).parent.resolve()

        self.carta = QPixmap(str(self.path) + "/imagenes/imagenes/carta")
       
        self.setFixedSize(200,200)
       
        self.mainFoto = QPixmap(imagen)
        
        self.setIcon(self.mainFoto)
        self.setIconSize(QSize(200,200))
        
        self.clicked.connect(self.cambiar)
        
        self.estado = False

    def cambiar(self):
        self.setIcon(self.mainFoto)
        self.estado = True
        Finestra.check(self.finestra)

    def girar(self):
        self.setIcon(self.carta)
        self.estado = False
    
    def getEstado(self):
        return self.estado


class Victoria(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Victoria")

        texto = QLabel("Enhorabuena has GANADO!!!!!!")
        texto.setStyleSheet("font-size: 50px; color: gold")
        self.setStyleSheet("background-color: black")

        self.setCentralWidget(texto)

       
if __name__ == "__main__":
    app = QApplication()
    finestra = Finestra()
    finestra.show()
    app.exec()
   