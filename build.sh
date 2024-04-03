if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi
${PYTHON} -m pip install -r requirements.txt
if [ ! d out ]; then
    mkdir out
fi
if [ $(uname) == "Linux" ]; then
    ${PYTHON} -m PyInstaller -D src/__init__.py -n gwat -p src/ --copy-metadata numpy --add-data pro/:pro/ --clean
elif [ $(uname) == "Darwin" ]; then
    ${PYTHON} -m PyInstaller -D -w src/__init__.py -n gwat -p src/ --copy-metadata numpy -i src/media/logo_notext_icon.ico --add-data pro/:pro/ --clean
else
    echo "unknown OS"
    exit 1 
fi
chmod +x dist/gwat/gwat
rm -rf build
rm gwat.spec
echo "built to dist/gwat"
