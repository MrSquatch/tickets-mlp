#!/bin/bash

# Activar el entorno virtual .venv
source /root/tickets-mlp/.venv/bin/activate

# Iniciar Jupyter Lab usando el entorno
jupyter lab --ip=192.168.30.40 --port=8888 --no-browser --allow-root
