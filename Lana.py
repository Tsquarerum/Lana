#import
import json, pyaudio,  subprocess, os
from vosk import Model, KaldiRecognizer
import webbrowser as wb
import torch
import sounddevice as sd
import numpy as np

model_path = "models/v4_ru.pt"


importer = torch.package.PackageImporter(model_path)
tts_model = importer.load_pickle("tts_models", "model")


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tts_model.to(device)


speaker = "baya"

def speak(text: str, speed: float = 1.00):
    audio = tts_model.apply_tts(
        text=text,
        speaker=speaker,
        sample_rate=24000,
        put_accent=True,
        put_yo=True,
    )
    if speed != 1.0:
        audio = np.interp(
            np.arange(0, len(audio), speed),
            np.arange(0, len(audio)),
            audio
        )
    sd.play(audio, 24000)
    sd.wait()
#import .py
from commands import commands
from apps import apps
from website import web


#model and recognizer
assistant_names = ["лана"]
model = Model('small_model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

#commands   
#PC             
def say_hello():#Hello
    speak("Здравствуйте...!")

def say_goodbye():#goodbye
    speak("До свидание!...")
    quit()

def say_goodgirl():#goodgirl 
    speak("Спасибо...!")
    
def say_aboutme():#aboutMile
    speak("Меня зовут Лана, я голосовой помощник, буду рада вам помогать")
    
def say_name():#sayname
    speak("Да сэр!...")
    
def say_thanks():#thanks 
    speak("Всегда пожалуйста...!")

def say_wait():#wait
    speak("Хорошо...буду вас ждать...!")
#site
def youtube():#YouTube
    url = web["translator"][-1]
    speak("открываю Переводчик...")
    wb.open(url)
def youtube():#YouTube
    url = web["youtube"][-1]
    speak("открываю Ютуб...")
    wb.open(url)
def github():#github
    url = web["github"][-1]
    speak("открываю Гитхаб...")
    wb.open(url)
def creator():#creator
    url = web["creator"][-1]
    speak("открываю Гитхаб Разработчика...")
    wb.open(url)
#apps
def open_app(text):
    for app, keywords in apps.items():
        for keyword in keywords[:-1]:
            if keyword.lower() in text.lower():
                exe_path = keywords[-1]
                try:
                    subprocess.Popen(exe_path)
                    speak(f"Открываю {app}...")
                except Exception as e:
                    print(f"Не удалось открыть {app}: {e}")
                    speak(text)
                return True
    return False
    
#site
def open_site(text):
    for website, keywords in web.items():
        for keyword in keywords[:-1]:  
            if keyword.lower() in text.lower():
                url = keywords[-1]
                if url.startswith("http"):
                    wb.open(url)
                    speak(f"Открываю {website}...")
                return True  
    return False  

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
    speak("Здравствуйте!... Чем могу помочь?")
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
        elif command == "say_thanks":
            say_thanks()
            command_executed = True
        elif command == "say_wait":
            say_wait()
            command_executed = True
        if not command_executed:
            found = open_app_or_site(text)
            if not found:
                speak("Команда не найдена...!")
        
        
        
        
        
        
    else:
        pass
        
        
        
        
        
