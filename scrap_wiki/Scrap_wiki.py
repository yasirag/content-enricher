from logging import exception
import requests
from bs4 import BeautifulSoup
from typing import Dict
from urllib.parse import quote



class WikipediaScraper:
    def __init__(self, tema, idioma: str = "en"):
        self.tema= tema.strip()
        self.idioma = idioma
        self.base_url = f"https://{idioma}.wikipedia.org/wiki"

    def buscar(self) -> Dict:
        try:
            # NUEVA VALIDACIÓN 1: Tema no vacío
            if not self.tema or self.tema.strip() == "":
                return {
                    "exito": False,
                    "titulo": None,
                    "contenido": None,
                    "url": None,
                    "error": "El tema no puede estar vacío"
                }

            # Código actual
            url = self._construir_url(self.tema)
            html = self._descargar_html(url)

            # NUEVA VALIDACIÓN 2: Status code
            # Necesitamos verificar que la respuesta fue exitosa

            soup = BeautifulSoup(html, "html.parser")
            titulo = self._extraer_titulo(soup)
            contenido = self._extraer_contenido(soup)

            return {
                "exito": True,
                "titulo": titulo,
                "contenido": contenido,
                "url": url,
                "error": None
            }
        except ConnectionError as e:
            # NUEVA VALIDACIÓN 3: Manejar error de conexión específicamente
            return {
                "exito": False,
                "titulo": None,
                "contenido": None,
                "url": None,
                "error": f"Error de conexión: {str(e)}"
            }
        except Exception as e:
            return {
                "exito": False,
                "titulo": None,
                "contenido": None,
                "url": None,
                "error": str(e)
            }
    def _construir_url(self, tema: str) -> str:
        tema_encoded = quote(tema.replace(" ", "_"), safe="")
        url = f"{self.base_url}/{tema_encoded}"
        return url


    def _descargar_html(self, url: str) -> str:
        session = requests.Session()
        response = session.get(url,headers={'user-agent': 'Mozilla/5.0'}, timeout=10)
        if response.status_code == 404:
            raise Exception(f"No se encontró artículo para '{self.tema}' en Wikipedia")
        elif response.status_code != 200:
            raise Exception(f"Error {response.status_code} al descargar: {url}")

        return response.text


    def _extraer_titulo(self, soup: BeautifulSoup) -> str:
        soup= BeautifulSoup(str(soup), "html.parser")
        h1= soup.find("h1", class_="firstHeading")
        if h1:
            return h1.text.strip()
        else:
            raise Exception(f"No se encontró el titulo del articulo: {self.tema}")

    def _extraer_contenido(self, soup: BeautifulSoup) -> str:

        contenido_div = soup.find("div", id="mw-content-text")


        if not contenido_div:
            raise Exception("No se encontró contenido para ese tema")


        parrafos = contenido_div.find_all("p")[:5]

        if not parrafos:
            raise Exception("No se encontraron párrafos en el artículo")


        contenido = "\n\n".join([p.text for p in parrafos])

        return contenido
