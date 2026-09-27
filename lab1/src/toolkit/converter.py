from .errors import (
    below_absolute_zero_error,
    incompatible_units_error,
    unknown_unit_error,
)


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Конвертирует заданное число из одной единицы измерения в другую.

    Поддерживаются следующие категории и единицы:
    - Длина: 'mm', 'cm', 'm', 'km'
    - Масса: 'mg', 'g', 'kg', 'ton'
    - Температура: 'c' (Цельсий), 'f' (Фаренгейт), 'k' (Кельвин)

    Args:
        value (float | int): Исходное числовое значение для конвертации.
        from_unit (str): Исходная единица измерения (например, 'm', 'kg', 'c').
        to_unit (str): Целевая единица измерения (например, 'km', 'g', 'f').

    Returns:
        float | int: Преобразованное значение, округленное до 5 знаков после запятой,
            либо исходное значение, если единицы измерения совпадают.

    Raises:
        unknown_unit_error: Если указана неизвестная или неподдерживаемая единица измерения.
        incompatible_units_error: Если попытка конвертации происходит между разными
            физическими величинами (например, длины в массу).
        below_absolute_zero_error: Если переданная температура меньше или равна значению
            абсолютного нуля для температуры(-273.15 по кельвину).
    """
    from_unit, to_unit = from_unit.lower(), to_unit.lower()

    if (from_unit and to_unit) not in ('mm', 'cm', 'm', 'km', "mg", "g", "kg", "ton", "c", "f", "k"): # проверка на то, что единцы верны
        raise unknown_unit_error

    meters = {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000} #по словарю можно будет понять отношение единцы относительно базовой величины
    kilos = {"mg": 0.001, "g": 1, "kg": 1000, "ton": 1000000}
    temperature_zero = {"c": -273.15, "f": -459.67, "k": 0}
    #счет длины
    if from_unit in ('mm', 'cm', 'm', 'km'):
        if to_unit in ('mm', 'cm', 'm', 'km'):
            if from_unit == to_unit:
                return value
            return round((value * meters[from_unit]) / meters[to_unit], 5)
        else:
            raise incompatible_units_error
    # счет веса
    elif from_unit in ("mg", "g", "kg", "ton"):
        if to_unit in ("mg", "g", "kg", "ton"):
            if from_unit == to_unit:
                return value
            return round((value * kilos[from_unit]) / kilos[to_unit], 5)
        else:
            raise incompatible_units_error
    # счет температуры
    elif from_unit in {"c", "f", "k"}:
        if to_unit in {"c", "f", "k"}:
            # Проверка на то, что числа больше абсолютных нулей
            if temperature_zero[from_unit] >= value:
                raise below_absolute_zero_error
            if from_unit == to_unit:
                return value

            # Перевод в Цельсии
            if from_unit == "f":
                value = (value - 32) / 1.8
            elif from_unit == "k":
                value += 273.15

            # Перевод из Цельсия в целевые единицы
            if to_unit == "c":
                return round(value, 5)
            elif to_unit == "f":
                return round((value * 1.8) + 32, 5)
            elif to_unit == "k":
                return round(value + 273.15, 5)
        else:
            raise incompatible_units_error