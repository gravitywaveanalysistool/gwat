@echo off
where python3 >nul
if %ERRORLEVEL%==0 (
    set PYTHON=python3
)
if %ERRORLEVEL% neq 0 (
    where python >nul
    if %ERRORLEVEL%==0 set PYTHON=python
    if %ERRORLEVEL% neq 0 (
        echo python not found
        exit 1
    )
)
%PYTHON% -m pip >nul || (
    echo pip not found
    exit 1
)

echo installing python requirements...
%PYTHON% -m pip install -r requirements.txt --upgrade
echo building gwat...
%PYTHON% -m PyInstaller -D -w src/__init__.py -n gwat -p src/ --copy-metadata numpy -i data/media/logo_notext_icon.ico --add-data pro/:pro/ --add-data data/:data/ --clean -y
echo cleaning up...
del build /s /f /Q >nul
for /f %%f in ('dir /ad /b build\') do rd /s /q build\%%f >nul
rd build
del gwat.spec
echo gwat built to dist/gwat