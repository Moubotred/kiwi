# PYTHONPATH=/home/kimshizi/Documents/pqt5/
# PYTHONPATH=/home/kimshizi/Proyects/kiwi

import os
from PyQt5.QtCore import QCoreApplication
import time
import pyautogui
from objetos import Config,Fecha
from core.formulario import form
from _test_.WidgetGestor import Configuraciones
from PyQt5.QtWidgets import QApplication
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def kimera(navegador,capturas,FORMULARIO,status_application=None):

    pwd = os.path.join(os.path.expanduser('~'),capturas)
    os.makedirs(pwd,exist_ok=True)

    stop_application = False

    try:
        with form(config=navegador) as session:

            # session.driver.delete_all_cookies()

            #pagina 1
            session.borrar_formulario()
            session.buttons(FORMULARIO['tecnico'],menu = True)
            
            session.insert_information(suministro = FORMULARIO['suministro'])
            pyautogui.screenshot(os.path.join(pwd,'pagina_1.png'))
            session.buttons(siguiente = True)

            #pagina 2
            session.buttons(FORMULARIO['se_puede_realizar'], menu = True)
            pyautogui.screenshot(os.path.join(pwd,'pagina_2.png'))
            session.buttons(siguiente = True)    

            #pagina 3
            session.insert_information(calendario = FORMULARIO['fecha'])
            pyautogui.screenshot(os.path.join(pwd,'pagina_3.png'))
            session.buttons(siguiente = True)

            #pagina 4
            session.buttons(FORMULARIO['tipo_medidor_retirado'], menu = True)
            session.buttons(FORMULARIO['ubicacion'], seleccion = True)
            session.insert_information(medidor = FORMULARIO['medidor_antes'])
            session.bt_Subir(FORMULARIO['tranferencia_imagen'])
            pyautogui.screenshot(os.path.join(pwd,'pagina_4.png'))
            session.buttons(siguiente = True)

            # #pagina 5
            session.buttons(FORMULARIO['tipo_medidor_instalado'], menu = True)
            session.insert_information(medidor = FORMULARIO['medidor_despues'])
            session.bt_Subir(FORMULARIO['tranferencia_imagen'])
            pyautogui.screenshot(os.path.join(pwd,'pagina_5.png'))
            session.buttons(siguiente = True)

            #pagina 6
            session.multiple_menu(submenu = 0,opcion = FORMULARIO['operador'])
            session.multiple_menu(submenu = 1,opcion = FORMULARIO['senal'])
            session.bt_Subir(FORMULARIO['tranferencia_imagen'])
            pyautogui.screenshot(os.path.join(pwd,'pagina_6.png'))
            session.buttons(siguiente = True)

            #pagina 7
            session.buttons(FORMULARIO['telemedida'], menu = True)
            pyautogui.screenshot(os.path.join(pwd,'pagina_7.png'))
            session.buttons(siguiente = True)

            #pagina 7 si telemedida esta invalidata

            session.bt_opcion_texto(motivo_telemedida_inabilitada='telemedida pendiente')
            pyautogui.screenshot(os.path.join(pwd,'pagina_8.png'))
            session.buttons(siguiente = True)

            #pagina 8
            session.bt_Subir(FORMULARIO['tranferencia_imagen'])
            pyautogui.screenshot(os.path.join(pwd,'pagina_9.png'))
            session.buttons(siguiente = True)

            #pagina 9
            session.buttons(FORMULARIO['se_entregó_medidor'], menu = True)
            pyautogui.screenshot(os.path.join(pwd,'pagina_10.png'))
            session.buttons(siguiente = True)

            #pagina 10
            session.tranferencia_multiples_imagenes(FORMULARIO['tranferencia_mutiple'])
            pyautogui.screenshot(os.path.join(pwd,'pagina_11.png'))
            session.buttons(siguiente = True)
            
            #pagina 11
            session.enviar()
            
            time.sleep(20)
    except Exception as e :
        print(f"Error en el script de Selenium: {e}")

    finally:
        print("El script de Selenium ha finalizado.")
        stop_application = True  # Indicar que la aplicación debe detenerse
        QCoreApplication.quit()  # Detener la aplicación PyQt5

def Guiki(upload):
    app = QApplication([])
    window = Configuraciones(upload)
    window.show()
    app.exec()

