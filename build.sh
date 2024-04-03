python3 -m pip install -r requirements.txt
if [ ! d out ]; then
    mkdir out
fi
if [ $(uname) == "Linux" ]; then
    python3 -m PyInstaller -D src/__init__.py -n gwat -p src/ --copy-metadata numpy --add-data pro/:pro/ --clean
elif [ $(uname) == "Darwin" ]; then
    python3 -m PyInstaller -D -w src/__init__.py -n gwat -p src/ --copy-metadata numpy -i src/media/logo_notext_icon.ico --add-data pro/:pro/ --clean
else
    echo "unknown OS"
    exit 1 
fi
rm -rf build
rm gwat.spec
echo "built to dist/gwat"
