from dataclasses import dataclass
from typing import Optional,Any,Dict
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver



@dataclass
class Tecnico:
    nombre: str

@dataclass
class Suministro:
    numero: str

@dataclass
class Fecha:
    dia: int
    mes: int
    anio: int

@dataclass
class Medidor:
    numero_meidor_antes:int
    numero_meidor_despues:int

@dataclass
class Imagen:
    ruta: Path

@dataclass
class Config:
    url: str = ""
    profile: Optional[Path] = None
    headless: bool = False
    timeout: int = 20

@dataclass
class Widget:
    pass

@dataclass
class FormularioDatos:
    tecnico: Tecnico
    suministro: Suministro
    fecha: Fecha
    medidor: Medidor









