import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote
from kirjanpito import Kirjanpito

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.kirjanpito = Kirjanpito()

        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            elif tuote_id == 2:
                return 10
            elif tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            elif tuote_id == 2:
                return Tuote(2, "mehu", 7)
            elif tuote_id == 3:
                return Tuote(3, "limu", 3)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote
        
        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_ostoksen_paatyttya_metodia_kutsutaan_oikeilla_arvoilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", self.kauppa._kaupan_tili, ANY)

    def test_kaksi_eri_tuotetta_oikeilla_arvoilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        summa = self.varasto_mock.hae_tuote(1).hinta + self.varasto_mock.hae_tuote(2).hinta
        self.kauppa.tilimaksu("pekka", "12345")
        
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", self.kauppa._kaupan_tili, summa)

    def test_kaksi_samaa_tuotetta_oikeilla_arvoilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        summa = self.varasto_mock.hae_tuote(1).hinta + self.varasto_mock.hae_tuote(1).hinta
        self.kauppa.tilimaksu("pekka", "12345")
        
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", self.kauppa._kaupan_tili, summa)

    def test_kaksi_eri_tuotetta_joista_toinen_loppu(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        summa = self.varasto_mock.hae_tuote(1).hinta
        self.kauppa.tilimaksu("pekka", "12345")
        
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", self.kauppa._kaupan_tili, summa)

    def test_asioinnin_aloitus_nollaa_edelliset_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.aloita_asiointi()
        
        self.assertEqual(self.kauppa._ostoskori.hinta(), 0)

    def test_kauppa_pyytaa_uuden_viitenumeron(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        viite1 = self.kirjanpito.tapahtumat[0]
        viite2 = self.kirjanpito.tapahtumat[1]
        
        self.assertNotEqual(viite1, viite2)
