import pytest
from unittest.mock import patch
from utils.utils import get_user_input


class TestUtils:
    """Tests para funciones auxiliares"""

    # ============ TEST 1: INPUT NORMAL ============
    @patch('builtins.input', return_value='Python')
    def test_get_user_input_normal(self, mock_input):
        """Test: Obtener input del usuario"""
        # 1️⃣ ARRANGE
        mensaje = "¿Qué tema buscas? "

        # 2️⃣ ACT
        resultado = get_user_input(mensaje)

        # 3️⃣ ASSERT
        assert resultado == 'Python', "Debería retornar el input"
        mock_input.assert_called_once_with(mensaje)

    # ============ TEST 2: INPUT VACÍO ============
    @patch('builtins.input', return_value='')
    def test_get_user_input_vacio(self, mock_input):
        """Test: Input vacío"""
        # 1️⃣ ARRANGE
        mensaje = "Ingresa algo: "

        # 2️⃣ ACT
        resultado = get_user_input(mensaje)

        # 3️⃣ ASSERT
        assert resultado == '', "Debería retornar string vacío"

    # ============ TEST 3: INPUT CON ESPACIOS ============
    @patch('builtins.input', return_value='  texto con espacios  ')
    def test_get_user_input_con_espacios(self, mock_input):
        """Test: Input con espacios (se mantienen)"""
        # 1️⃣ ARRANGE
        mensaje = "Ingresa: "

        # 2️⃣ ACT
        resultado = get_user_input(mensaje)

        # 3️⃣ ASSERT
        assert resultado == '  texto con espacios  ', "Debería mantener espacios"

    # ============ TEST 4: MENSAJE PASADO CORRECTAMENTE ============
    @patch('builtins.input', return_value='test')
    def test_get_user_input_mensaje_correcto(self, mock_input):
        """Test: El mensaje se pasa correctamente a input()"""
        # 1️⃣ ARRANGE
        mensaje = "🌍 ¿Qué idioma? "

        # 2️⃣ ACT
        get_user_input(mensaje)

        # 3️⃣ ASSERT
        mock_input.assert_called_once_with(mensaje)