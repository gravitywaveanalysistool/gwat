# BUILD_OS=$(uname)
# if [[ ${BUILD_OS} == *"MSYS"* ]] || [[ ${BUILD_OS} == *"MINGW"* ]]; then
#     BUILD_OS="Windows"
# elif [[ ${BUILD_OS} == "Darwin" ]]; then
#     BUILD_OS="macOS"
#     Platform=${Platform:-$(arch)}
# fi

# if [ ${BUILD_OS} == "Windows" ]; then

# elif [ ${BUILD_OS} == "Linux" ]; then

#pretend ubuntu is the only os
sudo apt-get install curl cmake g++ python3-venv
cd lib/gdl
./scripts/build_gdl.sh prep
./scripts/build_gdl.sh configure
./scripts/build_gdl.sh build
GDL_DLL = `find ./build -filename 'GDL.so'`
cd ../..
mkdir gdl_build
python3 -m venv pyenv
cp ${GDL_DLL} pyenv/lib/**/site-packages/GDL.so
