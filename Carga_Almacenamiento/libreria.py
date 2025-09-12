# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# %%
def _p(path):
    return Path(path).expanduser().resolve()

# %%
def cargar_csv(path, sep=",", encoding="utf-8", **kwargs):
    return pd.read_csv(_p(path), sep=sep, encoding=encoding, **kwargs)

# %%
def cargar_xlsx(path, hoja=0, **kwargs):
    return pd.read_excel(_p(path), sheet_name=hoja, engine="openpyxl", **kwargs)

# %%
def cargar_html(path_o_url, tabla=0, **kwargs):
    tablas = pd.read_html(str(path_o_url), **kwargs)  
    if tabla is None:
         return tablas
    return tablas[tabla]

# %%
def cargar_json(path, orient=None, **kwargs):
    p = _p(path)
    try:
        return pd.read_json(p, orient=orient, **kwargs)
    except ValueError:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.json_normalize(data)

# %%
def cargar_auto(path, **kwargs):
    ext = Path(path).suffix.lower()
    if ext == ".csv":
        return cargar_csv(path, **kwargs)
    if ext in (".xlsx", ".xls"):
        return cargar_xlsx(path, **kwargs)
    if ext in (".html", ".htm"):
        # para HTML suele tener sentido 'tabla=0'
        return cargar_html(path, **kwargs)
    if ext == ".json":
        return cargar_json(path, **kwargs)
    raise ValueError(f"Extensión no soportada: {ext}")

# %%
def forward_fill(df, columns=None, limit=None, inplace=False):
    objetivo = df if inplace else df.copy()
    if columns is None:
        objetivo= objetivo.ffill(limit=limit)
    else: 
        objetivo[columns]=objetivo[columns].ffill(limit=limit)
    return objetivo


# %%
def backward_fill(df, columns=None, limit=None, inplace=False):
    objetivo = df if inplace else df.copy()
    if columns is None:
        objetivo = objetivo.bfill(limit=limit)
    else:
        objetivo[columns]=objetivo[columns].bfill(limit=limit)
    return objetivo

# %%
def metodo_string(df, string, inplace=False):
    objetivo = df if inplace else df.copy()
    columnas_texto=[]
    for x in objetivo.columns:
        if objetivo[x].dtype == 'object':
            columnas_texto.append(x)
    objetivo.loc[:, columnas_texto] = objetivo.loc[:, columnas_texto].fillna(str(string))
    return objetivo

# %%
def promedio(df, inplace=False):
    objetivo = df if inplace else df.copy()
    cols_num = objetivo.select_dtypes(include='number').columns 

    if len(cols_num) == 0:
        return objetivo 

    medias = objetivo[cols_num].mean()
    objetivo.loc[:, cols_num] = objetivo.loc[:, cols_num].fillna(medias)
    return objetivo

# %%
def mediana(df, inplace=False):
    objetivo = df if inplace else df.copy()
    cols_num = objetivo.select_dtypes(include='number').columns 

    if len(cols_num) == 0:
        return objetivo 

    mediana = objetivo[cols_num].median()
    objetivo.loc[:, cols_num] = objetivo.loc[:, cols_num].fillna(mediana)
    return objetivo

# %%
def constante(df, constante, inplace=False):
    objetivo = df if inplace else df.copy()
    cols_num = objetivo.select_dtypes(include='number').columns 

    if len(cols_num) == 0:
        return objetivo 

    objetivo.loc[:, cols_num] = objetivo.loc[:, cols_num].fillna(constante)
    return objetivo

# %%
def nulos_en_dataframe(df):
  
    total_celdas = int(df.size)
    total_nulos = int(df.isna().sum().sum())
    pct_nulos = round((total_nulos / total_celdas) * 100, 2) if total_celdas else 0.0
    filas_con_nulos = int(df.isna().any(axis=1).sum())
    columnas_con_nulos = int(df.isna().any(axis=0).sum())

    return {
        "filas": int(len(df)),
        "columnas": int(df.shape[1]),
        "total_celdas": total_celdas,
        "total_nulos": total_nulos,
        "%_nulos_df": pct_nulos,
        "filas_con_algun_nulo": filas_con_nulos,
        "columnas_con_algun_nulo": columnas_con_nulos,
    }

def filas_impares(df):
    objetivo = df.iloc[1::2]
    return objetivo
