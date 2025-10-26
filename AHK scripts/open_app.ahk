; Скрипт принимает путь к .exe приложения как параметр
appPath := %1%

if FileExist(appPath)
{
    Run, %appPath%
}
else
{
    MsgBox, Не удалось найти приложение: %appPath%
}