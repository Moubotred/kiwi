import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from threading import Thread
from fastapi import FastAPI
import uvicorn
from sig.example import IntegratedWindow



# if __name__ == "__main__":
#     # Crear la aplicación PyQt5
#     app = QApplication(sys.argv)
#     window = IntegratedWindow(path_imagenes=path_absolute,imagenes=imagenes_lista)
#     window.show()
#     sys.exit(app.exec_())

#     # Ejecutar FastAPI en un hilo separado
#     server_thread = Thread(target=run_server, daemon=True)
#     server_thread.start()

#     # Ejecutar el bucle de eventos de PyQt5
#     sys.exit(qt_app.exec_())
