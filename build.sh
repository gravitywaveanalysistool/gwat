python3 -m pip install -r requirements.txt
mkdir out
if [ $(uname) == "Linux" ]; then
    pyinstaller -D src/__init__.py -n gwat -p src/ --copy-metadata numpy --add-data pro/:pro/ --clean
elif [ $(uname) == "Darwin" ]; then
    pyinstaller -D -w src/__init__.py -n gwat -p src/ --copy-metadata numpy -i src/media/logo_notext_icon.ico --add-data pro/:pro/ --clean
else
    echo "unknown OS"
    exit 1 
fi
rm -rf build
rm gwat.spec
echo "built to dist/gwat"
