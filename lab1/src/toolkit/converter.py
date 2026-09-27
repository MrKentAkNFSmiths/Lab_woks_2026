def convert(value, from_un, to_un):
    from_part, to_part = [value,from_un], [to_un]
    from_part[1], to_part[0] = from_part[1].lower(), to_part[0].lower()
    meters = {"mm":0.001, "cm":0.01, "m": 1, "km":1000}
    kilos = {"mg": 0.001,"g":1, "kg":1000, "ton":1000000}
    temperature_zero = {"c":-273.15, "f":-459.67, "k":0}
    if (from_part[1]and to_part[0]) in ('mm', 'cm', 'm', 'km'):
        if from_part[1] == to_part[0]:
            return from_part[0]
        return round((from_part[0]*meters[from_part[1]])/meters[to_part[0]], 5)

    elif (from_part[1] and to_part[0]) in ("mg","g", "kg", "ton"):
        if from_part[1] == to_part[0]:
            return from_part[0]
        return round((from_part[0] * kilos[from_part[1]]) / kilos[to_part[0]], 5)

    elif (from_part[1] and to_part[0]) in {"c","f","k"}:
        """Проверка на то, что числа больше абсолютных нулей"""
        if temperature_zero[from_part[1]] > from_part[0]:
            return "koch"
            pass #Рейзить ошибку что так не можэ быти
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




# print(convert(100, "m", 'km'))

# val1 = [[1000,"MM"],["M"]]
# val2 = [[10,"M"], ['mm']]
# val3 = [[1,'Cm'],['m']]
# val4 = [[10000000, 'cm'],['Km']]
#
# val12 = [[1000, "g"],["kg"]]
# val22 = [[10, "g"], ['kg']]
# val32 = [[1, 'ton'],['kg']]
# val42 = [[1000000,'mg'],['kg']]
#
# val13 = [[0,"k"],["c"]]
# val23 = [[-270,"c"], ['k']]
# val33 = [[100,'c'],['f']]
# val43 = [[100,'f'],['c']]
# val53 = [[100,'f'],['k']]
# val63 = [[-1000,'f'],['k']]
# val73 = [[-1000,'c'],['k']]
# val83 = [[-1000,'k'],['k']]
#
#
#
# print(convert(val1))
# print(convert(val2))
# print(convert(val3))
# print(convert(val4))
# print("")
# print(convert(val12))
# print(convert(val22))
# print(convert(val32))
# print(convert(val42))
# print("")
# print(convert(val13))
# print(convert(val23))
# print(convert(val33))
# print(convert(val43))
# print(convert(val53))
# print(convert(val63))
# print(convert(val73))
# print(convert(val83))