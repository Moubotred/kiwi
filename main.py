import re
import time
import pyautogui
from objetos import Config,FormularioDatos
from typing import Optional,Dict,Callable,Type,Any
from selenium import webdriver
from urllib.parse import urlsplit
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from execption.exceptions import GoogleFormularioException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)



from objetos import Fecha
        
class Google:
    def __init__(self,config:Config) -> None:
        self.config = config
        self.driver :Options[WebDriver] = None
        self.wait : Optional[WebDriverWait] = None

    def __enter__(self):
        """Permite usar la clase con context manager (with statement)"""
        self.conexion()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el navegador automáticamente al salir del context manager"""
        self.close()

    def conexion(self):

        """Establece la conexión con el navegador Firefox"""
        try:

            selenium_grid_url = "http://192.168.1.113:4444/wd/hub"

            # Create a desired capabilities object as a starting point.
            capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities['platform'] = "WINDOWS"
            capabilities['version'] = "10"

            firefox_options = Options()
            firefox_options.profile = self.config.profile
        
            if self.config.headless:
                firefox_options.add_argument("--headless")
                
            self.driver = webdriver.Remote(
                command_executor=selenium_grid_url,
                desired_capabilities=capabilities,
                options=firefox_options
                )
            
            self.wait = WebDriverWait(self.driver, self.config.timeout)
            self.driver.get(self.config.url)

            self.driver.set_window_rect(x=0, y=0, width=700, height=760)

        except Exception as e:
            print(e)
    
    def close(self) -> None:
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()

class Widget(Google):
    def __init__(self,config:Config) -> None:
        super().__init__(config)
        
    def _scroll(self):
        time.sleep(5)
        # self.driver.implicitly_wait(8)
        if self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[1]/div"))):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    

    def _open_menu(self,**kwargs)->bool:
        time.sleep(5)
        menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@jsname='LgbsSe']")))
        menu.click()
        return True

    def _opcion_menu(self,*argv,**kwargs)->bool:
        opcion = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='option' and @data-value='{argv[0]}']")))
        opcion.click()
        return True

    def _next_click(self, *argv, **kwargs):
        # self.driver.refresh()
        sandboxbutton = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.uArJ5e.UQuaGc.YhQJj.zo8FOc.ctEux')))
        if sandboxbutton:
            botonSiguiente = sandboxbutton[1] if len(sandboxbutton) > 1 else sandboxbutton[0]
            botonSiguiente.click()
            return True

    def _information_text(self,text:str):
        input_element = self.driver.find_element(By.XPATH, '//input[@class="whsOnd zHQkBf"]')
        input_element.clear() 
        input_element.send_keys(text) 
 
    def _information_numeric(self,numeric:int):
        input_element = self.driver.find_element(By.XPATH, '//input[@class="whsOnd zHQkBf"]')
        input_element.clear() 
        input_element.send_keys(numeric) 

    def _information_calendar(self,calendario:Fecha):

        try:
            # Usa los atributos de calendario para ingresar la fecha
            dia_input = self.navegador.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Día del mes']")))
            dia_input.clear()
            dia_input.send_keys(calendario.dia)

            mes_input = self.navegador.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Mes']")))
            mes_input.clear()
            mes_input.send_keys(calendario.mes)

            anio_input = self.navegador.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Año']")))
            anio_input.clear()
            anio_input.send_keys(calendario.anio)

        except NoSuchElementException:
            print("Elemento de fecha no encontrado. Verifica el XPath.")

class Event(Widget):
    def __init__(self,config:Config) -> None:
        super().__init__(config)
        self.handlers: Dict[str, Dict[Type, Callable[[Any], None]]] = {
            'suministro': {
                str: self._information_text,
                int: self._information_numeric,
            },
            'calendario': {
                Fecha: self._information_calendar,
            }
        }
    
    def event_accions(self,*opcion,**kawrgs):
        if kawrgs.get('tecnico') is True:
            self._open_menu()
            self._opcion_menu(opcion[0])

        if kawrgs.get('siguiente') is True:
            self._scroll()
            self._next_click()

    def event_information(self,*argv,**kwargs):
        for field, value in kwargs.items():
            if field in self.handlers:
                field_handlers = self.handlers[field]
                for expected_type, handler in field_handlers.items():
                    if isinstance(value, expected_type):
                        handler(value)
                        break
                else:
                    print(f"[!] No hay un manejador para el tipo '{type(value).__name__}' en el campo '{field}'.")
            else:
                print(f"[!] No hay un manejador definido para el campo '{field}'.")

# config = Config(
#     url = "https://docs.google.com/forms/d/e/1FAIpQLScl9GppEl6eY8sri9rZ8qOoQWRVj0-0m0G-Z2Gc7wehFGIVww/viewform",
#     # profile = "/home/kimshizi/.mozilla/firefox/ur8ejeca.default-release",
#     profile = r"C:\User\nimun\AppData\Roamning\Mozilla\Firefox\Profiles\xxkrjzbd.default-release-1",
#     headless = False,
#     timeout=20,
# )


# with Event(config) as session:
#     session.event_accions('Tony Guizado',tecnico=True)
#     session.event_information(suministro='222229')
#     session.event_accions(siguiente=True)