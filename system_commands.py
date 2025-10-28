import os
from Nika import speak
import subprocess
#путь к nircmd НЕ МЕНЯТЬ
NIRCMD = "nircmd.exe"

#звук на 20%up
def volume_up(percent=20):
    step = int(65535 * percent / 100)
    subprocess.run([NIRCMD, "changesysvolume", str(step)])
    speak("Громкость увеличена")
#звук на 20%down
def volume_down(percent=20):
    step = int(65535 * percent / 100)
    subprocess.run([NIRCMD, "changesysvolume", f"-{step}"])
    speak("Громкость уменьшена")
#звук mute(выкл.)
def mute():
    speak("Звук отключён")
    subprocess.run([NIRCMD, "mutesysvolume", "1"])
#звук unmute(вкл.)
def unmute():
    subprocess.run([NIRCMD, "mutesysvolume", "0"])
    speak("Звук включён")
#комп lock(блок.)
def lock_pc():
    subprocess.run([NIRCMD, "lockws"])
    speak("Экран заблокирован")
def restart_pc():
    speak("Перезагрузка компьютера")
    subprocess.run([NIRCMD, "exitwin", "reboot"])
def shutdown_pc():
    speak("Выключение компьютера")
    subprocess.run([NIRCMD, "exitwin", "poweroff"])
def sleep_pc():
    speak("Переключение компьютера в сонный режим")
    subprocess.run([NIRCMD, "standby"])
def empty_recycle_bin():
    subprocess.run([NIRCMD, "emptybin", "2"])
    speak("Очистка корзины")