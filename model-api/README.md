# 🚀 model-api

Backend en FastAPI que carga el modelo entrenado, clasifica los tickets
recibidos desde n8n y los guarda en una base de datos SQLite.

## 📂 Contenido

```
model-api/
├── main.py                # Endpoints de la API (clasificacion + consulta de tickets)
├── database.py             # Conexion y operaciones sobre la base de datos SQLite
├── preprocesamiento.py     # Clase AfectadosTransformer (copia sincronizada desde model-training/)
├── model_v1.joblib          # Modelo entrenado (copia sincronizada desde model-training/)
├── tickets.db               # Base de datos SQLite (se genera automaticamente al iniciar la API)
├── start_backend.sh
└── start_dbviewer.sh
```

## ⚡ Servicios que corren en esta carpeta

Esta carpeta levanta **dos procesos independientes**: la API (FastAPI) y el
visor web de la base de datos (sqlite-web). Cada uno debe ejecutarse en su
propia terminal, ya que ambos quedan corriendo en primer plano.

### 1️⃣ Backend (API)

Basta con ejecutar:

```bash
./start_backend.sh
```

Esto levanta la API en el puerto 8000. Puedes probarla directamente desde
el navegador, usando la documentación interactiva que genera FastAPI:

```
http://192.168.30.40:8000/docs
```

Ahí se puede ver el detalle de cada endpoint y probar el envío de un ticket
de prueba sin necesidad de n8n ni Postman. 🧪

### 2️⃣ Visor de la base de datos

En una terminal **distinta** a la del backend:

```bash
./start_dbviewer.sh
```

Esto levanta `sqlite-web`, una interfaz visual para consultar y editar los
tickets guardados directamente desde el navegador:

```
http://192.168.30.40:8080/
```

## 📡 Endpoints principales de la API

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Verifica que la API esté corriendo y que el modelo se haya cargado ✅ |
| POST | `/clasificar-ticket` | Recibe un ticket, lo clasifica y lo guarda en la base de datos 🎫 |

## 📝 Nota sobre `preprocesamiento.py` y `model_v1.joblib`

Ambos archivos son copias generadas desde `model-training/export_model/`.
Si se reentrena el modelo o se modifica la lógica de preprocesamiento, es
necesario actualizar ambas copias para que el backend siga funcionando
correctamente con la versión más reciente. 🔄
