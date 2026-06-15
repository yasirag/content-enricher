from scrap_wiki.Scrap_wiki import WikipediaScraper
from src.enrichers.google_enricher import ContentEnricher
from translator.TranslatorService import TranslatorService
from utils.utils import get_user_input

print("=== Content Enricher ===")

# PASO 1: Buscar en Wikipedia
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

# PASO 2: Enriquecer contenido con IA
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

# PASO 3: Mostrar contenido original y enriquecido
print("\n" + "=" * 60)
print("CONTENIDO ORIGINAL (5 párrafos)")
print("=" * 60)
print(resultado_scraper['contenido'])

print("\n" + "=" * 60)
print("CONTENIDO ENRIQUECIDO")
print("=" * 60)
print(resultado_enriquecimiento['contenido_enriquecido'])

# PASO 4: Seleccionar idioma de traducción
print("\n🌍 Selecciona idioma para traducir")
print("─" * 60)

while True:
    query_destino = get_user_input(
        "Ingresa inicial del idioma que quieres para la traducción  y presiona ENTER\n (ej: 'en' para english, 'f' para french): ").lower()

    idiomas_destino = TranslatorService.search_languages(query_destino)

    if not idiomas_destino:
        print(f"❌ No se encontraron idiomas con '{query_destino}'. Intenta de nuevo.")
        continue

    print(f"\n✓ Se encontraron {len(idiomas_destino)} idioma(s):")
    for num, idioma in idiomas_destino.items():
        print(f"  {num:2d}. {idioma}")

    if len(idiomas_destino) > 1:
        seleccion = get_user_input("Selecciona el número\n Y pulsa ENTER: ")
        try:
            num = int(seleccion)
            if num in idiomas_destino:
                idioma_destino = idiomas_destino[num]
                break
            else:
                print("❌ Número no válido. Intenta de nuevo.")
                continue
        except ValueError:
            print("❌ Debes ingresar un número. Intenta de nuevo.")
            continue
    else:
        idioma_destino = list(idiomas_destino.values())[0]
        print(f"✅ Idioma seleccionado: {idioma_destino}")
        break

# PASO 5: Traducir contenido
print(f"\n🌐 Traduciendo a {idioma_destino}...")
translator = TranslatorService()
resultado_traduccion = translator.translate_text(
    resultado_enriquecimiento['contenido_enriquecido'],
    "auto",  # ← DETECCIÓN AUTOMÁTICA (no pregunta al usuario)
    idioma_destino
)

if not resultado_traduccion["exito"]:
    print(f"❌ Error al traducir: {resultado_traduccion['error']}")
    exit()

print("✅ Contenido traducido exitosamente!")

# PASO 6: Mostrar resultado final
print("\n" + "=" * 60)
print(f"CONTENIDO TRADUCIDO A {idioma_destino.upper()}")
print("=" * 60)
print(resultado_traduccion['contenido_traducido'])

print("\n" + "=" * 60)
print("✅ Proceso completado exitosamente!")
print("=" * 60)