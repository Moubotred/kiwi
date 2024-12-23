
from typing import Optional
from objetos import Config
# from execption.exceptions import GoogleFormularioException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Base:
    def __init__(self, config:Config) -> None:
        self.config = config
        self.driver : Optional[WebDriver]
        self.wait : Optional[WebDriverWait]

    def __enter__(self):
        """Permite usar la clase con context manager (with statement)"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el navegador automáticamente al salir del context manager"""
        self.close()

    def connect(self) -> None:
        """Establece la conexión con el navegador Firefox utilizando el objeto Navegador proporcionado."""
        
        try:
            firefox_options = Options()
            firefox_options.profile = self.config.profile
            if self.config.headless:
                firefox_options.add_argument("--headless")
                
            self.driver = webdriver.Firefox(options=firefox_options)
            self.wait = WebDriverWait(self.driver, self.config.timeout)
            self.driver.get(self.config.url)

            self.driver.set_window_rect(x=0, y=0, width=700, height=760)

        except Exception as e:
            print('error: ',e)
        
    def close(self) -> None:
        """Cierra el navegador si está abierto"""
        if self.driver:
            self.driver.quit()


