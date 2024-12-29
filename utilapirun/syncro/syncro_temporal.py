import os
import shutil

def Archivo_temporal(suministro, pwd):
    # Verifica si el directorio base existe, si no, lo crea
    os.makedirs(pwd, exist_ok=True)

    # Asegura que el archivo suministro incluya una ruta absoluta
    suministro_path = os.path.abspath(suministro)

    if not os.path.isfile(suministro_path):
        # print(f"El archivo '{suministro}' no existe.")
        return False

    # Clasifica según la extensión
    if suministro.endswith('.pdf'):
        subcarpeta = 'pdf'

    elif suministro.endswith('.png'):
        subcarpeta = 'png'

    else:
        # print(f"Extensión no soportada para el archivo '{suministro}'.")
        return False

    # Crea el directorio de destino si no existe
    carpeta_destino = os.path.join(pwd, subcarpeta)
    os.makedirs(carpeta_destino, exist_ok=True)

    # Mueve el archivo al destino
    nuevo_path = os.path.join(carpeta_destino, os.path.basename(suministro))
    shutil.move(suministro_path, nuevo_path)

    # print(f"Archivo '{suministro}' movido a '{nuevo_path}'.")

    # Elimina el archivo relacionado (.TIF) si es necesario
    tif_path = suministro_path.replace('.pdf', '.TIF')
    if os.path.exists(tif_path):
        os.remove(tif_path)
        # print(f"Archivo relacionado '{tif_path}' eliminado.")

    return True