import pytest
from unittest.mock import patch, MagicMock
from scrap_wiki.Scrap_wiki import WikipediaScraper
from src.enrichers.google_enricher import ContentEnricher
from translator.TranslatorService import TranslatorService


class TestIntegration:
    """Tests de integración: flujo completo"""

    # ============ TEST 1: FLUJO COMPLETO SCRAPER → ENRICHER ============
    @patch('scrap_wiki.Scrap_wiki.requests.Session')
    @patch('scrap_wiki.Scrap_wiki.BeautifulSoup')
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'})
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    def test_scraper_enricher_integration(self, mock_model_class, mock_configure,
                                          mock_soup, mock_session_class):
        """Test: Flujo Scraper → Enricher"""
        # 1️⃣ ARRANGE Scraper
        mock_session_instance = MagicMock()
        mock_session_class.return_value = mock_session_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>content</html>"
        mock_session_instance.get.return_value = mock_response

        mock_soup_instance = MagicMock()
        mock_title = MagicMock()
        mock_title.text = "Python"
        mock_soup_instance.find.return_value = mock_title

        mock_paragraphs = [MagicMock(text=f"Párrafo {i}") for i in range(5)]
        mock_soup_instance.find_all.return_value = mock_paragraphs
        mock_soup.return_value = mock_soup_instance

        # ARRANGE Enricher
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance

        mock_gemini_response = MagicMock()
        mock_gemini_response.text = "Contenido enriquecido"
        mock_model_instance.generate_content.return_value = mock_gemini_response

        # 2️⃣ ACT
        scraper = WikipediaScraper(tema="Python", idioma="es")
        resultado_scraper = scraper.buscar()

        enricher = ContentEnricher()
        resultado_enricher = enricher.enrich(resultado_scraper["titulo"],
                                             resultado_scraper["contenido"])

        # 3️⃣ ASSERT
        assert resultado_scraper["exito"] == True, "Scraper debería exitoso"
        assert resultado_enricher["exito"] == True, "Enricher debería ser exitoso"
        assert resultado_enricher["contenido_enriquecido"] is not None

    # ============ TEST 2: FLUJO COMPLETO CON TRADUCCIÓN ============
    @patch('scrap_wiki.Scrap_wiki.requests.Session')
    @patch('scrap_wiki.Scrap_wiki.BeautifulSoup')
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'})
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    @patch('translator.TranslatorService.GoogleTranslator')
    def test_flujo_completo_scraper_enricher_translator(self, mock_translator, mock_model_class,
                                                        mock_configure, mock_soup, mock_session_class):
        """Test: Flujo completo Scraper → Enricher → Translator"""
        # ARRANGE Scraper
        mock_session_instance = MagicMock()
        mock_session_class.return_value = mock_session_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>content</html>"
        mock_session_instance.get.return_value = mock_response

        mock_soup_instance = MagicMock()
        mock_title = MagicMock()
        mock_title.text = "Python"
        mock_soup_instance.find.return_value = mock_title

        mock_paragraphs = [MagicMock(text=f"Párrafo {i}") for i in range(5)]
        mock_soup_instance.find_all.return_value = mock_paragraphs
        mock_soup.return_value = mock_soup_instance

        # ARRANGE Enricher
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance

        mock_gemini_response = MagicMock()
        mock_gemini_response.text = "Contenido enriquecido en español"
        mock_model_instance.generate_content.return_value = mock_gemini_response

        # ARRANGE Translator
        mock_translator_instance = MagicMock()
        mock_translator.return_value = mock_translator_instance
        mock_translator_instance.translate.return_value = "Enriched content in English"

        # ACT
        scraper = WikipediaScraper(tema="Python", idioma="es")
        resultado_scraper = scraper.buscar()

        enricher = ContentEnricher()
        resultado_enricher = enricher.enrich(resultado_scraper["titulo"],
                                             resultado_scraper["contenido"])

        translator = TranslatorService()
        resultado_traduccion = translator.translate_text(
            resultado_enricher["contenido_enriquecido"],
            "auto",
            "english"
        )

        # ASSERT
        assert resultado_scraper["exito"] == True
        assert resultado_enricher["exito"] == True
        assert resultado_traduccion["exito"] == True
        assert resultado_traduccion["contenido_traducido"] is not None
        