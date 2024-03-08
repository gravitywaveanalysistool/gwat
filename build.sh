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
sudo apt-get install curl cmake g++ python3-venv -y
cd lib/gdl
./scripts/build_gdl.sh prep
./scripts/build_gdl.sh configure
./scripts/build_gdl.sh build
cd ../..
GDL_DLL=`find ./lib/gdl/build -name 'GDL.so'`
python3 -m venv pyenv
INSTALL_DIR=`find pyenv -type d -name 'site-packages'`
cp ${GDL_DLL} ${INSTALL_DIR}/GDL.so
