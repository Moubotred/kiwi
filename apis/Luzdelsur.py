# hola :-3
# wwww
import os
import httpx
import base64
import aiofiles
from utilapirun.directorio import Directorio
# from utils.tuning import anime
from utilapirun.syncro.syncro_tunneo import lolis

from getpass import getuser
import asyncio
from constantes import pydirecion

async def LuzdelsurRecibo(suministro):
    # URL de la API
    url = "https://www.luzdelsur.pe/es/VerPagarRecibo/ObtenerImagenBoletaLibre"

    # Payload con el número de suministro
    payload = {
        "request": {
            "Suministro": f"{suministro}"  # Ajusta el número de suministro
        }
    }

    # Encabezados necesarios (incluye la Cookie si es requerida)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.luzdelsur.pe",
        "Referer": "https://www.luzdelsur.pe/es/VerPagarRecibo"
    }

    # Realiza la solicitud POST de manera asíncrona
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload, headers=headers)

        try:

            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                # Convertir la respuesta a JSON
                data = response.json()
                
                imagen_base64 = data['datos']['archivoBase64']

                if not imagen_base64:
                    return '⚒️ el recibo no existe en en la web 🥷'
                
                # Decodificar y guardar la imagen en un archivo de manera asíncrona
                try:
                    descargas = pydirecion.descargas
                    home = os.path.expanduser('~/')
                    directorio = os.path.abspath(os.path.join(home,descargas))
                    archivo = f'{suministro}.png'
                    async with aiofiles.open(archivo, "wb") as img_file:
                        await img_file.write(base64.b64decode(imagen_base64))
                        # await anime(suministro)
                        await lolis(suministro)
                        await Directorio(archivo,directorio)
                        
                    return archivo
                
                except TypeError:
                    return "La API no devolvió una imagen válida en formato base64"
                
            elif response.status_code != 200:
                return '⚠️ la web actualizo el codigo informar inmediatamente al adminstrador del Bot Miharu ☣️'
            
        except httpx.ReadTimeout:
            return '💤 tiempo de solicitud agotada ⏳'