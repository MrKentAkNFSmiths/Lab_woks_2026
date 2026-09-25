def convert(values):
    f, s = values
    f[0], s[0] = f[0].lower(), s[0].lower()
    meters = {"mm":0.001, "cm":0.01, "m": 1, "km":1000}
    kilos = {"mg": 0.001,"g":1, "kg":1000, "ton":1000000}
    temperature_zero = {"c":-273.15, "f":-459.67, "k":0}
    if (f[0]and s[0]) in ('mm', 'cm', 'm', 'km'):
        if f[0] == s[0]:
            return f[1]
        return round((f[1]*meters[f[0]])/meters[s[0]], 5)

    elif (f[0] and s[0]) in ("mg","g", "kg", "ton"):
        if f[0] == s[0]:
            return f[1]
        return round((f[1] * kilos[f[0]]) / kilos[s[0]], 5)

    elif (f[0] and s[0]) in {"c","f","k"}:
        """Проверка на то, что числа больше абсолютных нулей"""
        if temperature_zero[f[0]] > f[1]:
            return "koch"
            pass #Рейзить ошибку что так не можэ быти
        if f[0] == s[0]:
            return f[1]
        """В начале перевод в цельсии"""
        if f[0] == "f":
            f[1] = (f[1] - 32) /1.8
        elif f[0] == "k":
            f[1] += 273.15

        """Перевод из цельсий в нужные единицы"""
        if s[0] == "c":
            return round(f[1], 5)
        elif s[0] == "f":
            return round((f[1] * 1.8) + 32, 5)
        elif s[0] == "k":
            return round(f[1] + 273.15, 5)




#
# val1 = [["MM",1000],["M"]]
# val2 = [["M", 10], ['mm']]
# val3 = [['Cm', 1],['m']]
# val4 = [['cm', 100000],['Km']]
#
# val12 = [["g",1000],["kg"]]
# val22 = [["g", 10], ['kg']]
# val32 = [['ton', 1],['kg']]
# val42 = [['mg', 1000000],['kg']]
#
# val13 = [["k",0],["c"]]
# val23 = [["c", -270], ['k']]
# val33 = [['c', 100],['f']]
# val43 = [['f', 100],['c']]
# val53 = [['f', 100],['k']]
# val63 = [['f', -1000],['k']]
# val73 = [['c', -1000],['k']]
# val83 = [['k', -1000],['k']]
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