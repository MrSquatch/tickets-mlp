"""
Backend - Sistema de clasificacion de tickets (con modelo real + SQLite)

Estructura esperada en esta carpeta (model-api/):
    main.py
    database.py
    preprocesamiento.py
    model_v1.joblib
    tickets.db              <- se crea automaticamente al arrancar

Para correrlo:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Documentacion interactiva: http://localhost:8000/docs
"""

from contextlib import asynccontextmanager
from typing import Optional

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from preprocesamiento import AfectadosTransformer  # noqa: F401
from database import inicializar_db, registrar_ticket, get_connection


# --------------------------------------------
# Cargar el modelo UNA SOLA VEZ, al iniciar la aplicacion
# --------------------------------------------
try:
    pipeline = joblib.load("model_v1.joblib")
    print("[C_INFO]\t Modelo cargado correctamente.")
except FileNotFoundError:
    pipeline = None
    print("[C_ADVERTENCIA]\t No se encontro el archivo del modelo en 'model_v1.joblib'")


# --------------------------------------------
# Inicializar la base de datos al arrancar la aplicacion
# --------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_db()
    print("[C_INFO]\t Base de datos inicializada (tickets.db).")
    yield


app = FastAPI(title="API de Clasificacion de Tickets", lifespan=lifespan)


# --------------------------------------------
# Modelo de datos que esperamos recibir desde n8n
# --------------------------------------------
class Ticket(BaseModel):
    Pabellon: str
    Laboratorio: int
    Categoria: str
    Subcategoria: str
    Afectados: str
    Comentario: Optional[str] = None


# --------------------------------------------
# Endpoint de salud
# --------------------------------------------
@app.get("/")
def raiz():
    return {
        "status": "ok",
        "modelo_cargado": pipeline is not None
    }


# --------------------------------------------
# Endpoint principal: clasifica un ticket y lo registra en la BD
# --------------------------------------------
@app.post("/clasificar-ticket")
def clasificar_ticket(ticket: Ticket):
    if pipeline is None:
        raise HTTPException(
            status_code=500,
            detail="El modelo no esta cargado. Revisa que exista model_v1.joblib"
        )

    ticket_df = pd.DataFrame([{
        "Pabellon": ticket.Pabellon,
        "Laboratorio": ticket.Laboratorio,
        "Categoria": ticket.Categoria,
        "Subcategoria": ticket.Subcategoria,
        "Afectados": ticket.Afectados
    }])

    prediccion = pipeline.predict(ticket_df)[0]

    probabilidades = pipeline.predict_proba(ticket_df)[0]
    probabilidades_dict = {
        clase: round(float(prob), 4)
        for clase, prob in zip(pipeline.classes_, probabilidades)
    }

    # Registrar el ticket ya clasificado en la base de datos
    ticket_id = registrar_ticket(
        ticket_data=ticket.model_dump(),
        prediccion=prediccion
    )

    return {
        "id": ticket_id,
        "recibido": ticket.model_dump(),
        "criticidad_predicha": prediccion,
        "probabilidades": probabilidades_dict
    }
