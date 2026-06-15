import pytest
from unittest.mock import patch, MagicMock
from translator.TranslatorService import TranslatorService


class TestTranslatorService:
    """Tests para TranslatorService"""

    def setup_method(self):
        """Se ejecuta antes de cada test"""
        self.translator = TranslatorService()

    # TESTS UNITARIOS - Métodos aislados

    def test_search_languages_con_inicial_valida(self):
        """Test: Buscar idioma con inicial válida"""
        resultado = TranslatorService.search_languages("f")

        # Assertions
        assert len(resultado) > 0, "Debería encontrar idiomas con 'f'"
        assert "french" in resultado.values(), "Debería incluir 'french'"
        assert isinstance(resultado, dict), "Debería retornar dict"

    def test_search_languages_con_inicial_invalida(self):
        """Test: Buscar idioma con inicial inválida"""
        resultado = TranslatorService.search_languages("xyz123")

        assert len(resultado) == 0, "No debería encontrar idiomas"
        assert resultado == {}, "Debería retornar dict vacío"

    def test_search_languages_con_entrada_vacia(self):
        """Test: Buscar con entrada vacía"""
        resultado = TranslatorService.search_languages("")

        assert len(resultado) == 0, "No debería encontrar idiomas"

    def test_split_text_texto_corto(self):
        """Test: Dividir texto corto (no necesita división)"""
        texto = "Hola mundo"
        resultado = self.translator._split_text(texto, max_length=100)

        assert len(resultado) == 1, "Texto corto debería ser UN chunk"
        assert resultado[0] == texto, "El chunk debería ser idéntico"

    def test_split_text_texto_largo(self):
        """Test: Dividir texto largo en chunks"""
        texto = "Oración 1. Oración 2. Oración 3. Oración 4. Oración 5."
        resultado = self.translator._split_text(texto, max_length=30)

        assert len(resultado) > 1, "Texto largo debería dividirse"
        for chunk in resultado:
            assert len(chunk) <= 40, "Cada chunk debería respetar límite aproximado"

    # TESTS DE VALIDACIÓN

    def test_translate_text_con_texto_vacio(self):
        """Test: Traducir texto vacío"""
        resultado = self.translator.translate_text("", "spanish", "english")

        assert resultado["exito"] == False, "Debería fallar"
        assert resultado["error"] is not None, "Debería tener mensaje de error"
        assert "vacío" in resultado["error"].lower(), "Error debe mencionar texto vacío"

    def test_translate_text_idioma_destino_invalido(self):
        """Test: Idioma destino inválido"""
        resultado = self.translator.translate_text("Hola", "spanish", "xyz_invalido")

        assert resultado["exito"] == False, "Debería fallar"
        assert "no soportado" in resultado["error"].lower(), "Error debe mencionar idioma no soportado"

    # TESTS CON MOCK (sin llamar API real)

    @patch('translator.TranslatorService.GoogleTranslator')
    def test_translate_text_exitoso(self, mock_google):
        """Test: Traducción exitosa (mocked)"""
        # Configurar mock
        mock_instance = MagicMock()
        mock_instance.translate.return_value = "Hello world"
        mock_google.return_value = mock_instance

        resultado = self.translator.translate_text("Hola mundo", "spanish", "english")

        assert resultado["exito"] == True, "Debería ser exitoso"
        assert resultado["contenido_traducido"] == "Hello world", "Debería tener texto traducido"
        assert resultado["error"] is None, "No debería haber error"

    @patch('translator.TranslatorService.GoogleTranslator')
    def test_translate_text_error_conexion(self, mock_google):
        """Test: Error de conexión"""
        mock_instance = MagicMock()
        mock_instance.translate.side_effect = ConnectionError("No internet")
        mock_google.return_value = mock_instance

        resultado = self.translator.translate_text("Hola", "spanish", "english")

        assert resultado["exito"] == False, "Debería fallar"
        assert "conexión" in resultado["error"].lower(), "Debería mencionar conexión"

    @patch('translator.TranslatorService.GoogleTranslator')
    def test_translate_text_error_generico(self, mock_google):
        """Test: Error genérico de API"""
        mock_instance = MagicMock()
        mock_instance.translate.side_effect = Exception("API error")
        mock_google.return_value = mock_instance

        resultado = self.translator.translate_text("Hola", "spanish", "english")

        assert resultado["exito"] == False, "Debería fallar"
        assert resultado["error"] is not None, "Debería tener mensaje de error"