import unittest

from ..maksukortti import Maksukortti, MAUKAS, EDULLINEN


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.kortti = Maksukortti(1000)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10.00 euroa")

    def test_syo_edullisesti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_edullisesti()

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 7.50 euroa")

    def test_syo_maukkaasti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_maukkaasti()

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 6.00 euroa")

    def test_syo_edullisesti_ei_vie_saldoa_negatiiviseksi(self):
        kortti = Maksukortti(200)
        kortti.syo_edullisesti()

        self.assertEqual(str(kortti), "Kortilla on rahaa 2.00 euroa")

    # Lataa rahaa -testit

    def test_kortille_voi_ladata_rahaa(self):
        self.kortti.lataa_rahaa(2500)

        self.assertEqual(str(self.kortti), "Kortilla on rahaa 35.00 euroa")

    def test_kortin_saldo_ei_ylita_maksimiarvoa(self):
        self.kortti.lataa_rahaa(20000)
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 150.00 euroa")

    # Tehtävä 3: Lisää testejä

    def test_maukkaan_lounaan_syominen_ei_vie_saldoa_negatiiviseksi(self):
        kortti = Maksukortti(MAUKAS-1)
        kortti.syo_maukkaasti()
        self.assertEqual(kortti.saldo, MAUKAS-1)

    def test_negatiivisen_summan_lataaminen_ei_muuta_kortin_saldoa(self):
        saldo_aluksi = self.kortti.saldo
        self.kortti.lataa_rahaa(-1)
        self.assertEqual(self.kortti.saldo, saldo_aluksi)

    def test_kortilla_pystyy_ostamaan_edullisen_lounaan_kun_kortilla_rahaa_vain_edullisen_lounaan_verran(self):
        kortti = Maksukortti(EDULLINEN)
        kortti.syo_edullisesti()
        self.assertGreaterEqual(kortti.saldo, 0)

    def test_kortilla_pystyy_ostamaan_maukkaan_lounaan_kun_kortilla_rahaa_vain_maukkaan_lounaan_verran(self):
        kortti = Maksukortti(MAUKAS)
        kortti.syo_maukkaasti()
        self.assertGreaterEqual(kortti.saldo, 0)
