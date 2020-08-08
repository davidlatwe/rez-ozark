@echo off
set PATH=%USERPROFILE%\rez\core\Scripts\rez;%PATH%
set REZ_CONFIG_FILE=%~dp0rezconfig.py
call python .\rez.py %*
