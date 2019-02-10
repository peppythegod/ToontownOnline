@echo off
cd ..
:main
set DOWNLOAD_SERVER=http://127.0.0.1:6969/launcher/current/
set WEB_ACCT_PARAMS=None
set /P GAME_USERNAME= Game Username:
set GAME_SERVER=127.0.0.1:7000
set /P LOGIN_TOKEN= Login Token:
set GAME_CHAT_ELIGIBLE=1
set ACCOUNT_SERVER=http://toontown.go.com
Toontown.exe
pause
goto :main