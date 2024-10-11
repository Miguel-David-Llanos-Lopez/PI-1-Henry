from fastapi import APIRouter
from services.servicio_recomendacion import recomendar

router = APIRouter()

@router.get('/recomendacion{titulo}')
async def recomendacion(titulo):
    """Devuelve las 5 películas más similares al título dado."""
    return recomendar(titulo)