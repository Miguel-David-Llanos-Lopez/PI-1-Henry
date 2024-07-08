#
from fastapi import FastAPI
import pandas as pd
from scipy.sparse import hstack
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')


movies = pd.read_csv('./data/movies_limpio.csv')
movies['release_date'] = pd.to_datetime(movies['release_date'], format='%Y-%m-%d', errors='coerce')

moviesML = pd.read_csv('../data/moviesEDA.csv')
vectorizer = TfidfVectorizer(stop_words='english')
lista_matrices = []
for i in moviesML.columns:
    matriz = vectorizer.fit_transform(moviesML[i])
    lista_matrices.append(matriz)

combinacion_matrices = hstack(lista_matrices).tocsr() if len(lista_matrices) > 1 else lista_matrices[0]

def similitud_coseno(idx, matriz):
    return cosine_similarity(matriz[idx], matriz).flatten()

app = FastAPI()

@app.get('/')  # type: ignore
async def root():
    return {'message':'hola mundo'}

@app.get('/cantidad_filmaciones_mes/{mes}')
async def cantidad_filmaciones_mes(mes:str):
    cantidad_filmaciones = 0
    meses_es = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7,
                'agosto':8, 'septiembre':9, 'octubre':10, 'nobiembre':11, 'diciembre':12}
    mes = mes.lower()
    for i in meses_es:
        if i == mes:
            mes_buscado = meses_es[i]
    if not mes_buscado:
        return 'seleccione un mes valido'
    for j in movies['release_date'].dt.month:
        if j == mes_buscado:
            cantidad_filmaciones += 1

    return f'{cantidad_filmaciones} cantidad de películas fueron estrenadas en el mes de {mes}'

@app.get('/cantidad_filmaciones_dia/{dia}')
async def cantidad_filmaciones_dia(dia:str):
    cantidad_filmaciones = 0
    dias_es = {'lunes':0, 'martes':1, 'miercoles':2, 'miércoles':2, 'jueves':3,
                'viernes':4, 'sabado':5,'sábado':5, 'domingo':6}
    dia = dia.lower()
    for i in dias_es:
        if i == dia:
            dia_buscado = dias_es[i]
    if dia_buscado == None:
        return 'seleccione un dia valido'
    for j in movies['release_date'].dt.day_of_week:
        if j == dia_buscado:
            cantidad_filmaciones += 1

    return f'{cantidad_filmaciones} cantidad de películas fueron estrenadas en los días {dia}'

@app.get('/titulo_de_la_filmación/{titulo}')
async def score_titulo(titulo:str):
    scores = movies[['popularity', 'released_year', 'title']]
    score_filmacion = scores[scores['title'].str.lower() == titulo.lower()]
    if score_filmacion.empty:
        return f'No se encontró información para la película {titulo}.'
    return f'La película {score_filmacion.iloc[0]["title"]} fue estrenada en el año {score_filmacion.iloc[0]["released_year"]} con un score/popularidad de {score_filmacion.iloc[0]["popularity"]}'

@app.get('/votos_titulo/{titulo_de_la_filmacion}')
async def votos_titulo(titulo_de_la_filmacion:str):
    votos = movies[['released_year', 'title', 'vote_average', 'vote_count']]
    votos_filmacion = votos[votos['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if votos_filmacion.empty:
        return f'No se encontró información para la película {titulo_de_la_filmacion}.'
    elif votos_filmacion.iloc[0]['vote_count'] < 2000:
        return f'los votos para la pelicula {titulo_de_la_filmacion} son insuficientes para proporcionar la informacion'
    else:
        return f'La película {votos_filmacion.iloc[0]["title"]} fue estrenada en el año {votos_filmacion.iloc[0]["released_year"]} La misma cuenta con un total de {votos_filmacion.iloc[0]["vote_count"]} valoraciones, con un promedio de {votos_filmacion.iloc[0]["vote_average"]}'

#@app.get('/get_actor/{actor}')
#async def get_actor(nombre_actor):

@app.get('/votos_titulo/{titulo}')
async def recomendacion(titulo):
    titulo_filmacion = moviesML[moviesML['title'].str.lower() == titulo.lower()]
    if titulo_filmacion.empty:
        return f'La película {titulo} no existe en la base de datos'
    idx = titulo_filmacion.index[0]
    score = similitud_coseno(idx, combinacion_matrices)
    lista_pelis = list(enumerate(score))
    lista_pelis = sorted(lista_pelis, key=lambda x: x[1], reverse=True)
    lista_pelis = lista_pelis[1:6]
    indices = [i[0] for i in lista_pelis]
    return moviesML['title'].iloc[indices].tolist() # type: ignore