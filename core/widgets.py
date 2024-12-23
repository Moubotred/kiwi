import time
from objetos import Fecha
from objetos import Config
from core.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException,NoSuchElementException,ElementClickInterceptedException,ElementNotInteractableException)
from core.components import Components
from core.message import flagmessage,popmessage
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.wait import WebDriverWait


import logging
import inspect

CONFIG = {
    "borrarformulario":".NPEfkd.RveJvd.snByac",
    "menu": "//div[@jsname='LgbsSe']",
    "opcion_menu":"//div[@role='option' and @data-value='$']",
    "bt_siguiente":".uArJ5e.UQuaGc.YhQJj.zo8FOc.ctEux",
    "bt_subir":".E6FpNe.Ce1Y1c",
    "iframe":"/html/body/div[3]/div[2]/div/iframe",
    "examinar":"/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div/button/span",
    "insertar":'//input[@class="whsOnd zHQkBf"]',

    "dia":"//input[@aria-label='Día del mes']",
    "mes":"//input[@aria-label='Mes']",
    "anio":"//input[@aria-label='Año']",

    "seleccion":"//div[@aria-label='$']",
    "dialogdrive":".fFW7wc.XKSfm-Sx9Kwc.picker-dialog",
    "localizar_imagenes":".yP1fJf",
    "imagen_actual":".KdVr9e.oyDRHc"
}

# Configuración básica
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato de los mensajes
    filename="app.log",  # Archivo donde se guardan los logs
    filemode="w"  # 'w' para sobrescribir el archivo cada vez que se ejecuta el script
)

# Alternativamente, para que también se muestren en consola:
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

