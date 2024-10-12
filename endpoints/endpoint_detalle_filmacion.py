from fastapi import APIRouter
from services.detalles_pelicula import score_titulo , votos_titulo, get_actor, get_director

router = APIRouter()

@router.get('/score_titulo/{titulo}')
async def score(titulo):
    return score_titulo(titulo)

@router.get('/votos_titulo/{titulo}')
async def votos(titulo):
    return votos_titulo(titulo)

@router.get('/votos_titulo/{titulo}')
async def actor(titulo):
    return get_actor(titulo)

@router.get('/votos_titulo/{titulo}')
async def director(titulo):
    return get_director(titulo)