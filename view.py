from PyQt5.QtCore import QCoreApplication
import time
import random
from objetos import Config,Fecha
from core.formulario import form
from _test_.WidgetGestor import Configuraciones
from PyQt5.QtWidgets import QApplication
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import threading

suministro = random.getrandbits(32)

# fecha = Fecha(
# 	dia = 31,
# 	mes = 10,
# 	anio = 2024)

navegador = Config(
    url="https://docs.google.com/forms/d/e/1FAIpQLScl9GppEl6eY8sri9rZ8qOoQWRVj0-0m0G-Z2Gc7wehFGIVww/viewform",
    profile="/home/kimshizi/.mozilla/firefox/ur8ejeca.default-release",
    headless=False,
    timeout=40)

stop_application = False

FORMULARIO = {
    "tecnico":"Tony Guizado",
    "suministro":int("1846214"),

    "se_puede_realizar":"Si",

    "fecha":Fecha(
    	dia = 31,
	    mes = 10,
	    anio = 2024),

    "tipo_medidor_retirado":"A3R",
    "ubicacion":"Externo",
    "medidor_antes":int("5519560"),

    "tranferencia_imagen":int("1"),

    "tipo_medidor_instalado":"ITECHENE",
    "medidor_despues":int("5550326"),
    
    "operador":"Entel",
    "senal":"Media",
    
    "telemedida":"No",#Sí

    "se_entregó_medidor":"Sí",

    "tranferencia_mutiple":int("5"),

}

def main():

    global stop_application

    try:
        with form(config=navegador) as session:

            # session.driver.delete_all_cookies()

            #pagina 1
            session.borrar_formulario()
            session.buttons(FORMULARIO['tecnico'],menu = True)
            session.insert_information(suministro = FORMULARIO['suministro'])
            session.buttons(siguiente = True)

            #pagina 2
            session.buttons(FORMULARIO['se_puede_realizar'], menu = True)
            session.buttons(siguiente = True)    

            #pagina 3
            session.insert_information(calendario = FORMULARIO['fecha'])
            session.buttons(siguiente = True)

            #pagina 4
            session.buttons(FORMULARIO['tipo_medidor_retirado'], menu = True)
            session.buttons(FORMULARIO['ubicacion'], seleccion = True)
            session.insert_information(medidor = FORMULARIO['medidor_antes'])
            session.bt_Subir(FORMULARIO['tranferencia_imagen'])
            session.buttons(siguiente = True)

            # #pagina 5
            session.buttons(FORMULARIO['tipo_medidor_instalado'], menu = True)
            session.insert_information(medidor = FORMULARIO['medidor_despues'])
            session.bt_Subir(FORMULARIO['tranferencia_imagen'])
            session.buttons(siguiente = True)

            #pagina 6
            session.multiple_menu(submenu = 0,opcion = FORMULARIO['operador'])
            session.multiple_menu(submenu = 1,opcion = FORMULARIO['senal'])
            session.bt_Subir(FORMULARIO['tranferencia_imagen'])
            session.buttons(siguiente = True)

            #pagina 7
            session.buttons(FORMULARIO['telemedida'], menu = True)
            session.buttons(siguiente = True)

            #pagina 7 si telemedida esta invalidata

            session.bt_opcion_texto(motivo_telemedida_inabilitada='telemedida pendiente')
            session.buttons(siguiente = True)

            #pagina 8
            session.bt_Subir(FORMULARIO['tranferencia_imagen'])
            session.buttons(siguiente = True)

            #pagina 9
            session.buttons(FORMULARIO['se_entregó_medidor'], menu = True)
            session.buttons(siguiente = True)

            #pagina 10
            session.tranferencia_multiples_imagenes(FORMULARIO['tranferencia_mutiple'])
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

def Widget():
    app = QApplication([])
    window = Configuraciones()
    window.show()
    app.exec()

if __name__=="__main__":
    navegador_thread = threading.Thread(target=main)
    navegador_thread.start()
    Widget()
    navegador_thread.join()