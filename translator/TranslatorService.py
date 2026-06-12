from deep_translator import GoogleTranslator




#print(translate_text("mira que bonito todo", "es","en"))

class TranslatorService:
    def __init__(self):
        pass
    def translate_text(self, text:str, source_lang: str, target_lang:str):
        try:
            translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
            return translated_text
        except Exception as e:
            print("Unexpected error:", e)
