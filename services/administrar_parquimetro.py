from dataclasses import dataclass

from models.coche import Coche
from models.parquimetro import Parquimetro
from models.plaza import Ocupacion, Plaza
import datetime



@dataclass
class AdministrarParking():


    def aparcar_coche(self, matricula:str, parquimetro: Parquimetro, start_date: datetime):
        plaza=next((plaza for plaza in parquimetro.lista_plazas if plaza.estado==Ocupacion.LIBRE),None)
        self.validar_ocupacion(plaza)
        self.validar_coche_ya_aparcado(matricula, parquimetro)
        #start_date=datetime.datetime.now()
        self.validar_hora(start_date)
        coche=Coche(matricula, start_date)
        plaza.estado=Ocupacion.OCUPADO
        plaza.coche=coche
        return plaza

    def get_tiempo(self, plaza: Plaza, end_time: datetime):
        #end_time = datetime.datetime.now()
        difference = end_time - plaza.coche.start_date
        duration_in_s = difference.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]
        return hours

    def desaparcar_coche(self, matricula:str, parquimetro: Parquimetro, end_time: datetime):
        plaza=self.get_plaza_matricula(matricula, parquimetro)
        self.validar_desaparcar_coche_no_aparcado(plaza)
        importe=self.get_tiempo(plaza, end_time)*parquimetro.tarifa
        plaza.lista_importes.append(importe)
        plaza.estado=Ocupacion.LIBRE
        plaza.coche=None
        return importe

    def get_plaza_matricula(self, matricula:str, parquimetro: Parquimetro):
        plaza=next((plaza for plaza in parquimetro.lista_plazas if plaza.coche and plaza.coche.placa==matricula), None)
        return plaza

    def total_importe(self, parquimetro: Parquimetro):
        total_importe = sum([sum(plaza.lista_importes) for plaza in parquimetro.lista_plazas])
        return total_importe

    def num_puestos_libres(self, parquimetro: Parquimetro):
        num_puestos_libres=len([plaza for plaza in parquimetro.lista_plazas if plaza.estado==Ocupacion.LIBRE])
        return num_puestos_libres

    def validar_hora(self, start_date):
        if start_date.hour<5 or start_date.hour>20:
            raise ValueError("el parking esta cerrado")

    def validar_ocupacion(self, plaza: Plaza):
        if not plaza:
            raise ValueError("el parking esta lleno")

    def validar_coche_ya_aparcado(self,matricula: str, parquimetro: Parquimetro):
        plaza=self.get_plaza_matricula(matricula, parquimetro)
        if plaza:
            raise ValueError("esta matricula ya esta en este parking")

    def validar_desaparcar_coche_no_aparcado(self, plaza: Plaza):
        if not plaza:
            raise ValueError("el coche no esta aparcado")

