from scrap_wiki.Scrap_wiki import WikipediaScraper
from utils.utils import get_user_input

print("=== Content Enricher ===")


tema = get_user_input("¿Qué tema quieres buscar en Wikipedia?")


scraper = WikipediaScraper(tema=tema, idioma="es")


resultado = scraper.buscar()


if resultado["exito"]:
    print(f"\n Búsqueda exitosa!")
    print(f"Título: {resultado['titulo']}")
    print(f"\nContenido:\n{resultado['contenido']}")
    print(f"\nURL: {resultado['url']}")
else:
    print(f"\n Error: {resultado['error']}")