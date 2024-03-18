BUILD_OS=$(uname)
if [[ ${BUILD_OS} == *"MSYS"* ]] || [[ ${BUILD_OS} == *"MINGW"* ]]; then
    BUILD_OS="Windows"
elif [[ ${BUILD_OS} == "Darwin" ]]; then
    BUILD_OS="macOS"
    Platform=${Platform:-$(arch)}
fi

if [ ${BUILD_OS} == "Windows" ]; then

elif [ ${BUILD_OS} == "Linux" ]; then

    # if command -v apt-get >/dev/null 2>&1; then
    #     sudo apt-get install curl cmake g++ python3-venv -y
    # else
    #     log "Fatal error: unsupported package manager."
    #     exit 1
    #     # yum and zypper package install for curl cmake g++ python3-venv
    # fi

else
    log "Fatal error: unknown operating system."
    exit 1
fi

cd lib/gdl
./scripts/build_gdl.sh install_toolchain
./scripts/build_gdl.sh prep
./scripts/build_gdl.sh configure
./scripts/build_gdl.sh build
cd ../..
GDL_DLL=`find ./lib/gdl/build -name 'GDL.so'`
python3 -m venv pyenv
INSTALL_DIR=`find pyenv -type d -name 'site-packages'`
cp ${GDL_DLL} ${INSTALL_DIR}/GDL.so
source ./pyenv/bin/activate
pip install numpy matplotlib tk
