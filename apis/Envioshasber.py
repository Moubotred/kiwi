# whatsapp/apis/Envioshasber.py

import os
import httpx
import aiofiles



from utilapirun.descargar import Descargar
from utilapirun.convertidor import ConvertirPDF
from utilapirun.directorio import Directorio

from constantes import pydirecion

async def SistemaEnviosHasber(suministro:str) -> str:
    # URL de la solicitud POST
    url = "https://hasbercourier.easyenvios.com/modulos/controlador/herramientas/con_cargosenvios.php?tabla=congrid_envio_seguimiento"

    # Encabezados de la solicitud
    headers = {
        "Host": "hasbercourier.easyenvios.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://hasbercourier.easyenvios.com",
        "Referer": "https://hasbercourier.easyenvios.com/modulos/seguimiento.php",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
        "Connection": "keep-alive"
    }

    # Datos del cuerpo de la solicitud (POST data)
    data = {
        "ciacodigo": "17",
        "succodigo": "001",
        "asenombre": "",
        "codigoenvio": "",
        "codigounico": f"{suministro}",
        "asepropuesta": "",
        "strnrodocumento": "",
        "page": "1",
        "rows": "10",
        "sort": "a.asenumero",
        "order": "asc"
    }

    # Realiza la solicitud POST de manera asíncrona
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, data=data)
            if response.status_code == 200:
                data = response.json()

                # Extraer todas las filas de datos
                rows = data['rows']
                seleccionar = [row['artnombre'] == 'CARTAS / REEMPLAZO DE MEDIDOR EMPRESAS' for row in rows]

                if any(seleccionar):
                    descargas = pydirecion.descargas
                    home = os.path.expanduser('~/')
                    directorio = os.path.abspath(os.path.join(home,descargas))
                    UrlImage = str(data['rows'][seleccionar.index(True)].get('imagen1'))
                    response_data = await client.get(UrlImage)
                    formato_TIF = await Descargar(response=response_data,nombre_archivo=suministro)
                    formato_PDF = await ConvertirPDF(suministro=formato_TIF)
                    await Directorio(formato_PDF,directorio)
                    return formato_PDF
                
                else:
                    return '⚒️ actividad no programada 🥷'
                
            elif response.status_code != 200:
                return '⚠️ la web actualizo el codigo informar inmediatamente al adminstrador del Bot Miharu ☣️'
                    
                

        except httpx.HTTPStatusError as e:
            return f"Error en la solicitud: {e.response.status_code}"
        except httpx.RequestError as e:
            return f"Error de conexión: {e}"