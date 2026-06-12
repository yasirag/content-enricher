from scrap_wiki.Scrap_wiki import WikipediaScraper
from src.enrichers.google_enricher import ContentEnricher
from utils.utils import get_user_input

print("=== Content Enricher ===")


tema = get_user_input("¿Qué tema quieres buscar en Wikipedia? ")

print("\n📥 Buscando en Wikipedia...")
scraper = WikipediaScraper(tema=tema, idioma="es")
resultado_scraper = scraper.buscar()


if not resultado_scraper["exito"]:
    print(f"❌ Error: {resultado_scraper['error']}")
    exit()

print(f"✅ Búsqueda exitosa!")
print(f"📄 Título: {resultado_scraper['titulo']}")
print(f"🔗 URL: {resultado_scraper['url']}")

# PASO 3: Enriquecer contenido con Gemini
print("\n✨ Enriqueciendo contenido con IA...")
enricher = ContentEnricher()
resultado_enriquecimiento = enricher.enrich(
    title=resultado_scraper['titulo'],
    content=resultado_scraper['contenido']
)

if not resultado_enriquecimiento["exito"]:
    print(f"❌ Error al enriquecer: {resultado_enriquecimiento['error']}")
    exit()

print("✅ Contenido enriquecido exitosamente!")

# PASO 4: Mostrar resultados
print("\n" + "="*60)
print("CONTENIDO ORIGINAL (5 párrafos)")
print("="*60)
print(resultado_scraper['contenido'])

print("\n" + "="*60)
print("CONTENIDO ENRIQUECIDO")
print("="*60)
print(resultado_enriquecimiento['contenido_enriquecido'])