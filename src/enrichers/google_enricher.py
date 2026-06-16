import os
from typing import Dict
from dotenv import load_dotenv
import google.generativeai as genai

class ContentEnricher:


    def __init__(self, api_key: str = None):

        load_dotenv()
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY no encontrada en .env")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def enrich(self, title: str, content: str) -> Dict:

        try:
            prompt = self._build_prompt(title, content)
            enriched_content = self._call_gemini(prompt)

            return {
                "exito": True,
                "contenido_enriquecido": enriched_content,
                "error": None
            }
        except Exception as e:
            return {
                "exito": False,
                "contenido_enriquecido": None,
                "error": str(e)
            }

    def _build_prompt(self, title: str, content: str) -> str:

        prompt = f"""Eres un experto educativo especializado en claridad y profundidad.

Tu tarea es ENRIQUECER un artículo de Wikipedia sobre el siguiente tema:

TÍTULO: {title}

CONTENIDO ORIGINAL:
{content}

INSTRUCCIONES:
1. Amplía CADA PÁRRAFO con explicaciones más detalladas
2. Utiliza ejemplos concretos cuando sea relevante
3. Mejora la estructura del texto para máxima claridad
4. Explica conceptos complejos en lenguaje simple
5. Mantén el mismo número de párrafos (5) pero mucho más rico
6. No cambies el tema ni agregues información ficticia
7. Usa un tono educativo y profesional

RETORNA SOLO el contenido enriquecido, sin explicaciones adicionales."""

        return prompt

    def _call_gemini(self, prompt: str) -> str:

        response = self.model.generate_content(prompt)
        return response.text