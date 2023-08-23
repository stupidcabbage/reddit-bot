import async_google_trans_new


async def translate_text(text: str="Text is`t defined", dest: str="ru") -> str:
    """Переводит предоставленный текст с любого языка на любой язык.
    Без передачи параметра dest - на русский."""
    translator = async_google_trans_new.AsyncTranslator()

    return await translator.translate(text, dest)
