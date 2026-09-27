from .errors import (
    below_absolute_zero_error,
    incompatible_units_error,
    unknown_unit_error,
)


def convert(value, from_un, to_un):
    from_part, to_part = [value,from_un], [to_un]
    from_part[1], to_part[0] = from_part[1].lower(), to_part[0].lower()
    if (from_part[1] and to_part[0]) not in ('mm', 'cm', 'm', 'km', "mg","g", "kg", "ton", "c","f","k"):
        raise unknown_unit_error
    meters = {"mm":0.001, "cm":0.01, "m": 1, "km":1000}
    kilos = {"mg": 0.001,"g":1, "kg":1000, "ton":1000000}
    temperature_zero = {"c":-273.15, "f":-459.67, "k":0}
    if from_part[1] in ('mm', 'cm', 'm', 'km'):
        if to_part[0] in ('mm', 'cm', 'm', 'km'):
            if from_part[1] == to_part[0]:
                return from_part[0]
            return round((from_part[0]*meters[from_part[1]])/meters[to_part[0]], 5)
        else:
            raise incompatible_units_error

    elif from_part[1] in ("mg","g", "kg", "ton"):
        if to_part[0] in ("mg","g", "kg", "ton"):
            if from_part[1] == to_part[0]:
                return from_part[0]
            return round((from_part[0] * kilos[from_part[1]]) / kilos[to_part[0]], 5)
        else:
            raise incompatible_units_error
    elif (from_part[1]) in {"c","f","k"}:
        if to_part[0] in {"c","f","k"}:
            """Проверка на то, что числа больше абсолютных нулей"""
            if temperature_zero[from_part[1]] >= from_part[0]:
                raise below_absolute_zero_error
            if from_part[1] == to_part[0]:
                return from_part[0]
            """В начале перевод в цельсии"""
            if from_part[1] == "f":
                from_part[0] = (from_part[0] - 32) /1.8
            elif from_part[1] == "k":
                from_part[0] += 273.15

            """Перевод из цельсий в нужные единицы"""
            if to_part[0] == "c":
                return round(from_part[0], 5)
            elif to_part[0] == "f":
                return round((from_part[0] * 1.8) + 32, 5)
            elif to_part[0] == "k":
                return round(from_part[0] + 273.15, 5)
        else:
            raise incompatible_units_error
