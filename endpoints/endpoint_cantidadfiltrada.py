from fastapi import APIRouter
from services.cantidad_filtrada import filtrar_cantidad_por_fecha

router = APIRouter()

@router.get('/cantidad_filmaciones_mes/{mes}')
async def cantidad_filmaciones_mes(mes):
    filtro = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7,
                'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
    return filtrar_cantidad_por_fecha(mes ,filtro=filtro, tipo='mes')


@router.get('/cantidad_filmaciones_dia/{dia}')
async def cantidad_filmaciones_dia(dia):
    filtro = {'lunes':0, 'martes':1, 'miercoles':2, 'miércoles':2, 'jueves':3,
                'viernes':4, 'sabado':5,'sábado':5, 'domingo':6}
    return filtrar_cantidad_por_fecha(dia ,filtro=filtro, tipo='dia')