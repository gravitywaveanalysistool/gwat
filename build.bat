@echo off

call :findpy
call :findpip

echo installing python requirements...
%PIP% install -r requirements.txt --upgrade
echo building gwat...
%PYTHON% -m PyInstaller -D -w src/__init__.py -n gwat -p src/ --copy-metadata numpy --hidden-import='PIL._tkinter_finder' -i data/media/logo_notext_icon.ico --add-data pro/:pro/ --add-data data/:data/ --clean -y
echo cleaning up...
del build /s /f /Q >nul
for /f %%f in ('dir /ad /b build\') do rd /s /q build\%%f >nul
rd build
del gwat.spec
echo gwat built to dist/gwat


:findpy
python3 --version >nul 2>nul && (
    @REM if python3 was found
    set PYTHON=python3
    exit /b 0
)
python --version >nul 2>nul && (
    @REM if python was found
    set PYTHON=python
    exit /b 0
)
echo python was not found
exit /b 1

:findpip
%PYTHON% -m pip >nul 2>nul && (
    @REM if python -m pip works
    set PIP=%PYTHON% -m pip
    exit /b 0
)
echo pip was not found
exit /b 1
