import unittest

from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):

    ALKUSUMMA = 1000

    def setUp(self):
        self.maksukortti = Maksukortti(self.ALKUSUMMA)

    def test_luotu_kortti_on_olemassa(self):
        self.assertIsNotNone(self.maksukortti)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo, self.ALKUSUMMA)

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        lisattava = 1
        self.maksukortti.lataa_rahaa(lisattava)
        self.assertEqual(self.maksukortti.saldo, self.ALKUSUMMA+lisattava)

    def test_saldo_vahenee_oikein_jos_rahaa_on_tarpeeksi(self):
        vahennettava = self.ALKUSUMMA-1
        self.maksukortti.ota_rahaa(vahennettava)
        self.assertEqual(self.maksukortti.saldo, self.ALKUSUMMA-vahennettava)

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(self.ALKUSUMMA+1)
        self.assertEqual(self.maksukortti.saldo, self.ALKUSUMMA)

    def test_metodi_palauttaa_true_jos_rahat_riittivat_ja_muuten_false(self):
        self.assertFalse(self.maksukortti.ota_rahaa(self.ALKUSUMMA+1))
        self.assertTrue(self.maksukortti.ota_rahaa(self.ALKUSUMMA))

    def test_str_tulostus(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")


if __name__ == '__main__':
    unittest.main()
