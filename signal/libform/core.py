import logging

from libform.const import Config
from libform.snake import logger

from typing import Optional
from selenium import webdriver

from PyQt5.QtCore import QThread, pyqtSignal

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

class Base(QThread):
    """Este hilo ejecutará Selenium sin bloquear la UI"""

    taskStarted = pyqtSignal(str)
    taskFinished = pyqtSignal(str)

    def __init__(self, parent:None,config:Config) -> None:
        super(Base, self).__init__(parent)
        self.config = config
        self.driver : Optional[WebDriver] = None
        self.wait : Optional[WebDriverWait] = None
        self.logger = logging.getLogger(__class__.__name__)

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

            # self.logger.info("Iniciando conexión")
            self.taskStarted.emit("Iniciando Selenium...")

            firefox_options = Options()
            firefox_options.profile = self.config.profile
            if self.config.headless:
                firefox_options.add_argument("--headless")
                
            self.driver = webdriver.Firefox(options=firefox_options)
            self.wait = WebDriverWait(self.driver, self.config.timeout)

            self.driver.get(self.config.url)

            self.driver.set_window_rect(x=0, y=0, width=700, height=760)

        except Exception as e:
            self.taskFinished.emit(f"Error: {e}")
            self.logger.error(f'error:{e}')

    def close(self) -> None:
        """Cierra el navegador si está abierto"""
        if self.driver:
            self.driver.quit()
            self.taskFinished.emit("cerrando navegador")
            