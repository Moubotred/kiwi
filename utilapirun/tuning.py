# uwu 

import asyncio
from utilapirun.syncro import syncro_tunneo

async def anime(suministro):
    loop = asyncio.get_running_loop()
    Directorio = await loop.run_in_executor(None, syncro_tunneo.recibo_anime,suministro)