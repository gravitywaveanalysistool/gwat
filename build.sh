APT_PACKAGES=(python3 python3 python3-venv python-gdl zlib1g-dev libjpeg-dev libpng-dev)
RPM_PACKAGES=(python3 python3 python3-venv python3-gdl zlib-devel libjpeg-devel libpng-devel)

if [ $(uname) == "Linux" ]; then
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install ${APT_PACKAGES[@]} -y
        python3 -m venv pyenv
        # cp `dpkg -L python-gdl | grep .so` `find pyenv -type d -name site-packages`

    elif command -v yum >/dev/null 2>&1; then
        sudo yum install ${RPM_PACKAGES[@]} -y
        python3 -m venv pyenv
        

    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install ${RPM_PACKAGES[@]} -y
        python3 -m venv pyenv
        
    else
        echo "Fatal error: unsupported package manager."
        exit 1
    fi
else
    echo "Fatal error: unsupported operating system."
    exit 1
fi

source ./pyenv/bin/activate
python3 -m pip install numpy matplotlib tk pandas pillow tabulate metpy pyinstaller --upgrade
pyinstaller src/__init__.py -n gwat
