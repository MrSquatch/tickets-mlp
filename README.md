# 🎫 Clasificador Automático de Tickets - FISI

Sistema de clasificación automática de tickets de soporte técnico para los
laboratorios de cómputo de la facultad. Un modelo de Machine Learning
(Perceptrón Multicapa) analiza cada ticket reportado por los docentes y
predice su nivel de criticidad (**Baja**, **Media** o **Alta**), permitiendo
priorizar la atención del personal de soporte.

## ⚙️ ¿Cómo funciona el flujo completo?

1. 📝 El docente completa un formulario (alojado en n8n) reportando una
   incidencia en el laboratorio.
2. 📤 n8n arma el ticket y lo envía a la API (FastAPI).
3. 🤖 La API carga el modelo ya entrenado, clasifica el ticket y lo guarda
   en una base de datos SQLite.
4. 🚨 Si la criticidad es **Alta**, n8n envía una notificación por correo
   al personal de soporte.
5. 👀 Los tickets registrados pueden revisarse desde un visor web de la
   base de datos.

## 📂 Estructura del proyecto

```
tickets-mlp/
├── model-training/     # Generación de datos, visualización y entrenamiento del modelo
├── model-api/          # Backend (FastAPI) que sirve el modelo y gestiona los tickets
└── requirements.txt     # Dependencias compartidas del proyecto
```

Cada carpeta tiene su propio README con instrucciones específicas:
- 📊 [`model-training/README.md`](./model-training/README.md)
- 🚀 [`model-api/README.md`](./model-api/README.md)

## 🐍 Preparar el entorno (Python)

Todo el proyecto comparte un único entorno virtual, ubicado en la raíz.

> ⚠️ **Importante:** los scripts `.sh` del proyecto asumen que la carpeta
> se llama exactamente `.venv` — si le pones otro nombre, tendrás que
> ajustar esos scripts manualmente.

```bash
cd tickets-mlp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Cada vez que abras una terminal nueva para trabajar en el proyecto, recuerda
activar el entorno antes de correr cualquier script:

```bash
source .venv/bin/activate
```

## 🔗 n8n (formulario y automatización)

El formulario que reciben los docentes, junto con la lógica de envío del
ticket a la API y el envío de notificaciones por correo, está montado en
n8n, en un servidor separado del resto del proyecto:

```
http://192.168.30.25:5678/
```

## 🖥️ Servidor del proyecto (entrenamiento + API)

El resto del proyecto (Jupyter para entrenamiento, la API y el visor de
base de datos) corre en un servidor distinto, dentro de la red de la
facultad:

```
192.168.30.40
```

Ver el README de cada carpeta para las URLs específicas de cada servicio.
