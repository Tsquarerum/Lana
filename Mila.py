#import
import json, pyaudio,  subprocess, os
from vosk import Model, KaldiRecognizer
import webbrowser as wb
#import .py
from commands import commands
from apps import apps
from website import web

#model and recognizer
assistant_names = ["мила"]
model = Model('small_model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

#commands   
#PC             
def say_hello():#Hello
    print("Привет! Чем могу помочь?")

def say_goodbye():#goodbye
    print("Пока!")
    quit()

def say_goodgirl():#goodgirl
    print("Спасибо :3")

def say_aboutme():#aboutMile
    print("Меня зовут Мила,я голосовой помощник,буду рада вам помогать,если вы хотите посмотреть на все команды то советую посмотреть файлы как:commands.py, apps.py, website.py #могут в будущем измениться")

def say_name():#sayname
    print("Да сэр!")

def say_thanks():#thanks
    print("Всегда пожалуйста!")
#site
def youtube():#YouTube
    url = web["youtube"][-1]
    print("открываю YouTube...")
    wb.open(url)
def github():#github
    url = web["github"][-1]
    print("открываю GitHub...")
    wb.open(url)
def creator():#creator
    url = web["creator"][-1]
    print("открываю GitHub Разработчика...")
    wb.open(url)
#apps
def open_app(text):
    for app, keywords in apps.items():
        for keyword in keywords[:-1]:
            if keyword.lower() in text.lower():
                exe_path = keywords[-1]
                try:
                    subprocess.Popen(exe_path)
                    print(f"Открываю {app}...")
                except Exception as e:
                    print(f"Не удалось открыть {app}: {e}")
                return True
    return False
    
#site
def open_site(text):
    for website, keywords in web.items():
        for keyword in keywords[:-1]:  # кроме последнего элемента (URL)
            if keyword.lower() in text.lower():
                url = keywords[-1]
                if url.startswith("http"):
                    wb.open(url)
                    print(f"Открываю {website}...")
                return True  # сайт найден
    return False  # сайт не найден

#website and apps together   
def open_app_or_site(text):
    if open_app(text):
        return True
    if open_site(text):
        return True
    return False    


#listen
def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer ['text']

#commands
def recognize_command(text):
    text = text.lower()
    for cmd, keywords in commands.items():
        for word in keywords:
            if word.lower() == text:
                return cmd
    return None



#start
if __name__ == "__main__":
    print("Голосовой помощник запущен. Говори что-нибудь...")
    for text in listen():
        print(f"Вы сказали: {text}")
            
        command = recognize_command(text)
        command_executed = False
       #PC
        if command == "say_hello":
            say_hello()
            command_executed = True
        elif command == "say_goodbye":
            say_goodbye()
            command_executed = True
        elif command == "say_goodgirl":
            say_goodgirl()
            command_executed = True
        elif command == "say_aboutme":
            say_aboutme()
            command_executed = True
        elif command == "say_name":
            say_name()
            command_executed = True
        if not command_executed:
            found = open_app_or_site(text)
            if not found:
                print(f"Команда или приложение для слова '{text}' не найдено.")
   
        
        
        
        
        
        
    else:
        pass
        
        
        
        
        
