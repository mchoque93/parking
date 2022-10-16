from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from models.parquimetro import Parquimetro
from models.plaza import Ocupacion
from services.administrar_parquimetro import AdministrarParking


@patch("services.administrar_parquimetro.datetime")
class TestValidarTarea(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        '''
        Se inicializan una vez para todos los tests -> 1 vez
        :return:
        '''
        cls.administrar_parking = AdministrarParking()
        cls.start_date = datetime(2022, 10, 16, 10, 53, 23, 459111)
        cls.end_date = datetime(2022, 10, 16, 14, 53, 23, 459111)

    def setUp(self) -> None:
        '''
        Se inicializa una vez por test -> 8 veces
        :return:
        '''
        self.parquimetro = Parquimetro(9)

    def test_validar_tamano_parquimetro(self, _):
        self.assertEqual(len(self.parquimetro.lista_plazas), 87)

    def test_validar_aparcar_coche(self, datetime_mock):
        datetime_mock.datetime.now.return_value = self.start_date
        plaza = self.administrar_parking.aparcar_coche("123", self.parquimetro)

        self.assertIn(plaza.id, range(0, 87))
        self.assertEqual(plaza.estado, Ocupacion.OCUPADO)
        self.assertEqual(plaza.coche.placa, "123")
        self.assertEqual(plaza.coche.start_date, self.start_date)

    def test_desaparcar_coche(self, datetime_mock):
        datetime_mock.datetime.now.return_value = self.start_date
        plaza = self.administrar_parking.aparcar_coche("123", self.parquimetro)
        datetime_mock.datetime.now.return_value = self.end_date
        importe = self.administrar_parking.desaparcar_coche("123", self.parquimetro)

        self.assertEqual(plaza.estado, Ocupacion.LIBRE)
        self.assertIsNone(plaza.coche)
        self.assertEqual(importe, 36)

    def test_calcular_total_importe(self, datetime_mock):
        datetime_mock.datetime.now.return_value = self.start_date
        self.administrar_parking.aparcar_coche("123", self.parquimetro)
        self.administrar_parking.aparcar_coche("223", self.parquimetro)
        datetime_mock.datetime.now.return_value = self.end_date
        importe_1 = self.administrar_parking.desaparcar_coche("123", self.parquimetro)
        importe_2 = self.administrar_parking.desaparcar_coche("223", self.parquimetro)

        self.assertEqual(self.administrar_parking.total_importe(self.parquimetro), importe_1 + importe_2)

    def test_validar_matricula_coche_desaparcado(self, datetime_mock):
        datetime_mock.datetime.now.return_value = self.start_date
        self.administrar_parking.aparcar_coche("123", self.parquimetro)
        datetime_mock.datetime.now.return_value = self.end_date
        with self.assertRaises(ValueError):
            self.administrar_parking.desaparcar_coche("224", self.parquimetro)

    def test_calcular_plazas_libres(self, datetime_mock):
        datetime_mock.datetime.now.return_value = self.start_date
        self.administrar_parking.aparcar_coche("123", self.parquimetro)
        self.administrar_parking.aparcar_coche("222", self.parquimetro)
        self.administrar_parking.aparcar_coche("333", self.parquimetro)

        plazas_libres = self.administrar_parking.num_puestos_libres(self.parquimetro)

        self.assertEqual(plazas_libres, 84)

    def test_coche_ya_aparcado(self, datetime_mock):
        datetime_mock.datetime.now.return_value = self.start_date
        self.administrar_parking.aparcar_coche("123", self.parquimetro)
        with self.assertRaises(ValueError):
            self.administrar_parking.aparcar_coche("123", self.parquimetro)

    def test_validar_importe_total_misma_plaza(self, datetime_mock):
        datetime_mock.datetime.now.return_value = self.start_date
        self.administrar_parking.aparcar_coche("123", self.parquimetro)
        datetime_mock.datetime.now.return_value = self.end_date
        importe_1 = self.administrar_parking.desaparcar_coche("123", self.parquimetro)

        datetime_mock.datetime.now.return_value = datetime(2022, 10, 18, 6, 53, 23, 459111)
        self.administrar_parking.aparcar_coche("222", self.parquimetro)
        datetime_mock.datetime.now.return_value = datetime(2022, 10, 18, 19, 53, 23, 459111)
        importe_2 = self.administrar_parking.desaparcar_coche("222", self.parquimetro)

        self.assertEqual(self.administrar_parking.total_importe(self.parquimetro), importe_1 + importe_2)
