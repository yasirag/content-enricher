import pytest
from unittest.mock import patch, MagicMock
from scrap_wiki.Scrap_wiki import WikipediaScraper


class TestWikipediaScraper:


    def setup_method(self):

        self.scraper = WikipediaScraper(tema="Python", idioma="es")


    @patch('scrap_wiki.Scrap_wiki.requests.Session')
    @patch('scrap_wiki.Scrap_wiki.BeautifulSoup')
    def test_buscar_exitoso(self, mock_soup, mock_session_class):


        mock_session_instance = MagicMock()
        mock_session_class.return_value = mock_session_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>Python content</html>"
        mock_session_instance.get.return_value = mock_response


        mock_soup_instance = MagicMock()


        mock_title = MagicMock()
        mock_title.text = "Python (lenguaje de programación)"
        mock_soup_instance.find.return_value = mock_title


        mock_paragraphs = [
            MagicMock(text="Párrafo 1"),
            MagicMock(text="Párrafo 2"),
            MagicMock(text="Párrafo 3"),
            MagicMock(text="Párrafo 4"),
            MagicMock(text="Párrafo 5")
        ]
        mock_soup_instance.find_all.return_value = mock_paragraphs
        mock_soup.return_value = mock_soup_instance


        resultado = self.scraper.buscar()


        assert isinstance(resultado, dict), "Debería retornar dict"
        assert "exito" in resultado, "Debería tener 'exito'"
        assert "titulo" in resultado, "Debería tener 'titulo'"
        assert "contenido" in resultado, "Debería tener 'contenido'"
        assert "url" in resultado, "Debería tener 'url'"
        assert "error" in resultado, "Debería tener 'error'"

        assert resultado["exito"] == True, "exito debería ser True"
        assert resultado["titulo"] is not None, "titulo no debería ser None"
        assert resultado["contenido"] is not None, "contenido no debería ser None"
        assert resultado["url"] is not None, "url no debería ser None"
        assert resultado["error"] is None, "error debería ser None cuando es exitoso"


    def test_buscar_tema_vacio(self):


        scraper = WikipediaScraper(tema="", idioma="es")

        resultado = scraper.buscar()


        assert resultado["exito"] == False, "Debería fallar con tema vacío"
        assert resultado["error"] is not None, "Debería tener mensaje de error"
        assert "vacío" in resultado["error"].lower(), "Error debe mencionar tema vacío"


    @patch('scrap_wiki.Scrap_wiki.requests.Session')
    def test_buscar_error_conexion(self, mock_session_class):


        mock_session_instance = MagicMock()
        mock_session_class.return_value = mock_session_instance
        mock_session_instance.get.side_effect = ConnectionError("No internet")
        resultado = self.scraper.buscar()


        assert resultado["exito"] == False, "Debería fallar con error de conexión"
        assert resultado["error"] is not None, "Debería tener mensaje de error"
        assert "conexión" in resultado["error"].lower(), \
            "Error debería mencionar conexión"

    @patch('scrap_wiki.Scrap_wiki.requests.Session')
    def test_buscar_tema_no_existe(self, mock_session_class):

        mock_session_instance = MagicMock()
        mock_session_class.return_value = mock_session_instance

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "<html></html>"
        mock_session_instance.get.return_value = mock_response


        resultado = self.scraper.buscar()

        assert resultado["exito"] == False, "Debería fallar cuando tema no existe"
        assert resultado["error"] is not None, "Debería tener mensaje de error"
        assert "no se encontró" in resultado["error"].lower() or "404" in resultado["error"].lower(), \
            "Error debería mencionar que no se encontró"


    def test_scraper_inicializa_con_idioma(self):


        scraper = WikipediaScraper(tema="Python", idioma="en")


        assert scraper.idioma == "en", "Debería guardar el idioma"
        assert scraper.tema == "Python", "Debería guardar el tema"
        assert scraper.base_url == "https://en.wikipedia.org/wiki", "URL base debería ser correcta"