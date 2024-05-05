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
    echo "Error, make sure there's a valid path in your \$PATH"
    exit 1
fi
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR"
fi
WRAPPER_SCRIPT=$WRAPPER_PATH
source "${VENV_DIR}/bin/activate"
pip install .
cat << EOF > "$WRAPPER_SCRIPT"
#!/bin/bash
VENV_DIR="$VENV_DIR"
source "\${VENV_DIR}/bin/activate"
pyamp
EOF
chmod +x "$WRAPPER_SCRIPT"
deactivate
