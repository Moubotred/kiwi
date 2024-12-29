import asyncio
from utilapirun.syncro import syncro_convertidor

async def ConvertirPDF(suministro):
    if suministro:
        loop = asyncio.get_running_loop()
        
        # Ejecutar la conversión en un subproceso para no bloquear el bucle de eventos
        pdf_filename = await loop.run_in_executor(None, syncro_convertidor.Convertir_pdf, suministro)
        return pdf_filename
    else:
        return False
