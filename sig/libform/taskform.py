import os
import time
import platform
from libform.const import Config
from libform.main import executionWinForm
from PyQt5.QtCore import QThread, pyqtSignal

class FormWorker(QThread):
    """Worker thread para la automatización del formulario"""
    progress_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    
    def __init__(self, form_data, image_directory):
        super().__init__()
        self.form_data = form_data
        self.image_directory = image_directory
        self.navegador = Config(
            url="https://docs.google.com/forms/d/e/1FAIpQLScl9GppEl6eY8sri9rZ8qOoQWRVj0-0m0G-Z2Gc7wehFGIVww/viewform",
            profile = '/home/kimshizi/.mozilla/firefox/ur8ejeca.default-release' 
                     if 'Debian' in platform.version() 
                     else os.path.join(os.path.expanduser('~'),'Proyects','kiwi','ur8ejeca.default-release'),
            headless=False,
            timeout=40
        )
    
    def fill_page_1(self, session):
        """Llenar primera página del formulario"""
        self.progress_signal.emit("Llenando página 1...")
        session.borrar_formulario()
        session.buttons(self.form_data['tecnico'], menu=True)
        session.insert_information(suministro=self.form_data['suministro'])
        session.buttons(siguiente=True)
    
    def fill_page_2(self, session):
        """Llenar segunda página del formulario"""
        self.progress_signal.emit("Llenando página 2...")
        session.buttons(self.form_data['se_puede_realizar'], menu=True)
        session.buttons(siguiente=True)
    
    def fill_page_3(self, session):
        """Llenar tercera página del formulario"""
        self.progress_signal.emit("Llenando página 3...")
        session.insert_information(calendario=self.form_data['fecha'])
        session.buttons(siguiente=True)
    
    def fill_page_4(self, session):
        """Llenar cuarta página del formulario"""
        self.progress_signal.emit("Llenando página 4...")
        session.buttons(self.form_data['tipo_medidor_retirado'], menu=True)
        session.buttons(self.form_data['ubicacion'], seleccion=True)
        session.insert_information(medidor=self.form_data['medidor_antes'])
        session.bt_Subir(self.form_data['tranferencia_imagen'])
        session.buttons(siguiente=True)
    
    def fill_page_5(self, session):
        """Llenar quinta página del formulario"""
        self.progress_signal.emit("Llenando página 5...")
        session.buttons(self.form_data['tipo_medidor_instalado'], menu=True)
        session.insert_information(medidor=self.form_data['medidor_despues'])
        session.bt_Subir(self.form_data['tranferencia_imagen'])
        session.buttons(siguiente=True)
    
    def fill_page_6(self, session):
        """Llenar sexta página del formulario"""
        self.progress_signal.emit("Llenando página 6...")
        session.multiple_menu(submenu=0, opcion=self.form_data['operador'])
        session.multiple_menu(submenu=1, opcion=self.form_data['senal'])
        session.bt_Subir(self.form_data['tranferencia_imagen'])
        session.buttons(siguiente=True)
    
    def fill_remaining_pages(self, session):
        """Llenar páginas restantes del formulario"""
        self.progress_signal.emit("Llenando páginas finales...")
        # Página 7
        session.buttons(self.form_data['telemedida'], menu=True)
        session.buttons(siguiente=True)
        
        # Página 7 (telemedida inválida)
        session.bt_opcion_texto(motivo_telemedida_inabilitada='telemedida pendiente')
        session.buttons(siguiente=True)
        
        # Página 8
        session.bt_Subir(self.form_data['tranferencia_imagen'])
        session.buttons(siguiente=True)
        
        # Página 9
        session.buttons(self.form_data['se_entregó_medidor'], menu=True)
        session.buttons(siguiente=True)
        
        # Página 10
        session.tranferencia_multiples_imagenes(self.form_data['tranferencia_mutiple'])
        session.buttons(siguiente=True)
        
        # Página 11
        session.enviar()
        
    def run(self):
        """Ejecuta la automatización del formulario"""
        try:
            with executionWinForm(parent=None, config=self.navegador) as session:
                self.fill_page_1(session)
                self.fill_page_2(session)
                self.fill_page_3(session)
                self.fill_page_4(session)
                self.fill_page_5(session)
                self.fill_page_6(session)
                self.fill_remaining_pages(session)
                
                self.progress_signal.emit("Esperando confirmación...")
                time.sleep(20)
                self.finished_signal.emit(True)
                
        except Exception as e:
            self.error_signal.emit(f"Error en el script de Selenium: {str(e)}")
            self.finished_signal.emit(False)