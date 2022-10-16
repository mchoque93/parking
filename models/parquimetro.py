from dataclasses import dataclass, field
from models.plaza import Plaza

@dataclass
class Parquimetro:
    tarifa:float
    lista_plazas: list =field(default_factory=lambda: [Plaza(id) for id in range(1, 87+1)])