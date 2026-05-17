#!/bin/bash

VENV_PATH="/home/vision/projects/defect_detection/venv"

# Kiểm tra đã activate đúng venv chưa
if [[ "$VIRTUAL_ENV" != "$VENV_PATH" ]]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
fi

# Chạy FastAPI
python3 main.py