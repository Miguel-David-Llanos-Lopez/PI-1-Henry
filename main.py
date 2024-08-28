# se importan las librerias necesarias
from fastapi import FastAPI
import pandas as pd
from scipy.sparse import hstack
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# se lee el archivo
movies = pd.read_csv('./data/movies_limpio.csv')
# se transforma la columna 'release_date' en datetime para extraer las fechas correctamente mas tarde
movies['release_date'] = pd.to_datetime(movies['release_date'], format='%Y-%m-%d', errors='coerce')

# se realiza el preprsesamiento antes de crear los endpoints para ejecutarlo solo una vez y tenerlo disponible cuando se requiera
moviesML = pd.read_csv('./data/moviesML.csv')
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

app = FastAPI()
# para ver si la API despliega correctamente
@app.get('/')  # type: ignore
async def root():
    return {'message':'hola mundo'}

@app.get('/cantidad_filmaciones_mes/{mes}')
async def cantidad_filmaciones_mes(mes:str):
    """ se ingresa un mes en español y retorna la cantidad de filmaciones estrenadas ese mes 

    Args:
        mes (str): un mes en español puede estar con o sin mayusculas ej: Enero

    Returns:
        str: x películas fueron estrenadas en el mes de x
    """
    cantidad_filmaciones = 0
    meses_es = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7,
                'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
    mes = mes.lower().strip()
    for i in meses_es:
        if i == mes:
            mes_buscado = meses_es[i]
    if not mes_buscado:
        return 'seleccione un mes valido'
    for j in movies['release_date'].dt.month:
        if j == mes_buscado:
            cantidad_filmaciones += 1

    return f'{cantidad_filmaciones} películas fueron estrenadas en el mes de {mes}'

@app.get('/cantidad_filmaciones_dia/{dia}')
async def cantidad_filmaciones_dia(dia:str):
    """ se ingresa un dia de la semana en español y retorna la cantidad de filmaciones estrenadas ese dia

    Args:
        mes (str): un dia de la semana en español puede estar con o sin mayusculas ej: Lunes

    Retorna:
        str: x películas fueron estrenadas en los dias x
    """
    cantidad_filmaciones = 0
    dias_es = {'lunes':0, 'martes':1, 'miercoles':2, 'miércoles':2, 'jueves':3,
                'viernes':4, 'sabado':5,'sábado':5, 'domingo':6}
    dia = dia.lower().strip()
    for i in dias_es:
        if i == dia:
            dia_buscado = dias_es[i]
    if dia_buscado == None:
        return 'seleccione un dia valido'
    for j in movies['release_date'].dt.day_of_week:
        if j == dia_buscado:
            cantidad_filmaciones += 1

    return f'{cantidad_filmaciones} películas fueron estrenadas en los días {dia}'

@app.get('/titulo_de_la_filmación/{titulo}')
async def score_titulo(titulo:str):
    """se ingresa un titulo de pelicula y se buscara en el dataframe si hay coincidencias, en caso de haberlas
    se regresara un texto con el año de estreno popularidad y titulo de la filmacion

    Args:
        titulo (str): el nombre de la filmacion con o sin mayusculas Ej: Cars 2

    Returns:
        str: La película x fue estrenada en el año x con un score/popularidad de x

    """
    scores = movies[['popularity', 'release_year', 'title']]
    score_filmacion = scores[scores['title'].str.lower() == titulo.lower().strip()]
    if score_filmacion.empty:
        return f'No se encontró información para la película {titulo}.'
    return f'La película {score_filmacion.iloc[0]["title"]} fue estrenada en el año {score_filmacion.iloc[0]["release_year"]} con un score/popularidad de {score_filmacion.iloc[0]["popularity"]}'

