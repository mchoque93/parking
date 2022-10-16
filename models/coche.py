from dataclasses import dataclass
from datetime import datetime


@dataclass
class Coche:
    placa: str
    start_date: datetime

