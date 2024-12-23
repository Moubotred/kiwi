from typing import Union

import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Any, Dict
from urllib.parse import urlsplit
import pyautogui
from typing import Optional
from dataclasses import dataclass

@dataclass
class Medidor:
	numero:int

@dataclass
class Suminstro:
	numero:int

@dataclass
class Calendario:
    dia: int
    mes: int
    anio: int



class Complementos:

	@staticmethod
	def _drag_and_drop(
		x_inicial: int = 1080,
		y_inicial: int = 511,
		x_final: Optional[int] = None,
		y_final: Optional[int] = None,
		duration: float = 1) -> None:
		"""
		Realiza una acción de arrastre desde una posición inicial a una posición final.
		
		:param x_inicial: Coordenada x inicial de arrastre. Valor predeterminado: 1080.
		:param y_inicial: Coordenada y inicial de arrastre. Valor predeterminado: 511.
		:param x_final: Coordenada x final a la que se quiere arrastrar. 
						Si no se proporciona, se moverá 200 píxeles a la derecha de x_inicial.
		:param y_final: Coordenada y final a la que se quiere arrastrar. 
						Si no se proporciona, se mantendrá en la misma altura que y_inicial.
		:param duration: Duración del arrastre en segundos. Por defecto es 1 segundo.
		"""
		# Si no se proporciona una posición final, usa valores por defecto
		if x_final is None:
			x_final = x_inicial + 200  # Mueve 200 píxeles a la derecha si no se especifica x_final
		if y_final is None:
			y_final = y_inicial  # Mantiene la misma altura si no se especifica y_final

		# Mueve el cursor a la posición inicial
		pyautogui.moveTo(x_inicial, y_inicial)

		# Presiona el botón izquierdo del ratón
		pyautogui.mouseDown(button='left')

		# Mueve el cursor a la posición final mientras se mantiene presionado el botón
		pyautogui.dragTo(x_final, y_final, duration=duration)

		# Suelta el botón del ratón
		pyautogui.mouseUp(button='left')

		return True
	
	@staticmethod
	def _uploaded_file_verification(esquema: str) -> None:
		"""
		Verifica que el dominio en el esquema de URL sea 'drive.google.com'.
		"""
		parsed_url = urlsplit(esquema)
		dominio = parsed_url.netloc
		dominio_esperado = 'drive.google.com'
		if dominio == dominio_esperado:
			print('[*] Imagen Insertada Correctamente')
		else:
			print('[*] Dominio no coincide con el esperado.')

	@staticmethod
	def _ingresar_fecha(wait, calendario: Optional[Calendario]) -> None:
		"""
		Ingresa una fecha en los campos de día, mes y año utilizando un objeto Calendario.
		"""
		if calendario is None:
			print("No se proporcionó un objeto Calendario válido.")
			return
		
		try:
			# Usa los atributos de calendario para ingresar la fecha
			dia_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Día del mes']")))
			dia_input.clear()
			dia_input.send_keys(calendario.dia)

			mes_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Mes']")))
			mes_input.clear()
			mes_input.send_keys(calendario.mes)

			anio_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Año']")))
			anio_input.clear()
			anio_input.send_keys(calendario.anio)
		
		except NoSuchElementException:
			print("Elemento de fecha no encontrado. Verifica el XPath.")

class Componentes:
	def __init__(self) -> None:
		self.complementos = Complementos()

	def Scroll(self,timeout:int = 5):
		time.sleep(timeout)
		if self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[1]/div"))):
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	def Buttons(self,**kwargs)-> bool:

		try:
			
			if kwargs['Siguiente']:
				sandboxbutton = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.uArJ5e.UQuaGc.YhQJj.zo8FOc.ctEux')))

				if sandboxbutton:
					botonSiguiente = sandboxbutton[1] if len(sandboxbutton) > 1 else sandboxbutton[0]
					botonSiguiente.click()
					return True

			if kwargs['Uploadimagen']:

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
					
					if self.complementos._drag_and_drop():
						return True
						
						
				botonSubir = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.E6FpNe.Ce1Y1c')))
				botonSubir.click()

				botonExaminar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.fFW7wc.XKSfm-Sx9Kwc.picker-dialog')))
				self.driver.implicitly_wait(5)

				if self.complementos._drag_and_drop():
					return True
				
				return False

			if kwargs['Examinar']:
				verificacion = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.yP1fJf')))
				if verificacion:
					buscar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.KdVr9e.oyDRHc')))
					esquema = buscar.get_attribute('data-view-file-link')
					self.complementos._uploaded_file_verification(esquema=esquema)


		except (TimeoutException, ElementClickInterceptedException) as e:
			pass

	def Menuopen(self,**kwargs)-> None:
		"""
		opcion:argumento a seleccionar
		"""
		try:
			if kwargs['desplegar'] and kwargs['opcion']:
				menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@jsname='LgbsSe']")))
				menu.click()

				opcion = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='option' and @data-value='{kwargs['opcion']}']")))
				opcion.click()
			
			if kwargs['selecion'] and kwargs['opcion']:
				interno_radio = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{kwargs['opcion']}']")))
				interno_radio.click()
				
		except (TimeoutException, ElementClickInterceptedException) as e:
			pass

	def Sendinformation(self, *information: Union[int, str], **kwargs: Dict[str, Any]) -> None:
		try:
			# Busca el elemento input
			input_element = self.driver.find_element(By.XPATH, '//input[@class="whsOnd zHQkBf"]')
			input_element.clear()  # Limpia el campo antes de escribir
			
			# Determina el tipo de 'information' y envía el valor adecuado
			if information and isinstance(information[0], (int, str)):
				input_element.send_keys(str(information[0]))

			# Procesa la información de calendario si está presente en kwargs
			calendario = kwargs.get('calendario')
			if calendario and isinstance(calendario, (list, tuple)) and len(calendario) == 3:
				self.complementos._ingresar_fecha(calendario)
		
		except NoSuchElementException:
			print("Elemento no encontrado. Verifica el XPath.")


formulario = Componentes()

formulario.Scroll()
formulario.Menuopen(desplegar=True,opcion ='Tony Guizado')
formulario.Sendinformation(7898)
formulario.Buttons(siguiente=True)

formulario.Scroll()
formulario.Menuopen(desplegar=True,opcion ='Si')
formulario.Buttons(siguiente=True)

formulario.Scroll()
formulario.Sendinformation(calendario=(12,10,2024))
formulario.Buttons(siguiente=True)

formulario.Scroll()
formulario.Menuopen(selecionar=True,opcion='A3R')
formulario.Scroll()
formulario.Sendinformation(121212)
formulario.Buttons(Uploadimagen=True)
formulario.Buttons(Examinar=True)
formulario.Buttons(siguiente=True)

formulario.Scroll()
formulario.Sendinformation('ITECHENE')
formulario.Scroll()
formulario.Sendinformation('66666')
formulario.Buttons(Uploadimagen=True)
formulario.Buttons(Examinar=True)
formulario.Buttons(siguiente=True)
