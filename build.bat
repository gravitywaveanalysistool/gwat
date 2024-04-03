@echo off
echo installing python requirements...
python3 -m pip install -r requirements.txt
echo building gwat...
python3 -m PyInstaller -D -w src/__init__.py -n gwat -p src/ --copy-metadata numpy -i src/media/logo_notext_icon.ico --add-data pro/:pro/ --clean -y
echo cleaning up...
del build /s /f /Q >nul
for /f %%f in ('dir /ad /b build\') do rd /s /q build\%%f >nul
rd build
del gwat.spec
echo gwat built to dist/gwat