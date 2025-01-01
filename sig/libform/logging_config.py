import logging

# Configuración básica
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato de los mensajes
    filename="app.log",  # Archivo donde se guardan los logs
    filemode="w"  # 'w' para sobrescribir el archivo cada vez que se ejecuta el script
)

# Alternativamente, para que también se muestren en consola:
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)
