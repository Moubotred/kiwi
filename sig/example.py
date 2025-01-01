#
import time
import sys
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import Qt, QUrl, QMimeData
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, 
    QSplitter, QHBoxLayout,
    QMessageBox
)
from libform.const import Config, Fecha
from libform.main import executionWinForm
import os
import platform

from libform.taskform import FormWorker

class IntegratedWindow(QMainWindow):
    def __init__(self,path_imagenes,imagenes):
        super().__init__()
        self.form_data = None  # Aquí almacenarás los datos del formulario
        self.path_imagenes = path_imagenes
        self.imagenes = imagenes

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
        # self.imagenes = ''
        # self.imagenes = os.path.join(os.path.expanduser('~'),self.upload)

        self.directorio = self.path_imagenes if os.path.abspath(self.path_imagenes) else os.makedirs(self.path_imagenes,exist_ok=True)

        # self.directorio = '/home/kimshizi/Documents/pqt5/_test_/imagenes'
        # self.indice_imagenes = sorted(os.listdir(self.directorio))

        self.indice_imagenes = self.imagenes

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

        
    # def start_form_process(self):
        """Inicia el proceso del formulario"""
        if not self.form_data:
            # Aquí deberías inicializar form_data con los valores reales
            self.form_data = {
            "tecnico": "Tony Guizado",
            "suministro": int("1846214"),
            "se_puede_realizar": "Si",
            "fecha": Fecha(dia=31, mes=10, anio=2024),
            "tipo_medidor_retirado": "A3R",
            "ubicacion": "Externo",
            "medidor_antes": int("5519560"),
            "tranferencia_imagen": int("1"),
            "tipo_medidor_instalado": "ITECHENE",
            "medidor_despues": int("5550326"),
            "operador": "Entel",
            "senal": "Media",
            "telemedida": "No",
            "se_entregó_medidor": "Sí",
            "tranferencia_mutiple": int("5"),
        }   
        

        """
            CODIGO FUNCIONAL
                no implementado por motivo de obtener los datos 
                de formulario primero medianete el bot y luego 
                procesarlo con selenium
        
        self.worker = FormWorker(self.form_data, self.upload)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.error_signal.connect(self.show_error)
        self.worker.finished_signal.connect(self.process_finished)
        self.worker.start()

        

        """


        
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

    def update_progress(self, message):
        """Manejar actualizaciones de progreso"""
        print(f"Progreso: {message}")
        
    def show_error(self, message):
        """Muestra errores en un diálogo"""
        QMessageBox.critical(self, "Error", message)
        
    def process_finished(self, success):
        """Maneja la finalización del proceso"""
        status = "Proceso completado exitosamente" if success else "Proceso terminó con errores"
        print(f"Proceso completado {status}")
        
    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        self.image_updater.stop()
        self.image_updater.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # upload_dir = os.path.join(os.path.expanduser('~'), 'Documents/pqt5/imagenes/i-o')
    # ls = os.listdir(upload_dir)

    window = IntegratedWindow(path_imagenes=None,imagenes=None)
    window.show()
    sys.exit(app.exec_())