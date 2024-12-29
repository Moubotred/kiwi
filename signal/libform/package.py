import pyautogui
from urllib.parse import urlsplit

class EmpaquetadoManual:

    @staticmethod
    def _drag_and_drop():

        posicion_inicial = pyautogui.position()

        x_inicial = 1080
        y_inicial = 511
        x_destino = x_inicial - 750  # Nuevo punto en x
        y_destino = y_inicial        # Nuevo punto en y (sin cambios)


        # Mueve el cursor a la posición inicial
        pyautogui.moveTo(x_inicial, y_inicial)

        # Presiona el botón izquierdo del ratón
        pyautogui.mouseDown(button='left')

        # Mueve el cursor 200 píxeles a la derecha mientras se mantiene presionado el botón
        pyautogui.dragTo(x_inicial - 750, y_inicial, duration=1)
        
        posicion_final = pyautogui.position()

        if posicion_final != (x_destino, y_destino):
            return False
        
        return True


    @staticmethod
    def _uploaded_file_verification(esquema: str) -> bool:
        """
        Verifica que el dominio en el esquema de URL sea 'drive.google.com'.
        """
        try:
            parsed_url = urlsplit(esquema)
            dominio = parsed_url.netloc
            dominio_esperado = 'drive.google.com'
            if dominio == dominio_esperado:
                return True
            else:
                return False

        except Exception as e:
            print('error: ',e)
            

