from PyQt5.QtCore import Qt, QUrl, QMimeData
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QSplitter, QHBoxLayout
from PyQt5.QtGui import QPixmap, QDrag
import os

class Configuraciones(QMainWindow):
    def __init__(self,upload):
        super().__init__()
        self.upload = upload
        self.initui()
    
    def initui(self):
        self.setWindowTitle('Configuraciones')

        self.widgetpersonalizado = QSplitter(Qt.Horizontal)

        """detalles de pantalla"""
        app = QApplication.instance() 
        screen = app.primaryScreen()
        size = screen.size( )
        screen_width = size.width()
        screen_height = size.height()
        """--------------------"""

        """ Sección gestor de imágenes """ 
        self.imagenes = os.path.join(os.path.expanduser('~'),self.upload)
        self.directorio = self.imagenes if os.path.abspath(self.imagenes) else os.makedirs(self.imagenes,exist_ok=True)
        # self.directorio = '/home/kimshizi/Documents/pqt5/_test_/imagenes'
        self.indice_imagenes = sorted(os.listdir(self.directorio))
        self.indice_inicial = 0
        self.indice_actual = 0  # Iniciar en 0
        self.pixmap = QPixmap(os.path.join(self.directorio, self.indice_imagenes[self.indice_actual]))
        self.pixmap = self.pixmap.scaled(800, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imagen = QLabel()
        self.imagen.setPixmap(self.pixmap)
        self.imagen.setAcceptDrops(True)
        """---------------------------"""

        # Añadir el gestor de imágenes al QSplitter
        self.gestor = self.gestorArchivos()
        self.widgetpersonalizado.addWidget(self.gestor)

        # Configurar QSplitter como widget central
        self.setCentralWidget(self.widgetpersonalizado)
        self.setGeometry(int(screen_width / 2), 0, int(screen_width / 2), screen_height)
        self.show()

    def gestorArchivos(self):
        contenedor = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.imagen, alignment=Qt.AlignCenter)
        contenedor.setStyleSheet("background-color: #297ff0;")
        contenedor.setLayout(layout)
        return contenedor

    def actualizarImagen(self):
        """Actualizar la imagen en QLabel con la siguiente en la lista."""
        self.indice_actual = (self.indice_actual + 1) % len(self.indice_imagenes)
        nueva_imagen = os.path.join(self.directorio, self.indice_imagenes[self.indice_actual])
        self.pixmap = QPixmap(nueva_imagen).scaled(800, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imagen.setPixmap(self.pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Iniciar el arrastre de la imagen
            mime_data = QMimeData()
            mime_data.setUrls([QUrl.fromLocalFile(os.path.join(self.directorio, self.indice_imagenes[self.indice_actual]))])

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(self.pixmap)
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

            # Actualizar la imagen después del arrastre
            self.actualizarImagen()

# app = QApplication([])
# window = Configuraciones()
# window.show()
# app.exec()
