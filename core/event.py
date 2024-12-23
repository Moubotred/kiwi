from objetos import Fecha
from objetos import Config
from core.base import Base
from core.widgets import Widgets
from core.message import flagmessage,flagmessagefunc
from typing import Any, Dict, Callable, Type,Optional

class Event(Widgets):
    def __init__(self,config:Config) -> None:
        super().__init__(config)

        self.handlers: Dict[str, Dict[Type, Callable[[Any], None]]] = {

            'suministro': {
                int: self.information_numeric
            },
            'informacion': {
                str: self.information_text
            },
            'medidor': {
                int: self.information_numeric
            },
            'calendario': {
                Fecha:self.information_calendar
            }
        }

    # @flagmessagefunc
    def buttons(self,*argumento:str,**kawrgs:False) -> bool:

        if kawrgs.get('menu') is True:
            self.abrir_menu()
            self.opcion_menu(opcion=argumento[0])
            return True
            
        if kawrgs.get('siguiente') is True:
            self.bt_siguiente()
            return True

        if kawrgs.get('seleccion') is True:
            self.seleccionar(argumento[0])
            return True
            
    # @flagmessagefunc
    def insert_information(self,**kwargs):
        self.contador_preguntas(forzar_scroll_tiempo=True)
        for field, value in kwargs.items():
            # print(field,'||||',value,'\n')
            if field in self.handlers:
                # print(field,'|||',self.handlers,'\n')
                field_handlers = self.handlers[field]
                # print(field_handlers,'\n')
                for expected_type, handler in field_handlers.items():
                    # print(expected_type,handler,'\n')
                    if isinstance(value, expected_type):
                        # print(value,'\n')
                        handler(value)
                        return True
                        break
                else:
                    print(f"[!] No hay un manejador para el tipo '{type(value).__name__}' en el campo '{field}'.")
            else:
                print(f"[!] No hay un manejador definido para el campo '{field}'.")
            