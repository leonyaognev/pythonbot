from googletrans import Translator


def transruen(text):
    translator = Translator()
    translation = translator.translate(text, src='ru', dest='en')
    return translation.text


def transenru(text):
    translator = Translator()
    result = translator.translate(text, src='en', dest='ru')
    return result.text
