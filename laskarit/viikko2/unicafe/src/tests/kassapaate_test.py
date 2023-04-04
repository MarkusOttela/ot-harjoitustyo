import unittest

from kassapaate  import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):

    KASSA_LAHTOSUMMA = 100000

    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_olion_alustus(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA)
        self.assertEqual(self.kassapaate.maukkaat,  0)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_edullinen_kateisella(self):
        # Rahat eivät riitä
        vaihto = self.kassapaate.syo_edullisesti_kateisella(140)
        self.assertEqual(vaihto, 140)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,  self.KASSA_LAHTOSUMMA)

        # Syntyy vaihtorahaa
        vaihto = self.kassapaate.syo_edullisesti_kateisella(340)
        self.assertEqual(vaihto, 100)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat,  0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA+240)

    def test_maukas_kateisella(self):
        # Rahat eivät riitä
        vaihto = self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(vaihto, 300)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,  self.KASSA_LAHTOSUMMA)

        # Syntyy vaihtorahaa
        vaihto = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(vaihto, 100)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA+400)

    def test_edullinen_kortilla_kun_rahat_eivat_riita(self):
        maksukortti = Maksukortti(saldo=100)

        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(maksukortti))

        self.assertEqual(maksukortti.saldo, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  0)

    def test_edullinen_kortilla_kun_rahat_riitavat(self):
        maksukortti = Maksukortti(saldo=500)

        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(maksukortti))

        self.assertEqual(maksukortti.saldo, 500-240)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat,  0)

    def test_maukas_kortilla_kun_rahat_eivat_riita(self):
        maksukortti = Maksukortti(saldo=100)

        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(maksukortti))

        self.assertEqual(maksukortti.saldo, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  0)

    def test_maukas_kortilla_kun_rahat_riitavat(self):
        maksukortti = Maksukortti(saldo=500)

        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(maksukortti))

        self.assertEqual(maksukortti.saldo, 500-400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  1)

    def test_negatiivisen_rahan_lataaminen_kortille(self):
        maksukortti = Maksukortti(saldo=500)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, -100)
        self.assertEqual(maksukortti.saldo, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA)

    def test_rahan_lataaminen_kortille(self):
        maksukortti = Maksukortti(saldo=500)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 100)
        self.assertEqual(maksukortti.saldo, 600)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.KASSA_LAHTOSUMMA + 100)


if __name__ == '__main__':
    unittest.main()
