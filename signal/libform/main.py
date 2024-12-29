from libform.event import Event
from libform.const import Config
from PyQt5.QtCore import QThread, pyqtSignal

class executionWinForm(Event):
    def __init__(self, parent:None, config: Config) -> None:
        super(executionWinForm,self).__init__(parent,config)