class Widgets(Base):
    def __init__(self,config:Config) -> None:
        super().__init__(config)

        self.componente = Components()

    @staticmethod
    def get_function_name():
        """Devuelve el nombre de la función actual."""
        return inspect.currentframe().f_back.f_code.co_name

    def contador_preguntas(self,forzar_scroll_tiempo:bool=False,forzar_tiempo:bool=False) -> None:

        """
        funcion permite realizar scroll para ubicar un elemento
        args:
            force_time : permite solo poner un tiempo implcito
            forzar_scroll_tiempo: permite forzar el tiempo y hace un scroll
        """
        if forzar_tiempo:
            time.sleep(2)
        
        if forzar_scroll_tiempo:
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

    def borrar_formulario(self):

        """
        funcin permite borrar todos los datos de formulario
        args:
            css_selector_borrar:indetifica la expresion de 
            donde se localiza el boton borrar formulario
        """

        self.contador_preguntas(forzar_scroll_tiempo=True)

        try:
            """localiza el boton borrar datos de formualario y abrir popup"""
            localizar_bt_formulario = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,CONFIG['borrarformulario'])))
            if len(localizar_bt_formulario) > 1:
                localizar_bt_formulario[1].click()
                
                """confimar el borrado de formualario"""
                confirmaborrado = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,CONFIG['borrarformulario'])))
                confirmaborrado[5].click() # abre una ventana popup para confirmar

                logging.info('[+] formulario borrado exitosamente')


        except Exception as e:
            logging.error(f'[!] error funcion {self.get_function_name()} tipo:{e}')

    def abrir_menu(self)-> bool:
        """
        funcion usadada para poder abrir el menu 

        args:
            xpath_menu:
                ingresa la expresion de xpath si cambia el elemento
                en el diccionario CONFIG
        """

        self.contador_preguntas(forzar_tiempo=True)

        try:
            menu = self.wait.until(EC.element_to_be_clickable((By.XPATH,CONFIG['menu'])))
            menu.click()
            logging.info('[+] menu abierto exitosamente')
            return True
        
        except Exception as e:
            logging.error(f'[!] error funcion:[{self.get_function_name()}] tipo:{str(e)}')
            
    def opcion_menu(self,opcion:str,)-> bool:
        """
        funcion permite seleccionar una opcion una vez desplegao el menu

        args:
            opcion: permite seleccionar una opcion del menu desplegado

        return:
            bool
        """
        try:
            localizar_opcion = self.wait.until(EC.element_to_be_clickable((By.XPATH, CONFIG['opcion_menu'].replace('$',opcion))))
            localizar_opcion.click()
            logging.info('[+] opcion seleccionada exitosamente')
            return True
        
        except Exception as e:
            logging.error(f'[!] error funcion:[{self.get_function_name()}] tipo:{str(e)}')

    def bt_siguiente(self)-> None:        
            
        """
        funcion permite realizar pasar a la siguinte 
        pagina del formulario de google form

        args:
            css_selector_siguinte: expresion que permite localizar el bt
        """
        self.contador_preguntas(forzar_scroll_tiempo=True)
        try:
            localizar_bt_siguinte = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,CONFIG['bt_siguiente'])))
            if localizar_bt_siguinte:
                botonsiguinte = localizar_bt_siguinte[0] if len(localizar_bt_siguinte)<2 else localizar_bt_siguinte[1]
                botonsiguinte.click()
                logging.info('[+] bt siguiente ejecutado')
                return True
            
        except (TimeoutException,Exception) as e:
            logging.error(f'[!] error funcion: [{self.get_function_name()}] tipo: {str(e)}')

    def bt_Subir(self,subir_imagenes:int) -> None:
        """
        funcion permite subir imagens arrastrando y soltando
        interactuando con los elementos

        args:
            subir_imagenes:
                ingresar el numero de imagens que se va a subir
        """

        try:
            
            for imagen in range(subir_imagenes):
                self.contador_preguntas(forzar_tiempo=True)
                localizar_bt_Subir = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,CONFIG['bt_subir'])))
                localizar_bt_Subir.click()

                localizar_iframe = self.buscar_iframe()
                extraer_texto_Examinar = localizar_iframe

                if extraer_texto_Examinar:
                    logging.info('[+] google drive abierto ')
                    if self.componente._drag_and_drop():
                        self.verificar_imagen_subida(imagen=subir_imagenes)
                        
        except Exception as e:
            logging.error(f'error funcion: [{self.get_function_name()}] tipo: {str(e)}')
    
    def bt_cerrar(self):
        try:
            botonCerrar = self.driver.find_elements(By.CSS_SELECTOR, '.XuQwKc')
            if len(botonCerrar) > 0:
                time.sleep(1)
                botonCerrar[0].click()
                return True
            return False
        
        except Exception as e:
            print('error: ',e)

    def bt_opcion_texto(self,motivo_telemedida_inabilitada:str) -> None:
        try:
            opciones = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.uHMk6b.fsHoPb')))
            opciones[5].click()

            motivo = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.Hvn9fb.zHQkBf')))
            motivo.send_keys(motivo_telemedida_inabilitada)

            logging.info('[+] motivo de telemedida inabilitada insertado')

        except Exception as e :
            logging.error(f'[!] error funcion :[{self.get_function_name()}] tipo: {e}')

    def bt_atras(self,*argv):
        """funcinon aun no definida revisar backup.py lineas 202 hasta 217"""
        pass    

    def information_text(self,text:str) -> None :

        """
        funcion permite realizar una insetacion de informacion de tipo str
        primeramente limpia el elemento y luego inserta los datos de la variable
        asignda text

        arg:
            None

        return:
            None

        """
        enviar_informacion = self.wait.until(EC.presence_of_element_located((By.XPATH, CONFIG['insertar'])))
        enviar_informacion.clear() 
        enviar_informacion.send_keys(text)

    def information_numeric(self,numeric:int) -> None:
        """
        funcion permite realizar una insetacion de informacion de tipo int
        primeramente limpia el elemeto y luego inserta los datos de la variable
        asignda numeric

        arg:
            None

        return:
            None

        """
        enviar_informacion = self.wait.until(EC.presence_of_element_located((By.XPATH, CONFIG['insertar'])))
        enviar_informacion.clear() 
        enviar_informacion.send_keys(numeric) 
            
    def information_calendar(self,calendario:Fecha) -> bool:
        
        """
        funcion insertar informacion de tipo objeto calendario o Fecha
        
        arg:
            calendario: 
                recibe un objeto de tipo calendario el cual lleva dia,mes,anio

        return:
            bool
        """

        self.contador_preguntas(forzar_tiempo=True)

        try:
            # Usa los atributos de calendario para ingresar la fecha
            dia_input = self.wait.until(EC.presence_of_element_located((By.XPATH,CONFIG['dia'])))
            dia_input.clear()
            dia_input.send_keys(calendario.dia)

            mes_input = self.wait.until(EC.presence_of_element_located((By.XPATH, CONFIG['mes'])))
            mes_input.clear()
            mes_input.send_keys(calendario.mes)

            anio_input = self.wait.until(EC.presence_of_element_located((By.XPATH, CONFIG['anio'])))
            anio_input.clear()
            anio_input.send_keys(calendario.anio)

            logging.info('[+] informacion de calendario insertada')

        except NoSuchElementException as e:
            logging.error(f'error funcion: [{self.get_function_name()}] tipo: {str(e)}')
            return False

    def seleccionar(self,opcion:str) -> bool:
        """ 
        funcion permite poder seleccionar ona opcion del menu de tipo radiobutton 
        args:
            opcion:
                seleciona las opciones que aparescan en el formulario
                las cuales son Interno y Externo
        return:
            bool
        """
        self.contador_preguntas(forzar_scroll_tiempo=True)
        try:
            interno_radio = self.wait.until(EC.element_to_be_clickable((By.XPATH,CONFIG['seleccion'].replace('$',opcion))))
            interno_radio.click()
            logging.info('[+] seleccion exitosa')
            return True
    
        except Exception as e:
            logging.error(f'[!] error funcion: [{self.get_function_name()}] tipo: {str(e)}')
            return False

    def multiple_menu(self,submenu:int,opcion:str) -> None:
        """
        funcion permite seleccionar multiples menus detectando todos 
        los elementos en una lista y buscando por indice numerico
        que submenu busca 

        args:
            submenu: 
                permite indetificar que submenu desplegar 
                requiero un dato de tipo entero int

            opcion:
                insertar la opcion o el valor del 
                submenu actual abierto

        return:
            None
                
        """
        self.contador_preguntas(forzar_scroll_tiempo=True)

        try:

            """localiza el elemento y insetar la opcion del menu desplegado"""
            localizar_menus = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,CONFIG['menu'])))
            localizar_menus[submenu].click()
            self.opcion_menu(opcion=opcion)

        except Exception as e:
            logging.error(f'error funcion: [{self.get_function_name}] tipo: {e}')

    def buscar_iframe(self) -> bool:
        """
        funcion permite localizar el cuadro de diaglogo de google drive
        para poder mover una imagen arrastrando

        args:
            None

        return:
            bool
        """
        
        # self.contador_preguntas(forzar_tiempo=True)

        try:
            """busca el elemento iframe"""
            espera_iframe = self.wait.until(lambda d:(time.sleep(1),d.find_element(By.XPATH,CONFIG['iframe']))[1])
            self.driver.switch_to.frame(espera_iframe) # cambia de contenido al iframe
            """------------------------"""
            logging.info('[+] buscando iframe y cambio de contexto')

            """extraer el texto para ver si ya existe el elemento en el dom"""
            extraer_texto_Examinar = self.wait.until(lambda d:(time.sleep(4),d.find_element(By.XPATH,CONFIG['examinar']))[1]).text
            self.driver.switch_to.default_content() # regresar al contenido principal
            """------------------------------------------------------------"""
            logging.info('[+] extraccion de informacion de boton examinar')

            if isinstance(extraer_texto_Examinar,str):
                logging.info('[+] iteraccion con el iframe exitosa')
                return True
            
            logging.error(f'[!] error funcion: [{self.get_function_name()}] tipo: {str(e)}')
            return False
        
        except (TimeoutException,Exception) as e:
            logging.error(f'error funcion: [{self.get_function_name()}] tipo: {str(e)}')

    def verificar_imagen_subida(self,imagen:int):
        try:
            dominiodrive = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.KdVr9e.oyDRHc')))
            total_elementos = len(dominiodrive)
            # logging.info(f'[+] total elementos : {total_elementos} original: {pos_original} modificacion: {pos_mod}')

            url_extraction = dominiodrive[int(imagen)-1].get_attribute('data-view-file-link')

            # logging.info(f'[+] total elementos : {total_elementos} original: {pos_original} modificacion: {pos_mod}')
            if self.componente._uploaded_file_verification(esquema=url_extraction):
                logging.info('[+] imagen subida exitosamente')
                    
        except Exception as e:
            logging.error(f'[!] error funcion [{self.get_function_name()}] tipo:{e}')

    def enviar(self):
        try:

            fin = WebDriverWait(self.driver,60)

            localizar_bt_enviar = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.l4V7wb.Fxmcue')))
            localizar_bt_enviar[1].click()

            fin_formulario = fin.until(EC.presence_of_element_located((By.CSS_SELECTOR,".vHW8K"))).text

            if isinstance(fin_formulario,str):
                logging.info('[+] envio formulario exitoso')

        except Exception as e :
            logging.info(f'[+] error funcion: [{self.get_function_name()}] tipo: {e}')

    """
    Funciones no usadas
        Descripcion:
        las funciones que estan comentadas no se estan usando por ahora
        o son funciones que se usan de ejemplos
    """

    # def elements_get(self,css_selector):
    #     try:
    #         return self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
    #     except TimeoutException:
    #         return []  # Devolver lista vacía en caso de no encontrar elementos
    # def buttonx(self,item:int):
    #     css_button_upload = '.E6FpNe.Ce1Y1c'
    #     try:
    #         """preiona el boton de subir contenido"""
    #         time.sleep(5)
    #         button_subir = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,css_button_upload))).click()
    #         """----------------------------------"""
    #         extraer_texto_Examinar = self.buscar_iframe()
    #         if extraer_texto_Examinar:
    #             if self.componente._drag_and_drop():
    #                 self.file_successfully_uploaded(posicion=item)

    #     except (TimeoutException,Exception) as e:
    #         print(f'error:{str(e)}')

    #         # print('[*] intentando borrar imagen actual...')

    #         # if self._botonCerrar():
    #         #     self.buttonx(item)
    #         #     print('[*] imagen borrada exitosamente...')
    #         # else:
    #         #     print('[*] fallo al borrar imagen........')
                        
    # def upload(self,iteraciones,force=False):

    #     css_button_upload = '.E6FpNe.Ce1Y1c'
    #     xpath_iframe = '/html/body/div[3]/div[2]/div/iframe'
    #     xpath_examinar = '/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div/button/span'

    #     # for item in range(iteraciones):
    #     try:

    #         if isinstance(iteraciones,int):
    #             self.buttonx(iteraciones)

    #         # if force:
    #         #     self.agregar(4)

    #     except TimeoutException:
    #         print("[!] Timeout: No se pudo encontrar el elemento en la iteración ")
    #     except NoSuchElementException:
    #         print("[!] NoSuchElement: No se pudo localizar el elemento en la iteración")
    #     except AttributeError as e:
    #         print(f"[!] AttributeError: {e}")
    #     except Exception as e:
    #         print(f"[!] Error inesperado: {e}")

    # def _Verify_file_upload_correctly(self):
    #     verificacion = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.yP1fJf')))
    #     if verificacion:
    #         buscar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.KdVr9e.oyDRHc')))
    #         esquema = buscar.get_attribute('data-view-file-link')
    #         return esquema
    #     return 'example.com'

    # def file_successfully_uploaded(self,posicion:int)-> None:
    #     try:
    #         imagencargada = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.yP1fJf')))
    #         total_imagenes_cargadas = len(imagencargada)
    #         if total_imagenes_cargadas > 0:
    #             dominiodrive = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.KdVr9e.oyDRHc')))
    #             url_extraction = dominiodrive[posicion].get_attribute('data-view-file-link')
    #             self.componente._uploaded_file_verification(esquema=url_extraction)

    #     except (TimeoutException,Exception) as e:
    #         raise exception_file_successfully_uploaded(f"error al procesar la verficacion de archivo error: {str(e)}")

    # def _dom_elements_questions(self,elemento_padre):
    #     try:
    #         time.sleep(1)
    #         return self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,elemento_padre)))
    #     except TimeoutException:
    #         return False
        
    # def sandbox_elements(self,elemento):
    #     modelo = self._dom_elements_questions(elemento)[0]
    #     modelo.find_elements()

    # def _add_file_drive(self,*argv,**kwargs) -> str:
    #     try:
    #         eliminar_archivo = self._botonCerrar()
    #         if kwargs.get('activate_mode_test') is True:
    #             if eliminar_archivo is True and kwargs.get('botonCerrar') is True:
    #                 verification_exists_button = self._botonSubir()
    #                 if verification_exists_button:
    #                     botonExaminar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.fFW7wc.XKSfm-Sx9Kwc.picker-dialog')))
    #                     self.driver.implicitly_wait(5)
    #                     # self.componente._drag_and_drop()
    #                     # verify_file = self._Verify_file_upload_correctly()
    #                     # self.componente._uploaded_file_verification(esquema=verify_file)
    #                     return True

    #         if eliminar_archivo:
    #             verification_exists_button = self._botonSubir()
    #             if verification_exists_button:
    #                 botonExaminar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.fFW7wc.XKSfm-Sx9Kwc.picker-dialog')))
    #                 self.driver.implicitly_wait(5)
    #                 self.componente._drag_and_drop()
    #                 verify_file = self._Verify_file_upload_correctly()
    #                 self.componente._uploaded_file_verification(esquema=verify_file)
    #                 return True            

    #         self._botonSubir()
    #         botonExaminar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.fFW7wc.XKSfm-Sx9Kwc.picker-dialog')))
    #         self.driver.implicitly_wait(5)

    #         # /html/body/div[3]/div[2]/div


    #         # self.componente._drag_and_drop()
    #         # verify_file = self._Verify_file_upload_correctly()
    #         # self.componente._uploaded_file_verification(esquema=verify_file)

    #     except TimeoutException:
    #         raise GoogleFormularioException('Fallo en relizar los clicks')

    # def eliminar(self):
    #     googledriverimagen = '.KdVr9e.oyDRHc'
    #     try:
    #         googledriverimagen = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,googledriverimagen)))
    #         total_de_elemetos = len(googledriverimagen)
    #         if total_de_elemetos > 0:
    #             botonCerrar = self.driver.find_elements(By.CSS_SELECTOR, '.XuQwKc')
    #             for item in range(len(botonCerrar)):
    #                 botonCerrar[item].click()
    #                 print('[*] elimiando elemeto: ',item)

    #     except TimeoutException:
    #         print('[*] Campo limpio de imagenes')

    # def tranferencia_multiples_imagenes(self,subir_imagenes:int):
    #     for imagen in range(subir_imagenes):
    #         localizar_bt_subir = self.wait.until(lambda d:(time.sleep(5), d.find_element(By.CSS_SELECTOR,CONFIG['bt_subir']))[1])
    #         localizar_bt_subir.click()

    #         localizar_dialog_drive = self.wait.until(lambda localizar_bt_subir:localizar_bt_subir.find_element(By.CSS_SELECTOR,CONFIG['dialogdrive']))
    #         self.driver.implicitly_wait(5)

    #         mover_imagen = self.componente._drag_and_drop()
    #         if mover_imagen:
    #             imagencargada = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,CONFIG['localizar_imagenes'])))
    #             total_imagenes_cargadas = len(imagencargada)
    #             if total_imagenes_cargadas > 0:
    #                 time.sleep(4)
    #                 localizar_dominiodrive_imagen_actual = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,CONFIG['imagen_actual'])))
    #                 url_extraction = localizar_dominiodrive_imagen_actual[imagen].get_attribute('data-view-file-link')
    #                 transferencia_exitosa = self.componente._uploaded_file_verification(esquema=url_extraction)
    #                 if transferencia_exitosa:
    #                     logging.info('[+] transferencia de archivo exitoso')

