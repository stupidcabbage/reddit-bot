from googletrans import Translator

translator = Translator()

def translate_text(text: str, dest: str="ru") -> str:
    """Переводит предоставленный текст с любого языка на любой язык.
    Без передачи параметра dest - на русский."""
    return translator.translate(text, dest).text