@app.get('/votos_titulo/{titulo_de_la_filmacion}')
async def votos_titulo(titulo_de_la_filmacion:str):
    """ se ingresa un titulo de pelicula y se buscara en el dataframe si hay coincidencias, en caso de haberlas
        se regresara un texto con el año de estreno, promedio de votos, conteo de votos y titulo de la filmacion.
        la pelicula debera tener mas de 2000 votos para proporcionar la informacion

    Args:
        titulo_de_la_filmacion (str): el nombre de la filmacion con o sin mayusculas Ej: Cars 2

    Returns:
        str: La película x fue estrenada en el año x La misma cuenta con un total de x valoraciones, con un promedio de x
    """
    votos = movies[['release_year', 'title', 'vote_average', 'vote_count']]
    votos_filmacion = votos[votos['title'].str.lower() == titulo_de_la_filmacion.lower().strip()]
    if votos_filmacion.empty:
        return f'No se encontró información para la película {titulo_de_la_filmacion}.'
    elif votos_filmacion.iloc[0]['vote_count'] < 2000:
        return f'los votos para la pelicula {titulo_de_la_filmacion} son insuficientes para proporcionar la informacion'
    else:
        return f'La película {votos_filmacion.iloc[0]["title"]} fue estrenada en el año {votos_filmacion.iloc[0]["release_year"]} La misma cuenta con un total de {votos_filmacion.iloc[0]["vote_count"]} valoraciones, con un promedio de {votos_filmacion.iloc[0]["vote_average"]}'

@app.get('/get_actor/{actor}')
async def get_actor(nombre_actor:str):
    """ se ingresa el nombre de un a actor y se buscara en el dataframe si hay coincidencias, en caso de haberlas
        se regresara un texto con el nombre, cantidad de filmaciones en las que ha participado, el retorno total de las perliculas 
        y el retorno promedio por filmacion
        no se contaran las peliculas donde el actor sea tambien director

    Args:
        nombre_actor (str): el nombre del actor con o sin mayusculas Ej: Chris Casamassa

    Returns:
        str: El actor x ha participado de x cantidad de filmaciones, el mismo ha conseguido un retorno de x con un promedio de x por filmacion')
    """
    actores_validos = movies[movies['director'].str.lower() != nombre_actor.lower().strip()]
    
    movies_filtrado = actores_validos[actores_validos['cast'].apply(lambda x: isinstance(x, str) and nombre_actor in x.split(', '))]
    conteo = movies_filtrado.shape[0]
    retorno_total = movies_filtrado['return'].sum()
    if conteo == 0:
        return (f'El nombre ingresado {nombre_actor} no ha participado en ninguna de estas peliculas')
    else:
        retorno_promedio = retorno_total/conteo
        return (f'El actor {nombre_actor} ha participado de {conteo} cantidad de filmaciones, el mismo ha conseguido un retorno de {round(retorno_total,2)} con un promedio de {round(retorno_promedio,2)} por filmacion')

@app.get('/get_director/{director}')
async def get_director(director:str):
    """ se ingresa el nombre de un director y se buscara en el dataframe si hay coincidencias, en caso de haberlas
        se regresara un texto con el nombre, filmaciones en las que ha participado y el retorno total de las perliculas 
        no se contaran las peliculas donde el actor sea tambien director

    Args:
        director (str): el nombre del director con o sin mayusculas Ej: Michael Mann

    Returns:
        str: el director x ha obtenido un retorno de x sus filmaciones han sido x
    """
    filmaciones_por_director = movies[movies['director'].str.lower() == director.lower().strip()]
    retorno_total = filmaciones_por_director['return'].sum()
    filmaciones = []
    for i in range(0, filmaciones_por_director.shape[0]):
        filmaciones.append(f"{filmaciones_por_director.iloc[i]['title']} del año {filmaciones_por_director.iloc[i]['release_year']} obtuvo un retorno de {filmaciones_por_director.iloc[i]['return']}, la filmacion tuvo un costo de {filmaciones_por_director.iloc[i]['budget']} y una gancia de {filmaciones_por_director.iloc[i]['revenue']}")
    return f'el director {director} ha obtenido un retorno de {retorno_total} sus filmaciones han sido {filmaciones}'

@app.get('/recomendacion/{titulo}')
async def recomendacion(titulo:str):
    """ Se ingresa un titulo de pelicula y se buscara en el dataframe si hay coincidencias, en caso de haberlas
        se regresara una lista con las 5 peliculas mas parecidas a la ingresada

    Args:
        titulo (str): el nombre de la filmacion con o sin mayusculas Ej: Cars 2

    Returns:
        str: retorna una lista de las 5 peliculas mas parecidas a la pelicula ingresada
    """
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