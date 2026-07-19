#!/bin/bash

# Activar el entorno virtual .venv
source /root/tickets-mlp/.venv/bin/activate

# Iniciar servidor fastapi usando el entorno
uvicorn main:app --reload --host 0.0.0.0 --port 8000
