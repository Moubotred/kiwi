from core.event import Event
from objetos import Config

class form(Event):
    def __init__(self, config: Config) -> None:
        super().__init__(config)