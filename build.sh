if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "python not found"
    exit 1
fi
if ! command -v ${PYTHON} -m pip >/dev/null 2>&1; then
    echo "pip not found"
    exit 1
fi
${PYTHON} -m pip install -r requirements.txt --upgrade
if [ ! d out ]; then
    mkdir out
fi
if [ $(uname) == "Linux" ]; then
    ${PYTHON} -m PyInstaller -D src/__init__.py -n gwat -p src/ --copy-metadata numpy --hidden-import='PIL._tkinter_finder' --add-data pro/:pro/ --add-data data/:data/ --clean
elif [ $(uname) == "Darwin" ]; then
    ${PYTHON} -m PyInstaller -D -w src/__init__.py -n gwat -p src/ --copy-metadata numpy --hidden-import='PIL._tkinter_finder' -i data/media/logo_notext_icon.ico --add-data pro/:pro/ --add-data data/:data/ --clean
else
    echo "unknown OS"
    exit 1 
fi
chmod +x dist/gwat/gwat
rm -rf build
rm gwat.spec
echo "built to dist/gwat"
