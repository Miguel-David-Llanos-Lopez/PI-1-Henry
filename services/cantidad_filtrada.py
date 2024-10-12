from config import movies

def filtrar_cantidad_por_fecha(valor_buscado:str, filtro:dict, tipo:str):
    cantidad_filmaciones = 0
    valor_buscado = valor_buscado.lower().strip()
    valor_encontrado = filtro.get(valor_buscado)
    if not valor_buscado:
        return f'Seleccione un {tipo} válido'
    for fecha in movies['release_date'].dt.month if tipo == "mes" else movies['date'].dt.dayofweek:
        if fecha == valor_encontrado:
            cantidad_filmaciones += 1
        return f'Cantidad de filmaciones en el {tipo} {valor_buscado}: {cantidad_filmaciones}'
