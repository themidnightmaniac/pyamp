#!/bin/bash
VENV_DIR="$(pwd)/env"
BIN_DIRS=(
    "$HOME/.local/bin"
    "$HOME/bin"
    "/usr/local/bin"
    "/opt/"
)
for folder in "${BIN_DIRS[@]}"; do
    if [ -d "$folder" ] && [[ ":$PATH:" == *":$folder:"* ]]; then
        WRAPPER_PATH="$folder/pyamp"
        break
    fi
done
if [ -z "$WRAPPER_PATH" ]; then
    echo "ERROR: Make sure there's a valid path in your \$PATH"
    echo "Valid Paths:"
    echo $BIN_DIRS
    exit 1
fi
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR"
fi
WRAPPER_SCRIPT=$WRAPPER_PATH
source "${VENV_DIR}/bin/activate"
if [[ $1 = "-e" ]]; then
    echo "WARNING: Installing in editable mode!"
    pip install -e .
else
    pip install .
fi

cat << EOF > "$WRAPPER_SCRIPT"
#!/bin/bash
if [ -z "$VENV_DIR" ] || [ ! -d "$VENV_DIR" ]; then
    echo "Error: VENV_DIR is not set or does not exist or is not a directory: $VENV_DIR"
    exit 1
fi
VENV_DIR="$VENV_DIR"
source "\${VENV_DIR}/bin/activate"
pyamp
EOF
chmod +x "$WRAPPER_SCRIPT"
deactivate
mkdir $HOME/.config/pyamp
cp src/resources/onsongchange.sh $HOME/.config/pyamp/
chmod +x $HOME/.config/pyamp/onsongchange.sh