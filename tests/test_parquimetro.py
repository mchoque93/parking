from datetime import datetime
from unittest import TestCase

from models.parquimetro import Parquimetro
from models.plaza import Ocupacion
from services.administrar_parquimetro import AdministrarParking


class TestValidarTarea(TestCase):

    def setUpClass(cls) -> None:
        cls.administrar_parking = AdministrarParking()

    def setUp(self) -> None:
        self.parquimetro = Parquimetro(9)

    def test_validar_tamano_parquimetro(self):
        assert (len(self.parquimetro.lista_plazas) == 87)

    def test_validar_aparcar_coche(self):
        parquimetro = Parquimetro(9)
        # quitar esto-> como hacer para no tener que inicializar el objeto??
        adm = AdministrarParking()
        start_date = datetime(2022, 10, 16, 10, 53, 23, 459111)
        plaza = adm.aparcar_coche("123", parquimetro, start_date)
        assert (plaza.id in range(0, 87))
        assert (plaza.estado == Ocupacion.OCUPADO)

    def test_desaparcar_coche(self):
        parquimetro = Parquimetro(9)
        # quitar esto-> como hacer para no tener que inicializar el objeto??
        adm = AdministrarParking()
        start_date = datetime(2022, 10, 16, 10, 53, 23, 459111)
        plaza = adm.aparcar_coche("123", parquimetro, start_date)
        end_date = datetime(2022, 10, 16, 14, 53, 23, 459111)
        importe = adm.desaparcar_coche("123", parquimetro, end_date)
        assert plaza.estado == Ocupacion.LIBRE
        assert plaza.coche is None
        diff = end_date - start_date
        duration_in_s = diff.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]
        assert (importe == parquimetro.tarifa * hours)

    def test_calcular_total_importe(self):
        parquimetro = Parquimetro(9)
        adm = AdministrarParking()

        start_date_1 = datetime(2022, 10, 16, 10, 53, 23, 459111)
        adm.aparcar_coche("123", parquimetro, start_date_1)
        end_date_1 = datetime(2022, 10, 16, 14, 53, 23, 459111)
        importe_1 = adm.desaparcar_coche("123", parquimetro, end_date_1)

        start_date_2 = datetime(2022, 10, 16, 6, 53, 23, 459111)
        adm.aparcar_coche("223", parquimetro, start_date_2)
        end_date_2 = datetime(2022, 10, 16, 19, 53, 23, 459111)
        importe_2 = adm.desaparcar_coche("223", parquimetro, end_date_2)

        assert (adm.total_importe(parquimetro) == importe_1 + importe_2)

    def test_validar_matricula_coche_desaparcado(self):
        parquimetro = Parquimetro(9)
        adm = AdministrarParking()
        start_date_1 = datetime(2022, 10, 16, 10, 53, 23, 459111)
        adm.aparcar_coche("123", parquimetro, start_date_1)
        end_date_1 = datetime(2022, 10, 16, 14, 53, 23, 459111)
        with self.assertRaises(ValueError):
            adm.desaparcar_coche("224", parquimetro, end_date_1)

    def test_calcular_plazas_libres(self):
        parquimetro = Parquimetro(9)
        adm = AdministrarParking()
        start_date_1 = datetime(2022, 10, 16, 10, 53, 23, 459111)
        adm.aparcar_coche("123", parquimetro, start_date_1)
        start_date_1 = datetime(2022, 10, 16, 10, 53, 23, 459111)
        adm.aparcar_coche("222", parquimetro, start_date_1)
        start_date_1 = datetime(2022, 10, 16, 10, 53, 23, 459111)
        adm.aparcar_coche("333", parquimetro, start_date_1)

        num = adm.num_puestos_libres(parquimetro)

        assert (num == 84)

    def test_coche_ya_aparcado(self):
        parquimetro = Parquimetro(9)
        adm = AdministrarParking()
        start_date_1 = datetime(2022, 10, 16, 10, 53, 23, 459111)
        adm.aparcar_coche("123", parquimetro, start_date_1)
        start_date_1 = datetime(2022, 10, 16, 10, 53, 23, 459111)
        with self.assertRaises(ValueError):
            adm.aparcar_coche("123", parquimetro, start_date_1)

    def test_validar_importe_total_misma_plaza(self):
        parquimetro = Parquimetro(9)
        adm = AdministrarParking()

        start_date_1 = datetime(2022, 10, 16, 10, 53, 23, 459111)
        adm.aparcar_coche("123", parquimetro, start_date_1)
        end_date_1 = datetime(2022, 10, 16, 14, 53, 23, 459111)
        importe_1 = adm.desaparcar_coche("123", parquimetro, end_date_1)

        start_date_2 = datetime(2022, 10, 18, 6, 53, 23, 459111)
        adm.aparcar_coche("222", parquimetro, start_date_2)
        end_date_2 = datetime(2022, 10, 18, 19, 53, 23, 459111)
        importe_2 = adm.desaparcar_coche("222", parquimetro, end_date_2)

        assert adm.total_importe(parquimetro) == importe_1 + importe_2
