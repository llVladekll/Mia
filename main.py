import speech_recognition as sr
import pyttsx3, json, colorama, random
from colorama import Fore, Style

rpt = {}                                                     #
colorama.init()                                              # Датасет не забудь!!!!!!
engine = pyttsx3.init()                                      # Прости за кучу хуйни от колорамы которая ебет глаза в коде
with open('dataset.json', 'r', encoding='utf-8') as f:       #
    dataset = json.loads(f.read())                           #

def say(text, audio=True):
    print(f'{Fore.RED}[{Style.RESET_ALL}Mia{Fore.RED}]{Style.RESET_ALL}: {text}')
    if audio is True:
        engine.say(text)
        engine.runAndWait()
    else: pass

def listen():
    voice_recognizer = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        audio = voice_recognizer.listen(source, phrase_time_limit=3)
    try:
        voice_text = voice_recognizer.recognize_google(audio, language="ru")
        print(
            f"{Fore.GREEN}[{Style.RESET_ALL}You{Fore.GREEN}]{Style.RESET_ALL}: {Style.BRIGHT}{voice_text}{Style.RESET_ALL}")
        if voice_text != "":
            return voice_text.lower()
        else:
            return listen()
    except sr.UnknownValueError:
        return listen()
    except sr.RequestError:
        print(
            f"{Fore.LIGHTBLACK_EX}[{Style.RESET_ALL}{Fore.RED}Error{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL}: Ошибка соединения")
        return listen()

def recognize(text):
    global dataset, rpt
    for i in dataset:
        if any(word in text for word in dataset[i]["question"]):
            mood = dataset[i]["mood"]
            if rpt.get(mood) == None or rpt.get(mood) == False:
                rpt.update({mood: True})
                say(random.choice(dataset[i]["answer"]))
            elif rpt.get(mood) == True:
                if random.choice([True, False]) == 'True':
                    say(random.choice(dataset[i]["answer"]))
                else:
                    say(random.choice(['Кажется ты это уже говорил, зачем повторяться?',
                                       'Что-то такое я уже слышала', "Ты вроде это говорил",
                                       "Ты уже говорил", "Тебе не кажется что ты повторяешься?",
                                       "Мы же об этом уже говорили"]))


def start():
    while True:
        recognize(listen())

try:
    print(f'{Fore.LIGHTBLACK_EX}[{Style.RESET_ALL}{Fore.RED}Log{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL}: Mia was started')
    start()
except KeyboardInterrupt:
    say('Пока')