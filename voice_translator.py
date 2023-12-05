from datetime import datetime
from playsound import playsound
import os
import logging
from gtts import gTTS
import speech_recognition as sr
from googletrans import Translator
user_credentials = {}
def login():
    print("Welcome to the Voice Translator!")
    print("Do you have an account? (yes/no)")
    choice = input()
    if choice.lower() == 'yes':
        return existing_user_login()
    elif choice.lower() == 'no':
        return new_user_signup()
    else:
        print("Invalid choice. Exiting.")
        return False
def existing_user_login():
    print("Enter your username: ")
    username = input()
    print("Enter your password: ")
    password = input()
    if check_credentials(username, password):
        print("Login successful!")
        return True
    else:
        print("Login failed. Exiting.")
        return False
def check_credentials(username, password):
    if username in user_credentials and user_credentials[username] == password:
        return True
    else:
        return False
def new_user_signup():
    print("Great! Let's create a new account.")
    username = input("Enter your desired username: ")
    password = input("Enter your desired password: ")
    user_credentials[username] = password
    print("Account created successfully! Now, let's log in.")
    return existing_user_login()
def existing_user_login_with_username(username):
    print("Enter your password: ")
    password = input()
    if check_credentials(username, password):
        print("Login successful!")
        return True
    else:
        print("Login failed. Exiting.")
        return False
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Voice listening")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Voice Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"The User said {query}\n")
    except Exception as e:
        print("Please say that again")
        return "None"
    return query
def destination_language():
    print("Please say that language in which you want to convert")
    print()
    to_lang = takecommand()
    while to_lang == "None":
        to_lang = takecommand()
    to_lang = to_lang.lower()
    return to_lang
def select_voice():
    return 'en'
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.origin, translation.text
def main():
    if not login():
        return
    dic = {'afrikaans': 'af', 'albanian': 'sq',
           'amharic': 'am', 'arabic': 'ar',
           'armenian': 'hy', 'azerbaijani': 'az',
           'basque': 'eu', 'belarusian': 'be',
           'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg',
           'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny',
           'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw',
           'corsican': 'co', 'croatian': 'hr', 'czech': 'cs',
           'danish': 'da', 'dutch': 'nl', 'english': 'en',
           'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl',
           'finnish': 'fi', 'french': 'fr', 'frisian': 'fy',
           'galician': 'gl', 'georgian': 'ka', 'german': 'de',
           'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht',
           'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he',
           'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu',
           'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id',
           'irish': 'ga', 'italian': 'it', 'japanese': 'ja',
           'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk',
           'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku',
           'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la',
           'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb',
           'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms',
           'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi',
           'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my',
           'nepali': 'ne', 'norwegian': 'no', 'odia': 'or',
           'pashto': 'ps', 'persian': 'fa', 'polish': 'pl',
           'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro',
           'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd',
           'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn',
           'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk',
           'slovenian': 'sl', 'somali': 'so', 'spanish': 'es',
           'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv',
           'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te',
           'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk',
           'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz',
           'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh',
           'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
    logging.basicConfig(filename='translation_log.txt', level=logging.INFO)
    query = takecommand()
    while query.lower() != "exit":
        while query == "None":
            query = takecommand()
        to_lang = destination_language()
        while to_lang not in dic:
            print("Language in which you are trying to convert is currently not available, please input some other language")
            print()
            to_lang = destination_language()
        to_lang_code = dic[to_lang]
        try:
            original_text, translated_text = translate_text(query, to_lang_code)
            text = f"Original Text: {original_text}\nTranslated Text: {translated_text}"
        except Exception as e:
            print(f"Error during translation: {e}")
            text = "Error during translation. Please try again."
        voice_choice = select_voice()
        speak = gTTS(text=translated_text, lang=voice_choice, slow=False)
        speak.save(f"captured_voice.mp3")
        playsound(f'captured_voice.mp3')
        os.remove('captured_voice.mp3')
        logging.info(f"{datetime.now()} - User query: {query}, Destination language: {to_lang_code}, Translated text: {text}")
        print(text)
        query = takecommand()
    print("Thank you for using the voice translator. Have a great day!")
if __name__ == "__main__":
    main()
