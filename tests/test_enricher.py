import pytest
from unittest.mock import patch, MagicMock
from src.enrichers.google_enricher import ContentEnricher


class TestContentEnricher:
    """Tests para ContentEnricher"""

    # ============ TEST 1: INICIALIZACIÓN CON API KEY ============
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    def test_init_con_api_key_valida(self, mock_model, mock_configure, monkeypatch):
        """Test: Inicializar ContentEnricher con API key válida"""
        # 1️⃣ ARRANGE
        # El mock de GenerativeModel ya está en place
        mock_model.return_value = MagicMock()

        # 2️⃣ ACT
        enricher = ContentEnricher()

        # 3️⃣ ASSERT
        assert enricher.api_key == 'test_api_key', "Debería guardar la API key"
        assert enricher.model is not None, "Debería tener modelo Gemini"
        mock_configure.assert_called_once_with(api_key='test_api_key')

    # ============ TEST 2: INICIALIZACIÓN SIN API KEY ============
    @patch.dict('os.environ', {}, clear=True)
    @patch('src.enrichers.google_enricher.load_dotenv')
    def test_init_sin_api_key(self, mock_load_dotenv):
        """Test: Fallar si no hay API key"""
        # 1️⃣ ARRANGE
        mock_load_dotenv()

        # 2️⃣ ACT & ASSERT
        with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
            ContentEnricher()

    # ============ TEST 3: ENRIQUECIMIENTO EXITOSO ============
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    def test_enrich_exitoso(self, mock_model_class, mock_configure):
        """Test: Enriquecimiento exitoso"""
        # 1️⃣ ARRANGE
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance

        # Simular respuesta de Gemini
        mock_response = MagicMock()
        mock_response.text = "Contenido enriquecido con más detalles y ejemplos"
        mock_model_instance.generate_content.return_value = mock_response

        enricher = ContentEnricher()
        title = "Python"
        content = "Python es un lenguaje de programación."

        # 2️⃣ ACT
        resultado = enricher.enrich(title, content)

        # 3️⃣ ASSERT
        assert resultado["exito"] == True, "Debería ser exitoso"
        assert resultado["contenido_enriquecido"] is not None, "Debería tener contenido"
        assert resultado["error"] is None, "No debería haber error"
        assert "enriquecido" in resultado["contenido_enriquecido"].lower()

    # ============ TEST 4: VALIDACIÓN TITLE VACÍO ============
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    def test_enrich_title_vacio(self, mock_model_class, mock_configure):
        """Test: Enriquecer con título vacío"""
        # 1️⃣ ARRANGE
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance

        enricher = ContentEnricher()

        # 2️⃣ ACT
        resultado = enricher.enrich("", "contenido")

        # 3️⃣ ASSERT
        # Gemini podría manejar esto, pero verificamos estructura
        assert isinstance(resultado, dict), "Debería retornar dict"
        assert "exito" in resultado, "Debería tener 'exito'"

    # ============ TEST 5: VALIDACIÓN CONTENT VACÍO ============
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    def test_enrich_content_vacio(self, mock_model_class, mock_configure):
        """Test: Enriquecer con contenido vacío"""
        # 1️⃣ ARRANGE
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance

        enricher = ContentEnricher()

        # 2️⃣ ACT
        resultado = enricher.enrich("Titulo", "")

        # 3️⃣ ASSERT
        assert isinstance(resultado, dict), "Debería retornar dict"
        assert "exito" in resultado, "Debería tener 'exito'"

    # ============ TEST 6: ERROR DE API ============
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    def test_enrich_error_api(self, mock_model_class, mock_configure):
        """Test: Error al llamar a Gemini"""
        # 1️⃣ ARRANGE
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance
        mock_model_instance.generate_content.side_effect = Exception("API Error")

        enricher = ContentEnricher()

        # 2️⃣ ACT
        resultado = enricher.enrich("Python", "contenido")

        # 3️⃣ ASSERT
        assert resultado["exito"] == False, "Debería fallar"
        assert resultado["error"] is not None, "Debería tener error"
        assert resultado["contenido_enriquecido"] is None, "No debería tener contenido"

    # ============ TEST 7: ESTRUCTURA CORRECTA DEL RETORNO ============
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    def test_enrich_estructura_retorno(self, mock_model_class, mock_configure):
        """Test: Estructura del dict retornado"""
        # 1️⃣ ARRANGE
        mock_model_instance = MagicMock()
        mock_model_class.return_value = mock_model_instance

        mock_response = MagicMock()
        mock_response.text = "Contenido enriquecido"
        mock_model_instance.generate_content.return_value = mock_response

        enricher = ContentEnricher()

        # 2️⃣ ACT
        resultado = enricher.enrich("Python", "contenido")

        # 3️⃣ ASSERT
        assert isinstance(resultado, dict), "Debe ser dict"
        assert set(resultado.keys()) == {"exito", "contenido_enriquecido", "error"}, \
            "Debe tener exactamente estas 3 claves"

    # ============ TEST 8: API KEY POR PARÁMETRO ============
    @patch('src.enrichers.google_enricher.genai.configure')
    @patch('src.enrichers.google_enricher.genai.GenerativeModel')
    def test_init_con_api_key_parametro(self, mock_model_class, mock_configure):
        """Test: Pasar API key como parámetro"""
        # 1️⃣ ARRANGE
        mock_model_class.return_value = MagicMock()
        api_key = "parametro_api_key"

        # 2️⃣ ACT
        enricher = ContentEnricher(api_key=api_key)

        # 3️⃣ ASSERT
        assert enricher.api_key == api_key, "Debería usar API key del parámetro"
        mock_configure.assert_called_once_with(api_key=api_key)