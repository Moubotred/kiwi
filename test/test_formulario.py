import pytest
import random
import threading
from objetos import Config,Fecha
from app import Guiki
import os
from app import kimera

suministro = random.getrandbits(32)

navegador = Config(
    url = "https://docs.google.com/forms/d/e/1FAIpQLScl9GppEl6eY8sri9rZ8qOoQWRVj0-0m0G-Z2Gc7wehFGIVww/viewform",
    profile = os.path.join(os.path.expanduser('~'),'Proyects','kiwi','ur8ejeca.default-release'),
    # profile = '/home/kimshizi/.mozilla/firefox/ur8ejeca.default-release',
    headless = False,
    timeout = 40)

stop_application = False

formulario = {
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

capturas = 'Documents/pqt5/capturas' # local
# capturas = 'Proyects/kiwi/capturas' # vps

upload_driver = 'Documents/pqt5/imagenes' # local
# upload_driver = 'Proyects/kiwi/imagenes' # vps

if __name__== "__main__":
    navegador_thread = threading.Thread(target=kimera,args=(navegador,capturas,formulario))
    navegador_thread.start()
    # Guiki(upload = upload_driver)
    navegador_thread.join()