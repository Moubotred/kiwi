import asyncio
from utilapirun.syncro import syncro_temporal

async def Directorio(suministro,pwd):
    loop = asyncio.get_running_loop()
    Directorio = await loop.run_in_executor(None, syncro_temporal.Archivo_temporal,suministro,pwd)
