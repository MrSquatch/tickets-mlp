# 📊 model-training

Esta carpeta contiene todo lo relacionado al dataset, la visualización exploratoria 
de los datos y el entrenamiento del modelo de clasificación (MLP).

## 📂 Contenido

```
model-training/
├── dataset.csv           # Dataset sintético de tickets
├── training.ipynb         # Notebook: carga, visualizacion y analisis del dataset
├── export_model/
│   ├── export_model.ipynb  # Notebook: preprocesamiento, entrenamiento y exportacion del modelo
│   ├── preprocesamiento.py # Clase AfectadosTransformer, usada por el pipeline
│   └── model_v1.joblib     # Modelo entrenado, listo para usar en model-api/
└── start_jupyter.sh
```

## 🚀 Cómo iniciar Jupyter

Antes que nada, asegúrate de tener el entorno virtual activado (ver el
[README principal](../README.md) si aún no lo creaste):

```bash
source ../.venv/bin/activate
```

Luego, desde esta carpeta, simplemente ejecuta:

```bash
./start_jupyter.sh
```

Esto es todo lo necesario — dado que el proyecto ya está montado en el
servidor de la facultad, una vez que Jupyter esté corriendo puedes acceder
a él directamente desde el navegador, sin ninguna configuración adicional:

```
http://192.168.30.40:8888/
```

## 📓 Notebooks

- **`training.ipynb`** 📈: carga el dataset y genera las visualizaciones
  exploratorias (distribución por pabellón, categoría, criticidad, etc.).
- **`export_model/export_model.ipynb`** 🧠: toma el dataset, lo transforma
  (one-hot encoding, tratamiento de la columna Afectados), entrena el MLP,
  lo evalúa, y finalmente exporta el modelo (`model_v1.joblib`) junto con
  una copia de sus archivos hacia `model-api/`, dejándolo listo para
  producción.

## 📝 Nota sobre `preprocesamiento.py`

Este archivo define una transformación personalizada (`AfectadosTransformer`)
necesaria para que el pipeline de scikit-learn funcione correctamente. Es
importado tanto en `export_model.ipynb` como en el backend de `model-api/`
— si se modifica la lógica de esta clase, ambas copias deben actualizarse
para mantenerse sincronizadas. 🔄
