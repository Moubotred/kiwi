import os

path = os.getcwd()
path_back = os.path.dirname(path)
path_absolute = os.path.join(path_back,'imagenes','i-o')

if os.path.abspath(path_absolute):
    print(path_absolute)
else:
    print('no existe ruta')