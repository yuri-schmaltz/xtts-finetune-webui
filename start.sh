#!/bin/bash

if [ ! -d "venv" ]; then
  echo "Virtual environment not found. Run install.sh first."
  exit 1
fi

source venv/bin/activate

python -m src.xtts_demo

