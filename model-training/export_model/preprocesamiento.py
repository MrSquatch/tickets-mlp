"""
Modulo de preprocesamiento personalizado para el proyecto de clasificacion
de tickets de soporte tecnico.

Este archivo debe estar disponible tanto en el entorno de entrenamiento
(notebook) como en el backend de FastAPI, ya que el pipeline exportado
con joblib necesita esta clase definida para poder cargarse correctamente.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class AfectadosTransformer(BaseEstimator, TransformerMixin):
    """
    Transforma la columna 'Afectados' (texto) en dos columnas numericas:
    - Aplica_Afectados (0/1): indica si el campo es relevante para esa fila
      (0 para PC Docente y Proyector, que usan 'No aplica')
    - Afectados_ordinal (0-3): nivel de afectacion, respetando el orden real
      (1 PC < 2-5 PCs < Mas de 5 PCs < Todo el laboratorio)
    """

    def __init__(self):
        self.mapeo = {
            "1 PC": 0,
            "2-5 PCs": 1,
            "Mas de 5 PCs": 2,
            "Todo el laboratorio": 3
        }

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        afectados = X['Afectados'] if isinstance(X, pd.DataFrame) else X.iloc[:, 0]
        aplica = (afectados != 'No aplica').astype(int)
        ordinal = afectados.map(self.mapeo).fillna(0).astype(int)
        return np.column_stack([aplica, ordinal])

    def get_feature_names_out(self, input_features=None):
        return ['Aplica_Afectados', 'Afectados_ordinal']