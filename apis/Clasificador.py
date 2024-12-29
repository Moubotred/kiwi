# whatsapp/apis/Clasificacion.py

import os
import platform
import numpy as np
from PIL import Image, ImageOps
import tflite_runtime.interpreter as tflite

class ImageClassifier:
    def __init__(self, model_path, labels_path):
        # Cargar el modelo TFLite
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Obtener detalles de entrada y salida
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Cargar etiquetas
        with open(labels_path, "r", encoding='utf-8') as f:
            self.class_names = f.readlines()
            
        # Parámetros de preprocesamiento de imagen
        self.target_size = (224, 224)
        self.input_shape = (1, 224, 224, 3)
        
    def preprocess_image(self, image_path):
        """Preprocesar una imagen para la predicción"""
        # Abrir y convertir la imagen a RGB
        image = Image.open(image_path).convert("RGB")
        
        # Redimensionar la imagen
        image = ImageOps.fit(image, self.target_size, Image.Resampling.LANCZOS)
        
        # Convertir a array de numpy y normalizar
        image_array = np.asarray(image)
        normalized_image = (image_array.astype(np.float32) / 127.5) - 1
        
        return normalized_image.reshape(self.input_shape)
    
    def predict_single(self, image_path):
        """Predecir la clase para una sola imagen"""
        # Preprocesar la imagen
        input_data = self.preprocess_image(image_path)
        
        # Configurar la entrada al modelo
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        # Realizar la inferencia
        self.interpreter.invoke()

        # Obtener los resultados de la salida
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        # Evitar referencias a los datos internos de los tensores
        output_data = np.squeeze(output_data)  # Asegurarse de que la salida sea un array 1D

        # Obtener la clase con mayor probabilidad
        index = np.argmax(output_data)
        
        # Retornar el nombre de la clase sin índice
        return self.class_names[index].split()[1]

    def predict_batch(self, image_paths):
        """Predecir las clases para múltiples imágenes (de manera secuencial)"""

        home = os.path.expanduser('~')
        # path = os.path.join(home,image_paths) if 'Debian' in platform.version() else os.path.join(home,'monitoring/descargas/procesar')

        # Crea el directorio si no existe
        if not os.path.exists(image_paths):
            os.makedirs(os.path.dirname(image_paths),exist_ok=True)

        # results = []
        # for image_path in image_paths:
        result = self.predict_single(image_paths)
            # results.append(result)
        return result

def main():
    # Inicializar el clasificador
    classifier = ImageClassifier(
        model_path=os.path.join(os.getcwd(), 'modelo_convertido.tflite'),
        labels_path=os.path.join(os.getcwd(), 'labels.txt')
    )
    
    # Obtener lista de imágenes
    image_dir = '/home/kimshizi/Downloads/clasificador/procesar'
    image_files = sorted(os.listdir(image_dir))

    # Predecir las imágenes y obtener los resultados
    predictions = classifier.predict_batch(image_files)
    
    # Imprimir los resultados
    for image_file, prediction in zip(image_files, predictions):
        print(f"Predicción para la imagen {image_file}: {prediction}")

# if __name__ == "__main__":
    # main()
