import unittest

from kassapaate import Kassapaate

class TestKassapaate(unittest.TestCase):

    kassa_lahtosumma = 1000_00

    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_olion_alustus(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassa_lahtosumma)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_edullinen_kateisella(self):
        # Rahat eivät riitä
        vaihto = self.kassapaate.syo_edullisesti_kateisella(140)
        self.assertEqual(vaihto, 140)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  0)

        # Syntyy vaihtorahaa
        vaihto = self.kassapaate.syo_edullisesti_kateisella(340)
        self.assertEqual(vaihto, 100)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat,  0)

    def test_maukas_kateisella(self):
        # Rahat eivät riitä
        vaihto = self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(vaihto, 300)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  0)

        # Syntyy vaihtorahaa
        vaihto = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(vaihto, 100)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat,  1)


if __name__ == '__main__':
    unittest.main()
