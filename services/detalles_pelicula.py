from config import movies


def score_titulo(titulo:str):
    scores = movies[['popularity', 'release_year', 'title']]
    score_filmacion = scores[scores['title'].str.lower() == titulo.lower().strip()]
    if score_filmacion.empty:
        return f'No se encontró información para la película {titulo}.'
    return f'La película {score_filmacion.iloc[0]["title"]} fue estrenada en el año {score_filmacion.iloc[0]["release_year"]} con un score/popularidad de {score_filmacion.iloc[0]["popularity"]}'

def votos_titulo(titulo_de_la_filmacion:str):
    votos = movies[['release_year', 'title', 'vote_average', 'vote_count']]
    votos_filmacion = votos[votos['title'].str.lower() == titulo_de_la_filmacion.lower().strip()]
    if votos_filmacion.empty:
        return f'No se encontró información para la película {titulo_de_la_filmacion}.'
    elif votos_filmacion.iloc[0]['vote_count'] < 2000:
        return f'los votos para la pelicula {titulo_de_la_filmacion} son insuficientes para proporcionar la informacion'
    else:
        return f'La película {votos_filmacion.iloc[0]["title"]} fue estrenada en el año {votos_filmacion.iloc[0]["release_year"]} La misma cuenta con un total de {votos_filmacion.iloc[0]["vote_count"]} valoraciones, con un promedio de {votos_filmacion.iloc[0]["vote_average"]}'

def get_actor(nombre_actor:str):
    actores_validos = movies[movies['director'].str.lower() != nombre_actor.lower().strip()]
    
    movies_filtrado = actores_validos[actores_validos['cast'].apply(lambda x: isinstance(x, str) and nombre_actor in x.split(', '))]
    conteo = movies_filtrado.shape[0]
    retorno_total = movies_filtrado['return'].sum()
    if conteo == 0:
        return f'El nombre ingresado {nombre_actor} no ha participado en ninguna de estas peliculas'
    else:
        retorno_promedio = retorno_total/conteo
        return f'El actor {nombre_actor} ha participado de {conteo} cantidad de filmaciones, el mismo ha conseguido un retorno de {round(retorno_total,2)} con un promedio de {round(retorno_promedio,2)} por filmacion'

def get_director(director:str):
    filmaciones_por_director = movies[movies['director'].str.lower() == director.lower().strip()]
    retorno_total = filmaciones_por_director['return'].sum()
    filmaciones = []
    for i in range(0, filmaciones_por_director.shape[0]):
        filmaciones.append(f"{filmaciones_por_director.iloc[i]['title']} del año {filmaciones_por_director.iloc[i]['release_year']} obtuvo un retorno de {filmaciones_por_director.iloc[i]['return']}, la filmacion tuvo un costo de {filmaciones_por_director.iloc[i]['budget']} y una gancia de {filmaciones_por_director.iloc[i]['revenue']}")
    return f'el director {director} ha obtenido un retorno de {retorno_total} sus filmaciones han sido {filmaciones}'
