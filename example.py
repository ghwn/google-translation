import json

from google_translator import GoogleTranslator


def main():
    with open("test_sentences.json", 'r') as f:
        sentences = json.load(f)

    translator = GoogleTranslator()
    for sentence in sentences:
        translation = translator.translate(sentence, src="en", dest="ko")
        print(sentence)
        print(translation, '\n')


if __name__ == "__main__":
    main()
