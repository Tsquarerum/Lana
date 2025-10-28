#import
import json, pyaudio,  subprocess, os
from vosk import Model, KaldiRecognizer
import webbrowser as wb
import torch
import sounddevice as sd
import numpy as np
import time

#import .py
from commands import commands
from apps import apps
from website import web


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



#model and recognizer
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
    speak("Меня зовут Ника, я голосовой помощник, буду рада вам помогать")
    
    
def say_thanks():#thanks 
    speak("Всегда пожалуйста...")

def say_wait():#wait
    speak("Хорошо...буду вас ждать...!")
#site
def translator():#Translator
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
def reddit():#reddit
    url = web["reddit"][-1]
    speak("открываю Реддит...")
    wb.open(url)
def gmail():#gmail не работает
    url = web["gmail"][-1]
    speak("открываю почту...")
    wb.open(url)
def telegram():#telegram
    url = web["telegram"][-1]
    speak("открываю Телеграмм...")
    wb.open(url)
def roblox():#roblox
    url = web["roblox"][-1]
    speak("открываю Роблокс...")
    wb.open(url)
#apps
def open_app(text):
    text_lower = text.lower()
    opened_any = False
    
    for app, keywords in apps.items():
        exe_path = keywords[-1]
        for keyword in keywords[:-1]:
            if all(word in text_lower for word in keyword.lower().split()):
                try:
                    subprocess.Popen(exe_path)
                    speak(f"Открываю {app}...")
                    opened_any = True
                    break
                except Exception as e:
                    print(f"Не удалось открыть {app}: {e}")
                    speak(f"Не получилось открыть {app}")
                    opened_any = True
                    break
    return opened_any
#site
def open_site(text):
    text_lower = text.lower()
    opened_any = False
    
    for website, keywords in web.items():
        url = keywords[-1]
        for keyword in keywords[:-1]:
            if all(word in text_lower for word in keyword.lower().split()):
                if url.startswith("http"):
                    wb.open(url)
                    speak(f"Открываю {website}...")
                    opened_any = True
                    break
    return opened_any

#website and apps together   
def open_app_or_site(text):
    text_lower = text.lower()
    opened_items = []

    #apps
    for app, keywords in apps.items():
        exe_path = keywords[-1]
        for keyword in keywords[:-1]:
            if all(word in text_lower for word in keyword.lower().split()):
                try:
                    subprocess.Popen(exe_path)
                    opened_items.append(app)
                    break
                except Exception as e:
                    print(f"Не удалось открыть {app}: {e}")
                    opened_items.append(app)
                    break
#site
    for website, keywords in web.items():
        url = keywords[-1]
        for keyword in keywords[:-1]:
            if all(word in text_lower for word in keyword.lower().split()):
                if url.startswith("http"):
                    opened_items.append(website)
                    break

    #Говорим один раз
    if opened_items:
        speak("Открываю"+ ",".join(opened_items))

        for app in opened_items:
            if app in apps:
                exe_path = apps[app][-1]
                try:
                    subprocess.Popen(exe_path)
                except:
                    pass
            elif app in web:
                url = web[app][-1]
                try:
                    wb.open(url)
                except:
                    pass
        return True

    return False

#commands
def recognize_command(text):
    text = text.lower()
    for cmd, keywords in commands.items():
        for word in keywords:
            if word.lower() == text:
                return cmd
    return None


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").lower().strip()
            if text:
                yield text
        else:
            yield ""
#start
if __name__ == "__main__":
    speak("Здравствуйте!... Скажите 'Ника', чтобы начать.")
    
    WAKE_WORD = "ника"
    WAKE_TIMEOUT = 20  
    listening = False
    last_active = 0
    timeout_announced = False  

    for text in listen():
        if not listening:
            if text and WAKE_WORD in text:
                listening = True
                last_active = time.time()
                timeout_announced = False
                speak("Да, сэр.")
            continue

        
        if listening:
            if text:
                print(f"Вы сказали: {text}")
                last_active = time.time()
                timeout_announced = False
            elif time.time() - last_active > WAKE_TIMEOUT and not timeout_announced:
                listening = False
                timeout_announced = True
                speak("Время ожидания истекло. Скажите 'Ника', чтобы начать снова.")
                continue
            else:
                continue

        text = text.replace(WAKE_WORD, "").strip()
        command_executed = False
        command = recognize_command(text)
        
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
      
        
  