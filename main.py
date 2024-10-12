from fastapi import FastAPI
import pandas as pd
from config import movies
from endpoints import endpoint_cantidadfiltrada, endpoint_recomendacion, endpoint_detalle_filmacion

app = FastAPI()
@app.get('/')  # type: ignore
async def root():
    return {'message':'hola mundo'}

app.include_router(endpoint_cantidadfiltrada.router)

app.include_router(endpoint_detalle_filmacion.router)

app.include_router(endpoint_recomendacion.router)