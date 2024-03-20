export DEPS="headless"

BUILD_OS=$(uname)
if [[ ${BUILD_OS} == *"MSYS"* ]] || [[ ${BUILD_OS} == *"MINGW"* ]]; then
    BUILD_OS="Windows"
elif [[ ${BUILD_OS} == "Darwin" ]]; then
    BUILD_OS="macOS"
    Platform=${Platform:-$(arch)}
fi

if [ ${BUILD_OS} == "Windows" ]; then
    if [ ${Platform:-`uname -m`} == "x86_64" ]; then
        export mname="mingw64"
        export MSYSTEM="MINGW64"
        export arch="x86_64"
    else
        export mname="mingw32"
        export MSYSTEM="MINGW32"
        export arch="i686"
    fi

    pacman -S --noconfirm --needed mingw-w64-${arch}-python mingw-w64-${arch}-python-pip
    python3 -m pip install virtualenv
    python3 -m virtualenv pyenv

elif [ ${BUILD_OS} == "Linux" ]; then
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install curl cmake g++ make python3 python3-venv -y
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install curl cmake gcc-c++ make python3 python3-venv -y
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install curl cmake gcc-c++ make python3 python3-venv -y
    else
        log "Fatal error: unsupported package manager."
        exit 1
    fi

    python3 -m venv pyenv
elif [ ${BUILD_OS} == "macOS" ]; then
    if ! command -v brew >/dev/null 2>&1; then
        log "Fatal error! Homebrew not found."
        exit 1
    fi
    brew update-reset
    brew install venv
    python3 -m venv pyenv
else
    log "Fatal error: unsupported operating system."
    exit 1
fi

cd lib/gdl
./scripts/build_gdl.sh prep
./scripts/build_gdl.sh configure
./scripts/build_gdl.sh build
cd ../..

GDL_DLL=`find ./lib/gdl/build -name 'GDL.so'`
INSTALL_DIR=`find pyenv -type d -name 'site-packages'`
cp ${GDL_DLL} ${INSTALL_DIR}/GDL.so
source ./pyenv/bin/activate
pip install numpy matplotlib tk
