
from urllib.parse import unquote

import sys
from PyQt5.QtWidgets import QApplication

from fastapi import FastAPI, HTTPException
from apis.Luzdelsur import LuzdelsurRecibo
from apis.Envioshasber import SistemaEnviosHasber
from apis.Clasificador import ImageClassifier
from fastapi import FastAPI, UploadFile, File
import os
from constantes import pydirecion
from typing import List
from pydantic import BaseModel
# from sig.example import IntegratedWindow
import json


app = FastAPI()

usuario_dat = []
imagenes_dat = []

class path_prediccion(BaseModel):
    usuario: str
    file: str

home = os.path.expanduser('~/')
proyecto = pydirecion.descargas
descargas = os.path.join(home,proyecto)

@app.get("/recibo")
async def recibo(suministro: str):
    if not suministro:
        raise HTTPException(status_code=400, detail="No se proporcionó el número de suministro")
    
    resultado = await LuzdelsurRecibo(suministro)

    # Verifica si el archivo se generó
    if resultado and os.path.exists(os.path.join(descargas,'png',resultado)):

        return {"suministro": resultado}
    
    else:
        raise HTTPException(status_code=500, detail=resultado)

@app.get("/actividad")
async def actividad(suministro: str):
    if not suministro:
        raise HTTPException(status_code=400, detail="No se proporcionó el número de suministro")
    
    resultado = await SistemaEnviosHasber(suministro)

    # Verifica si el archivo se generó
    if resultado and os.path.exists(os.path.join(descargas,'pdf',resultado)):

        return {"suministro": resultado}
    
    else:
        raise HTTPException(status_code=500, detail=resultado)

@app.get("/prediccion")
async def prediccion(suministro:bytes):

    json_string = suministro.decode("utf-8")
    datos = json.loads(json_string)

    global usuario_dat 
    global imagenes_dat

    usuario = list(datos.keys())[0]
    imagenes = list(datos.values())[0]

    usuario_dat.append(usuario)

    # path_inicial = os.getcwd()

    model_path = os.path.join('/home/kimshizi/Documents/pqt5/apis','modelo_convertido.tflite')
    labels_path = os.path.join('/home/kimshizi/Documents/pqt5/apis','labels.txt')

    # # Inicializar el clasificador
    classifier = ImageClassifier(model_path=model_path, labels_path=labels_path)

    try:
        prediccion = classifier.predict_batch(usuario=usuario,fileNames=imagenes)
        imagenes_dat.append(prediccion)
        # prediccion = 'Holi'
        return {"suministro":prediccion}
    
    except Exception as e:
        # print(f"Predicción para la imagen {image_file}: {prediction}")
        # predicti.append(prediction)
        raise HTTPException(status_code=500, detail='no se pudo realizar la prediccion')

@app.post("/reenviar_data")
async def retrieve_data():

    """
    Endpoint para enviar los datos almacenados a quien lo solicite.
    """

    if not usuario_dat and not imagenes_dat:
        raise HTTPException(status_code=404, detail="datos no disponibles !!!")
    return {"status": "success", "data": {usuario_dat[0]:imagenes_dat[0]}}