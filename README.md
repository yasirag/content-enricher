# 📚 Content Enricher

**Herramienta Python para buscar, enriquecer y traducir contenido de Wikipedia con IA**

---

## 📖 Descripción

Content Enricher es una aplicación Python que automatiza el proceso de extracción, enriquecimiento y traducción de contenido desde Wikipedia. 

**Funcionalidad principal:**
1. **Búsqueda en Wikipedia** → Extrae título + 5 párrafos
2. **Enriquecimiento con IA** → Amplía contenido con Google Gemini
3. **Traducción multi-idioma** → Traduce a 100+ idiomas

---

## ✨ Características

### ✅ Implementado
- ✅ Web scraping de Wikipedia (BeautifulSoup + Requests)
- ✅ Enriquecimiento de contenido con Google Gemini API
- ✅ Traducción a 100+ idiomas (GoogleTranslator)
- ✅ Arquitectura OOP con principios SOLID
- ✅ 29 tests unitarios e integración (95% cobertura)
- ✅ Manejo robusto de errores
- ✅ Logging en operaciones críticas
- ✅ Validación de entrada del usuario


---

## 🛠️ Requisitos Técnicos

### Software
- **Python:** 3.14
- **Sistema operativo:** Windows, macOS, Linux
- **Conexión a internet:** Requerida (APIs externas)

### Dependencias principales
```
beautifulsoup4==4.15.0      # Web scraping
requests==2.34.2            # HTTP requests
google-generativeai         # Gemini API
deep-translator==1.11.4     # Traducción multiidioma
python-dotenv               # Variables de entorno
pytest                      # Testing
pytest-cov                  # Cobertura de tests
```

### APIs requeridas
- **Google Generative AI** (Gemini) - Requiere API Key
  - Obtén tu clave: https://makersuite.google.com/app/apikey

---

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/yasirag/content-enricher.git
cd content-enricher
```

### 2. Crear entorno virtual (recomendado)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Crear archivo .env en la raíz del proyecto
# Windows
echo GOOGLE_API_KEY=tu_clave_aqui > .env

# macOS / Linux
echo "GOOGLE_API_KEY=tu_clave_aqui" > .env
```

**O edita `.env` manualmente:**
```
GOOGLE_API_KEY=sk-...tu_clave_api...
```

### 5. Verificar instalación
```bash
python main.py
```

Deberías ver:
```
=== Content Enricher ===
¿Qué tema quieres buscar en Wikipedia?
```

---

## 🚀 Uso

### Ejecución básica
```bash
python main.py
```

### Flujo de interacción
```
1. Ingresa tema a buscar en Wikipedia
   ej: "Artificial Intelligence"

2. El sistema busca y extrae 5 párrafos
   ✅ Búsqueda exitosa!

3. Enriquece el contenido con Gemini
   ✨ Enriqueciendo contenido...

4. Selecciona idioma para traducir
   Ingresa inicial: es (Spanish)

5. El contenido se muestra traducido en terminal
```

---

## 📁 Estructura del Proyecto

```
content-enricher/
├── main.py                          # Punto de entrada
├── .env                             # Variables de entorno (crear)
├── requirements.txt                 # Dependencias
├── README.md                        # Este archivo
│
├── scrap_wiki/
│   ├── __init__.py
│   └── Scrap_wiki.py               # WikipediaScraper
│
├── src/
│   ├── __init__.py
│   └── enrichers/
│       ├── __init__.py
│       └── google_enricher.py      # ContentEnricher (Gemini)
│
├── translator/
│   ├── __init__.py
│   └── TranslatorService.py        # TranslatorService
│
├── utils/
│   ├── __init__.py
│   └── utils.py                    # Funciones auxiliares
│
└── tests/
    ├── __init__.py
    ├── test_scraper.py             # Tests WikipediaScraper
    ├── test_enricher.py            # Tests ContentEnricher
    ├── test_translator.py          # Tests TranslatorService
    ├── test_utils.py               # Tests utilidades
    └── test_integration.py         # Tests integración
```

---

## 🧪 Testing

### Ejecutar todos los tests
```bash
pytest tests/ -v
```

### Ver cobertura
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Ejecutar tests específicos
```bash
# Solo tests del scraper
pytest tests/test_scraper.py -v

# Solo tests de traducción
pytest tests/test_translator.py -v

# Un test específico
pytest tests/test_scraper.py::TestWikipediaScraper::test_search_valid -v
```



## 🎓 Conceptos Aprendidos

Este proyecto demuestra:
- ✅ Web scraping con BeautifulSoup
- ✅ Integración de APIs externas (Google Generative AI)
- ✅ Traducción multiidioma
- ✅ Arquitectura OOP con SRP
- ✅ Testing unitario e integración
- ✅ Manejo de errores robusto
- ✅ Control de versiones con Git
- ✅ Buenas prácticas de código Python

---

## 📚 Referencias

### Documentación oficial
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](https://docs.python-requests.org/en/master/)
- [Google Generative AI](https://ai.google.dev/)
- [Deep Translator](https://deeptranslate.readthedocs.io/en/latest/)
- [pytest](https://docs.pytest.org/)

### APIs
- [Wikipedia](https://en.wikipedia.org)
- [Google Generative AI](https://makersuite.google.com/)

---

## 📝 Licencia

Este proyecto es de código abierto y disponible bajo licencia MIT.

---

## 👥 Autora: Yasira González

Desarrollado como proyecto educativo en Factoría F5.

---


**Última actualización:** Junio 2025  
**Versión:** 1.0  

