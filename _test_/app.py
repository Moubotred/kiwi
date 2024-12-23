from GoFom import GoogleForm, FormConfig, GoogleFormException
from WidgetGestor import Configuraciones
from PyQt5.QtWidgets import QApplication
import threading

def Navegador():
    """Función que se ejecutará en un hilo sbeparado"""
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

def Widget():
    app = QApplication([])
    window = Configuraciones()
    window.show()
    app.exec()

# Crear e iniciar el hilo para Navegador()
navegador_thread = threading.Thread(target=Navegador)
navegador_thread.start()

# Ejecutar Widget() en el hilo principal
Widget()