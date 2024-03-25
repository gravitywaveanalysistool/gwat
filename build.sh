if [ $(uname) == "Linux" ]; then
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install python3 python3 python3-venv python-gdl -y
        python3 -m venv pyenv
        cp `dpkg -L python-gdl | grep .so` `find pyenv -type d -name site-packages`

    elif command -v yum >/dev/null 2>&1; then
        sudo yum install python3 python3 python3-venv python3-gdl -y
        python3 -m venv pyenv
        

    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install python3 python3 python3-venv python3-gdl -y
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
python3 -m pip install numpy matplotlib tk pandas
