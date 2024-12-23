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
    profile = '/home/kimshizi/.mozilla/firefox/ur8ejeca.default-release',
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

if __name__== "__main__":
    navegador_thread = threading.Thread(target=kimera,args=(navegador,formulario))
    navegador_thread.start()
    Guiki(perfil='Documents/pqt5/_test_/imagenes')
    navegador_thread.join()