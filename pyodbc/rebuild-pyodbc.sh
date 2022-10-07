#!/bin/bash

echo "\npyodbc acquired from https://pypi.org/project/pyodbc/#files\n"
read -p "Ensure your venv is active, and press Return to continue> "

echo "brew install unixodbc"
brew install unixodbc

set -x

python3 -m pip uninstall pyodbc

export CPPFLAGS="-I/opt/homebrew/Cellar/unixodbc/2.3.11/include"
export LDFLAGS="-L/opt/homebrew/Cellar/unixodbc/2.3.11/lib -liodbc -liodbcinst"

python3 -m pip install pyodbc
