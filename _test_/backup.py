#!/usr/bin/env python
# /GoForm

# merojas idea
# https://chatgpt.com/c/67340f78-cf70-800e-b6d5-723f0ec9ed0b

# Status
# 200
# VersionHTTP/2
# Transferred14.01 kB (82.89 kB size)
# Referrer Policystrict-origin-when-cross-origin
# DNS ResolutionSystem

import os
import re
import time
import pyautogui
from urllib.parse import urlsplit

from dataclasses import dataclass
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

from pathlib import Path
import subprocess
import requests
from multiprocessing.pool import ThreadPool 

@dataclass
class FormConfig:
    """Configuración para el formulario de Google"""
    profile_path: str
    form_url: str
    headless: bool = False
    timeout: int = 20

class FileUploader:
    def __init__(self, folder: str, port: int = 9090):
        """
        Inicializa la clase FileUploader para manejar la subida de archivos.

        Args:
            folder: Carpeta desde donde se servirá el archivo.
            port: Puerto en el que se correrá el servidor HTTP.
        """
        self.folder = folder
        self.port = port
        self.public_url: Optional[str] = None
        self.processes = []  # Almacenar los procesos iniciados

    def _start_http_server(self):
        try:
            os.chdir(Path(os.getcwd()) / self.folder)
            process = subprocess.Popen(
                ["python", "-m", "http.server", str(self.port)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.processes.append(process)  # Agregar proceso a la lista
            print(f'[+] Servidor HTTP corriendo en el puerto {self.port}')
        except Exception as e:
            print(f"[!] Error al iniciar el servidor HTTP: {str(e)}")    

    def _start_ngrok(self):
        try:
            process = subprocess.Popen(
                ["ngrok", "http", str(self.port)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.processes.append(process)  # Agregar proceso a la lista
            print(f'[+] Ngrok corriendo para el puerto {self.port}')
        except Exception as e:
            print(f"[!] Error al iniciar Ngrok: {str(e)}")

    def _get_ngrok_url(self) -> Optional[str]:
        """Consulta la API local de ngrok para obtener la URL pública."""
        try:
            response = requests.get('http://127.0.0.1:4040/api/tunnels')
            response.raise_for_status()
            tunnels_info = response.json()
            tunnels = tunnels_info.get('tunnels', [])
            if tunnels:
                public_url = tunnels[0].get('public_url')
                # print(f'[+] URL pública obtenida: {public_url}')
                return public_url
            else:
                print("[!] No hay túneles activos de Ngrok")
                return None
        except requests.exceptions.ConnectionError:
            print("[!] Asegúrate de que Ngrok esté en ejecución manualmente")
            return None
        except Exception as e:
            print(f"[!] Error al obtener la URL de Ngrok: {str(e)}")
            return None

    def start_services(self):
        """Inicia el servidor HTTP y Ngrok simultáneamente y obtiene la URL pública."""
        try:
            pool = ThreadPool(2)
            pool.apply_async(self._start_http_server)
            pool.apply_async(self._start_ngrok)

            # Intentar obtener la URL pública varias veces, con espera entre cada intento
            attempts = 0
            max_attempts = 10
            while attempts < max_attempts:
                self.public_url = self._get_ngrok_url()
                if self.public_url:
                    break
                attempts += 1
                time.sleep(1)  # Espera 1 segundo antes de intentarlo de nuevo
        
            self.public_url = self._get_ngrok_url()

            if self.public_url:
                print(f'[+] URL pública : {self.public_url}')
            else:
                print("[!] Error: No se pudo obtener la URL pública de Ngrok")

        except Exception as e:
            print(f"[!] Error al iniciar los servicios: {str(e)}")
    
    def __enter__(self):
        """Inicializa los servicios al entrar en el contexto."""
        self.start_services()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Mata los procesos iniciados al salir del contexto."""
        for process in self.processes:
            process.terminate()
            print(f"[+] Proceso {process.pid} terminado")
        print("[+] Todos los procesos de servidor HTTP y Ngrok han sido terminados.")

class GoogleFormException(Exception):
    """Excepción personalizada para errores del formulario"""
    pass

class GoogleForm:
    def __init__(self, config: FormConfig) -> None:
        """
        Inicializa el formulario de Google con la configuración proporcionada
        
        Args:
            config: Configuración del formulario
        """
        self.config = config
        self.driver: Optional[WebDriver] = None
        self.wait: Optional[WebDriverWait] = None
        
    def __enter__(self):
        """Permite usar la clase con context manager (with statement)"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el navegador automáticamente al salir del context manager"""
        self.close()

    def connect(self) -> None:
            """Establece la conexión con el navegador Firefox"""
            try:
                firefox_options = Options()
                firefox_options.profile = self.config.profile_path
                if self.config.headless:
                    firefox_options.add_argument("--headless")
                    
                self.driver = webdriver.Firefox(options=firefox_options)
                self.wait = WebDriverWait(self.driver, self.config.timeout)
                self.driver.get(self.config.form_url)

                self.driver.set_window_rect(x=0, y=0, width=700, height=760)

            except Exception as e:
                raise GoogleFormException(f"Error al conectar: {str(e)}")

    def scroll(self) -> None:
        time.sleep(5)
        # self.driver.implicitly_wait(8)
        if self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[1]/div"))):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def botones(self,siguiente=False,atras=False) -> None:
        """Envía el formulario"""

        try:
            botones = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.uArJ5e.UQuaGc.YhQJj.zo8FOc.ctEux')))

            if siguiente:
                try:
                    botonSiguiente = botones[1]
                    botonSiguiente.click()

                except Exception as e:
        
                    botonSiguiente = botones[0]
                    botonSiguiente.click()

            if atras:
                botonAtras = botones[0]
                botonAtras.click()

        except Exception as e:
            raise GoogleFormException(f"Error al enviar el formulario: {str(e)}")

    def mover_imagen(self):
        # Posición inicial del cursor (puedes cambiar estos valores)
        x_inicial = 1080
        y_inicial = 511

        # Mueve el cursor a la posición inicial
        pyautogui.moveTo(x_inicial, y_inicial)

        # Presiona el botón izquierdo del ratón
        pyautogui.mouseDown(button='left')

        # Mueve el cursor 200 píxeles a la derecha mientras se mantiene presionado el botón
        pyautogui.dragTo(x_inicial - 750, y_inicial, duration=1)
        
        try:
            verificacion = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.yP1fJf')))
            if verificacion:
                buscar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.KdVr9e.oyDRHc')))
                esquema = buscar.get_attribute('data-view-file-link')
                parsed_url = urlsplit(esquema)
                dominio = parsed_url.netloc
                dominio_esperado = 'drive.google.com'
                if dominio == dominio_esperado:
                    print('[*] Imagen Insertada Correctamente')

        except Exception as e:
            raise GoogleFormException(f"Error:{e}")

    def close(self) -> None:
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()

    def insertar_informacion(self, valor: str) -> None:
        """
        Ingresa el número de suministro en el formulario
        
        Args:
            numero_suministro: Número de suministro a ingresar
        """
        try:
            input_element = self.driver.find_element(
                By.XPATH, '//input[@class="whsOnd zHQkBf"]'
            )
            input_element.clear()  # Limpia el campo antes de escribir
            input_element.send_keys(valor)

            # body_element = self.driver.find_element(By.TAG_NAME, "body")
            # body_element.click()

        except NoSuchElementException:
            raise GoogleFormException("No se encontró el campo de suministro")

    def insertar_imagen(self) -> bool:
            
        """codigo funcional"""

        original_implicit_wait =self.driver.timeouts.implicit_wait
        self.driver.implicitly_wait(0)
        botonCerrar = self.driver.find_elements(By.CSS_SELECTOR, '.XuQwKc')
        self.driver.implicitly_wait(original_implicit_wait)

        if botonCerrar:
            botonCerrar[0].click()
            botonSubir = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.E6FpNe.Ce1Y1c')))
            botonSubir.click()
            
            botonExaminar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.fFW7wc.XKSfm-Sx9Kwc.picker-dialog')))
            self.driver.implicitly_wait(5)
            return True    
        
        botonSubir = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.E6FpNe.Ce1Y1c')))
        botonSubir.click()

        botonExaminar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.fFW7wc.XKSfm-Sx9Kwc.picker-dialog')))
        self.driver.implicitly_wait(5)
        return True
  
    def calendario(self, dia: str,mes :str , ano:str) -> None:
        dia_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Día del mes']")))
        dia_input.clear()  # Borrar cualquier valor existente
        dia_input.send_keys(dia)  # Cambia "22" por el valor del día que desees ingresar

        # 2. Ingresar el Mes
        mes_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Mes']")))
        mes_input.clear()  # Borrar cualquier valor existente
        mes_input.send_keys(mes)  # Cambia "11" por el valor del mes que desees ingresar

        # 3. Ingresar el Año
        anio_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Año']")))
        anio_input.clear()  # Borrar cualquier valor existente
        anio_input.send_keys(ano)  # Cambia "2024" por el valor del año que desees ingresar

    def seleccionar_item(self, ubicacion) -> None:
        try:
            interno_radio = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{ubicacion}']")))
            interno_radio.click()    

        except (TimeoutException, ElementClickInterceptedException) as e:
            raise GoogleFormException(f"Error al seleccionar opcion : {str(e)}")
        
    def seleccionar(self, argumentos: str) -> None:
        """
        Selecciona un técnico del menú desplegable
        
        Args:
            tecnico: Nombre del técnico a seleccionar
        """
        try:

            """codigo prueba"""

            # lista_de_preguntas = self.wait.until((EC.presence_of_all_elements_located((By.CSS_SELECTOR,".Qr7Oae"))))
            # lista_de_preguntas.pop(0) # elimina el inidice 0 ya que solo es un banner no un preguntasgunta para interatuar

            # print(f"[*] numero preguntas {len(lista_de_preguntas)}")

            """-------------"""

            # Abrir menú desplegable
            menu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@jsname='LgbsSe']"))
            )
            menu.click()
            
            # Esperar y seleccionar opción
            opcion = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//div[@role='option' and @data-value='{argumentos}']")
                )
            )
            opcion.click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            raise GoogleFormException(f"Error al seleccionar técnico: {str(e)}")

    def verificar_tecnico(self, tecnico_verificar: str) -> bool:
        """
        Verifica si un técnico existe en la lista
        
        Args:
            tecnico_verificar: Nombre del técnico a verificar
            
        Returns:
            bool: True si el técnico existe, False en caso contrario
        """
        try:
            tecnicos = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
            )
            
            for tecnico in tecnicos:
                item = tecnico.get_attribute("innerHTML")
                if match := re.search(r'>([^<]+)</span>', item):
                    nombre = match.group(1)
                    if nombre != "Elegir" and nombre == tecnico_verificar:
                        return True
            return False
        except TimeoutException:
            raise GoogleFormException("Error al cargar la lista de técnicos")

    def procesar_formulario(self, tecnico: str, numero_suministro: str) -> None:
        """
        Procesa el formulario completo
        
        Args:
            tecnico: Nombre del técnico
            numero_suministro: Número de suministro
        """

        try:
            # with FileUploader(folder="imagen", port=9090) as uploader:
                # if not uploader.public_url:
                    # raise GoogleFormException("No se pudo obtener la URL pública de la imagen")
            
                # Scroll al final de la página para asegurar que todos los elementos sean visibles
                self.scroll()
                
                # Verificar y seleccionar técnico
                if self.verificar_tecnico(tecnico):

                    # pagina 1
                    self.seleccionar(argumentos=tecnico)
                    self.insertar_informacion(valor=numero_suministro)
                    self.botones(siguiente=True)
                    self.scroll()

                    # pagina 2
                    self.seleccionar(argumentos='Si')
                    self.botones(siguiente=True)
                    self.scroll()
                    

                    # pagina 3
                    self.calendario('6','11','2024')
                    self.botones(siguiente=True)
                    

                    # pagina 3
                    self.scroll()
                    self.seleccionar(argumentos='A3R')
                    self.scroll()
                    self.seleccionar_item(ubicacion='Interno')
                    self.scroll()
                    self.insertar_informacion(valor='555555')
                    self.insertar_imagen()
                    self.mover_imagen()
                    self.botones(siguiente=True)
                    

                    # pagina 4
                    self.scroll()
                    self.seleccionar(argumentos='ITECHENE')
                    self.scroll()
                    self.insertar_informacion(valor='66666')
                    self.insertar_imagen()
                    self.mover_imagen()
                    self.botones(siguiente=True)
                    

                    self.scroll()
                    self.seleccionar(argumentos='Entel')
                    self.seleccionar(argumentos='Baja')
                    self.insertar_imagen()
                    self.mover_imagen()
                    self.botones(siguiente=True)

                    time.sleep(10)
                    
                else:
                    raise GoogleFormException(f"Técnico '{tecnico}' no encontrado")
                
        except GoogleFormException as e:
            raise e
        except Exception as e:
            raise GoogleFormException(f"Error inesperado: {str(e)}")

def main():
    """Función principal de ejemplo"""
    config = FormConfig(
        profile_path="/home/kimshizi/.mozilla/firefox/ur8ejeca.default-release",
        form_url="https://docs.google.com/forms/d/e/1FAIpQLScl9GppEl6eY8sri9rZ8qOoQWRVj0-0m0G-Z2Gc7wehFGIVww/viewform",
        headless=False,
        timeout=24
    )

    try:

        with GoogleForm(config) as form:
            form.procesar_formulario(
                tecnico='Tony Guizado',
                numero_suministro='7998'
            )
    except GoogleFormException as e:
        print(f"Error al procesar el formulario: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()