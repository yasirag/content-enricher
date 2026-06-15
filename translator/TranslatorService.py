import logging
from deep_translator import GoogleTranslator
from typing import Dict

logger = logging.getLogger(__name__)


class TranslatorService:
    """
    Servicio de traducción usando GoogleTranslator.
    Responsabilidad única: traducir texto entre idiomas.
    """

    # Obtener idiomas soportados dinámicamente
    SUPPORTED_LANGUAGES = GoogleTranslator().get_supported_languages()

    def __init__(self):
        """Inicializa el servicio de traducción."""
        logger.info("TranslatorService inicializado")

    @staticmethod
    def search_languages(query: str) -> Dict[int, str]:
        """
        Busca idiomas por inicial o nombre parcial.

        Args:
            query: Letra inicial o nombre parcial (ej: 'f' → french, frisian, etc.)

        Returns:
            Dict: Idiomas que coinciden {número: idioma}
        """
        query = query.lower().strip()

        if len(query) == 0:
            return {}

        # Obtener todos los idiomas soportados
        all_languages = GoogleTranslator().get_supported_languages()

        # Filtrar por inicial o coincidencia parcial
        matches = {}
        counter = 1

        for lang in all_languages:
            if lang.startswith(query) or query in lang:
                matches[counter] = lang
                counter += 1

        return matches

    def _split_text(self, text: str, max_length: int = 4500) -> list:
        """
        Divide el texto en chunks si es muy largo.
        GoogleTranslator tiene límite de ~5000 caracteres.

        Args:
            text: Texto a dividir
            max_length: Máximo de caracteres por chunk

        Returns:
            list: Lista de fragmentos de texto
        """
        if len(text) <= max_length:
            return [text]

        chunks = []
        sentences = text.split('. ')
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def translate_text(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """
        Traduce texto de un idioma a otro.

        Args:
            text (str): Texto a traducir
            source_lang (str): Idioma origen (ej: 'spanish', 'english', o 'auto' para detección)
            target_lang (str): Idioma destino

        Returns:
            Dict: {
                "exito": bool,
                "contenido_traducido": str o None,
                "error": str o None
            }
        """
        logger.info(f"Iniciando traducción: {source_lang} → {target_lang}")

        # VALIDACIÓN 1: Texto no vacío
        if not text or text.strip() == "":
            logger.warning("Intento de traducción con texto vacío")
            return {
                "exito": False,
                "contenido_traducido": None,
                "error": "El texto no puede estar vacío"
            }

        # VALIDACIÓN 2: Idiomas especificados
        if not source_lang or not target_lang:
            logger.warning("Idiomas no especificados")
            return {
                "exito": False,
                "contenido_traducido": None,
                "error": "Debe especificar idiomas origen y destino"
            }

        # VALIDACIÓN 3: Idioma destino válido (source='auto' es siempre válido)
        if source_lang != 'auto' and source_lang not in self.SUPPORTED_LANGUAGES:
            logger.warning(f"Idioma origen no soportado: {source_lang}")
            return {
                "exito": False,
                "contenido_traducido": None,
                "error": f"Idioma '{source_lang}' no soportado"
            }

        if target_lang not in self.SUPPORTED_LANGUAGES:
            logger.warning(f"Idioma destino no soportado: {target_lang}")
            return {
                "exito": False,
                "contenido_traducido": None,
                "error": f"Idioma '{target_lang}' no soportado"
            }

        # TRADUCCIÓN
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)

            # Si el texto es muy largo, dividir en chunks
            chunks = self._split_text(text)
            translated_chunks = []

            for i, chunk in enumerate(chunks):
                logger.info(f"Traduciendo chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)")
                translated_chunk = translator.translate(chunk)
                translated_chunks.append(translated_chunk)

            translated_text = " ".join(translated_chunks)

            logger.info(f"Traducción exitosa - Original: {len(text)} chars → Traducido: {len(translated_text)} chars")

            return {
                "exito": True,
                "contenido_traducido": translated_text,
                "error": None
            }

        except ConnectionError as e:
            logger.error(f"Error de conexión: {str(e)}")
            return {
                "exito": False,
                "contenido_traducido": None,
                "error": "Error de conexión. Verifica tu conexión a internet"
            }

        except Exception as e:
            logger.error(f"Error inesperado en traducción: {str(e)}")
            return {
                "exito": False,
                "contenido_traducido": None,
                "error": f"Error en traducción: {str(e)}"
            }