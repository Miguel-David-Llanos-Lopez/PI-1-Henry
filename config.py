import pandas as pd

# se lee el archivo
movies = pd.read_csv('./data/movies_limpio.csv')
# se transforma la columna 'release_date' en datetime para extraer las fechas correctamente mas tarde
movies['release_date'] = pd.to_datetime(movies['release_date'], format='%Y-%m-%d', errors='coerce')