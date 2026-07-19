#!/bin/bash
# Activar el entorno virtual .venv
source /root/tickets-mlp/.venv/bin/activate

# Iniciar sqlite-web apuntando a la base de datos de tickets
sqlite_web tickets.db --host 0.0.0.0 --port 8080
