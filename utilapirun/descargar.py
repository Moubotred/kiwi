import httpx
import aiofiles

async def Descargar(response,nombre_archivo):

    nombre_archivo = f'{nombre_archivo}.TIF'

    # Guardar el contenido en un archivo de manera asíncrona
    async with aiofiles.open(nombre_archivo, 'wb') as archivo:
        await archivo.write(response.content)
        return nombre_archivo
    

