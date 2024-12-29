from urllib.parse import unquote

from fastapi import FastAPI, HTTPException
from apis.Luzdelsur import LuzdelsurRecibo
from apis.Envioshasber import SistemaEnviosHasber
from apis.Clasificador import ImageClassifier
from fastapi import FastAPI, UploadFile, File
import os
from constantes import pydirecion
from typing import List
from pydantic import BaseModel

import json


app = FastAPI()

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
async def predict_batch(suministro:bytes):

    json_string = suministro.decode("utf-8")
    datos = json.loads(json_string)
    
    model_path = os.path.join('/home/kimshizi/Proyects/monitoring/py/apis','modelo_convertido.tflite')
    labels_path = os.path.join('/home/kimshizi/Proyects/monitoring/py/apis','labels.txt')

    # Inicializar el clasificador
    classifier = ImageClassifier(model_path=model_path, labels_path=labels_path)

    # Obtener lista de imágenes

    image_dir = os.path.join(os.path.expanduser('~'),'imagenes',datos['usuario'])
    # image_files = sorted(os.listdir(image_dir))
    # image_files = os.listdir(image_dir)

    # image_files = suminsitro # imagen para ver la predicion

    predicti = {}

    # Predecir las imágenes y obtener los resultados
    predictions = classifier.predict_batch(image_dir)

    try:
        # Imprimir los resultados
        # for image_file, prediction in zip(image_files, predictions):
        
        predicti[image_dir.split('/')[-1]] = predictions

        return {"suministro": predicti}

    except Exception as e:
        # print(f"Predicción para la imagen {image_file}: {prediction}")
        # predicti.append(prediction)
        raise HTTPException(status_code=500, detail='o se pudo realizar la prediccion')

    # return {"predictions": image_files}