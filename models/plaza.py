from enum import IntEnum
from dataclasses import dataclass, field

from models.coche import Coche


class Ocupacion(IntEnum):
    LIBRE = 0
    OCUPADO =1

@dataclass
class Plaza:
    id: float
    coche: Coche = None
    estado: Ocupacion = Ocupacion.LIBRE
    lista_importes:list = field(default_factory=list)

