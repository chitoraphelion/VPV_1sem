import pandas as pd
from astroquery.jplhorizons import Horizons

def get_orbital_elements(object_id, epochs=None):
    """
    Получает орбитальные элементы объекта по его ID из базы JPL Horizons
    и сохраняет в pandas DataFrame.
    
    Параметры:
        object_id: int or str
            ID объекта в базе JPL Horizons.
        epochs: list or str
            Список дат в юлианских днях или диапазон.
            
    Возвращает:
        pandas.DataFrame с орбитальными элементами и другой полезной информацией.
    """
    if epochs is None:
        # Задаем дату по умолчанию, если не указаны эпохи
        epochs = ['2024-01-01']
    
    # Создаем запрос в JPL Horizons для объекта
    obj = Horizons(id=object_id, location='@sun', epochs=epochs)
    
    # Получаем орбитальные элементы и другую информацию
    try:
        elements = obj.elements()
        df = elements.to_pandas()
    except Exception as e:
        raise ValueError(f"Ошибка при выполнении запроса: {e}")
    
    return df
