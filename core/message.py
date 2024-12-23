import time
from functools import wraps
from colorama import Fore, Back, Style

# funciones : verde
# accionadores : amarillo

def flagmessage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        tiempo_ejecucion = round(end_time - start_time, 0)
        if result:
            print(f"{Fore.GREEN}[*] Successful widget: {func.__name__} time execution:{tiempo_ejecucion} segundos")
        else:
            print(f"{Fore.RED}[x] Failed widget : {func.__name__} time execution:{int(end_time - start_time)} segundos")
        return result    
    return wrapper

def flagmessagefunc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        tiempo_ejecucion = round(end_time - start_time, 0)
        if result:
            print(f"{Fore.YELLOW}[*] Successful function: {func.__name__} time execution:{tiempo_ejecucion} segundos")
        else:
            print(f"{Fore.MAGENTA}[x] Failed function : {func.__name__} time execution:{int(end_time - start_time)} segundos")
        return result    
    return wrapper

def popmessage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        tiempo_ejecucion = round(end_time - start_time, 0)
        if isinstance(result,list):
            print(f"[*] Successful function: {func.__name__} time execution:{tiempo_ejecucion} segundos")
            print(f'[*] number elements: {len(result)}')
        else:
            print(f"[x] Failed function : {func.__name__} time execution:{int(end_time - start_time)} segundos")
        return result    
    return wrapper

def scroll(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        tiempo_ejecucion = round(end_time - start_time, 0)
        if isinstance(result,list):
            print(f"[*] Successful function: {func.__name__} time execution:{tiempo_ejecucion} segundos")
            print(f'[*] number elements: {len(result)}')
        else:
            print(f"[x] Failed function : {func.__name__} time execution:{int(end_time - start_time)} segundos")
        return result    
    return wrapper
