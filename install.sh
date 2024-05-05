#!/bin/bash

# Path to the virtual environment directory
VENV_DIR="$(pwd)/env/"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR"
fi

# Activate the virtual environment and install dependencies
source "${VENV_DIR}/bin/activate"

# Install your program using pip
pip install .

# Create the wrapper script
cat << EOF > $HOME/.local/bin/pyamp
#!/bin/bash

# Change this to the path where your virtual environment is located
VENV_DIR="$VENV_DIR"

# Activate the virtual environment
source "\${VENV_DIR}/bin/activate"

# Run your program
pyamp
EOF

# Make the wrapper script executable
chmod +x $HOME/.local/bin/pyamp

# Exits the venv
deactivate
