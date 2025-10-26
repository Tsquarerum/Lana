#import
import json, pyaudio,  subprocess, os
from vosk import Model, KaldiRecognizer
from commands import commands
import apps
import webbrowser as wb


#model and recognizer
assistant_names = ["мили"]
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
    print("Меня зовут Мили,я голосовой помощник,буду рада вам помогать,если вы хотите посмотреть на все команды то советую посмотреть файлы как:commands.py и apps.py #могут в будущем измениться")

def say_name():#sayname
    print("Да сэр")
#site and apps
def youtube():#YouTube
    url = apps["youtube"][-1]
    print("открываю YouTube...")
    wb.open(url)

    
 
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
    for cmd, keywords in commands.items():
        for word in keywords:
            if word in text:
                return cmd
    return None
#apps
def open_app_by_name(text):
    for app, keywords in apps.apps.items():
        for keyword in keywords[:-1]:  # кроме последнего элемента (URL)
            if keyword.lower() in text.lower():
                url = keywords[-1]
                if url.startswith("http"):
                    wb.open(url)
                    print(f"Открываю {app}...")
                return
    print(f"Приложение или сайт для слова '{text}' не найдено.")

#start
if __name__ == "__main__":
    print("Голосовой помощник запущен. Говори что-нибудь...")
    for text in listen():
        print(f"Вы сказали: {text}")
            
        command = recognize_command(text)
       #PC
        if command == "say_hello":
            say_hello()
        elif command == "say_goodbye":
            say_goodbye()
        elif command == "say_goodgirl":
            say_goodgirl()
        elif command == "say_aboutme":
            say_aboutme()
        else:#not recognized
            print("Команда не распознана.")
       #site and apps
        open_app_by_name(text)
   
        
        
        
        
        
        
    else:
        pass
        
        
        
        
        
