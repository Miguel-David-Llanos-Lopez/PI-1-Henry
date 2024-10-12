import pandas as pd
from scipy.sparse import hstack
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from config import moviesML


vectorizer = TfidfVectorizer(stop_words='english')
lista_matrices = []
# se convierten las columnas en vectores
for i in moviesML.columns:
    matriz = vectorizer.fit_transform(moviesML[i])
    lista_matrices.append(matriz)

# se apilan las columnas de forma horizontal para que encajen con la entrada de datos que espera el modelo
combinacion_matrices = hstack(lista_matrices).tocsr()

def similitud_coseno(idx, matriz):
    return cosine_similarity(matriz[idx], matriz).flatten()


def recomendar(titulo:str):
    titulo_filmacion = moviesML[moviesML['title'].str.lower() == titulo.lower().strip()]
    if titulo_filmacion.empty:
        return f'La película {titulo} no existe en la base de datos'
    idmovie = titulo_filmacion.index[0]
    score = similitud_coseno(idmovie, combinacion_matrices)
    lista_pelis = list(enumerate(score))
    lista_pelis = sorted(lista_pelis, key=lambda x: x[1], reverse=True)
    lista_pelis = lista_pelis[1:6]
    indices = [i[0] for i in lista_pelis]
    return moviesML['title'].iloc[indices].tolist() # type: ignore