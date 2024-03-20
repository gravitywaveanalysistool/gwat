function install_package {
    if [ $(uname) == "Linux" ]; then
        if command -v apt >/dev/null 2>&1; then
            sudo apt update
            sudo apt install $@ -y
        elif command -v yum >/dev/null 2>&1; then
            sudo yum install $@ -y
        elif command -v zypper >/dev/null 2>&1; then
            sudo zypper install $@ -y
        else
            echo "Fatal error: unsupported package manager."
            exit 1
        fi
    else
        echo "Fatal error: unsupported operating system."
        exit 1
    fi

}

install_package python3 python3-venv
python3 -m venv pyenv
source ./pyenv/bin/activate
pip install numpy matplotlib tk
install_package python3-gdl
