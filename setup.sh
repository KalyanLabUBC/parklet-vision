# Automatically sets up all of the files in this folder (the virtual
# environment for Jupyter, installs all of the packages, etc.)

#!/usr/bin/env bash

# Exit immediately if a command fails
set -e

# -------- CONFIG --------
VENV_DIR="./venv"
KERNEL_NAME="parklet_vision"
KERNEL_DISPLAY_NAME="Python (Parklet Vision)"
REQUIREMENTS_FILE="./requirements.txt"
PYTHON_BIN="python3"
# ------------------------

echo "Creating virtual environment in ${VENV_DIR}..."
${PYTHON_BIN} -m venv ${VENV_DIR}

echo "Activating virtual environment..."
source ${VENV_DIR}/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

if [ -f "${REQUIREMENTS_FILE}" ]; then
    echo "Installing requirements from ${REQUIREMENTS_FILE}..."
    pip install -r ${REQUIREMENTS_FILE}
else
    echo "WARNING: ${REQUIREMENTS_FILE} not found, skipping dependency install."
fi

echo "Installing ipykernel..."
pip install ipykernel

echo "Registering Jupyter kernel..."
python -m ipykernel install \
    --user \
    --name "${KERNEL_NAME}" \
    --display-name "${KERNEL_DISPLAY_NAME}"

echo "Setup complete!"
echo "To activate later, run:"
echo "  source ${VENV_DIR}/bin/activate"
