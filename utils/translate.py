from time import sleep
from googletrans import Translator
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')


def translate(text):
    if text:
        translator = Translator()
        if len(text) <= 5000:
            translation = translator.translate(text=text, dest="ru").text
            sleep(10)
            return translation
        else:
            text = sent_tokenize(text=text, language="italian")
            fivek = ""
            translation = ""
            for sentence in text:
                if len(fivek + sentence) < 5000:
                    fivek += sentence
                else:
                    translation += translator.translate(text=fivek, dest="ru").text
                    fivek = sentence
                    print("Пауза в переводе...")
                    sleep(10)
            if fivek:
                translation += translator.translate(text=fivek, dest="ru").text
            return translation
    return None
