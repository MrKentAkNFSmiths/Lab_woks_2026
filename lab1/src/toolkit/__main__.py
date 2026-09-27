import argparse
import sys

from .calculator import calculate, validate
from .converter import convert
from .errors import validation_error  # Относительный импорт для работы модуля в пакете
from .tokenizer import tokenize


def calculation_call(expression: str):
    """Вспомогательная функция, соединяющая токенизацию, валидацию и калькуляцию.

    Сначала делает токенизацию, далее валидацию, и после этого вычисляет выражение.

    Args:
        expression (str): Математическое выражение в виде строки.

    Returns:
        int | float: Числовой результат вычисления.
    """
    expression = tokenize(expression)  # Разбиваем строку на токены (числа, операторы, скобки)
    expression = validate(expression)  # Проверяем синтаксис и переводим в ОПН (Shunting-yard)
    expression = calculate(expression)  # Вычисляем итоговое значение по ОПН
    return expression


def convertation_call(values):
    """Вспомогательная функция для конвертации единиц измерения.

    Args:
        values: Параметры для преобразования величин.

    Returns:
        float | int: Преобразованное значение.
    """
    return convert(values)


def main():
    """Главная точка входа CLI-приложения toolkit.

    Настраивает парсер аргументов командной строки для подкоманд 'calc' и 'convert',
    а так же находит ошибки, и заканчивает программу при помощи кодов(0/1/2).
    """
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="CLI calculator and converter of units",
        usage="""
  python3 -m toolkit calc "EXPRESSION"
  python3 -m toolkit convert VALUE --from UNIT --to UNIT
  python3 -m toolkit --help""",
        epilog="""
How to use:
---------------------------------------------------------
  calc:
    Performs math calculations. The math expression must be wrapped in quotes
    so the terminal correctly recognizes special characters.
    Example: python3 -m toolkit calc "(2+3*5)/7"

  convert:
    Converts units of measurement. Requires passing
    the number itself and two required flags: --from and --to.
    Example: python3 -m toolkit convert 1500 --from m --to km
---------------------------------------------------------""",

        formatter_class=argparse.RawTextHelpFormatter
    )

    #Помогает в дальнейшем разделять функцию калькулятора и конвертера
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Параметры для подкоманды 'calc'
    calc_parser = subparsers.add_parser("calc", help="Make calculation")
    calc_parser.add_argument(
        "expression",
        type=str,
        help="Mathematical expression, example: (2+3*5)/7"
    )

    # Параметры для подкоманды 'convert'
    convert_parser = subparsers.add_parser("convert", help="Convert units")
    convert_parser.add_argument(
        "value",
        type=float,
        help="Type VALUE which you want to convert"
    )
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Type UNIT from which you want to convert"
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Type UNIT to which you want to convert"
    )

    # Если нет аргументов, то открываем окно помощи(help)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)  # Завершение с кодом 1, т.к. это справка без параметров

    args = parser.parse_args()

    # Выполнение подкоманды 'calc'
    if args.command == "calc":
        try:
            result = calculation_call(args.expression)
            print(f"Calculation result: {result}")
        except validation_error as e:

            print(f"Calculation error: {e}", file=sys.stderr)
            sys.exit(2)
        sys.exit(0)


    elif args.command == "convert":
        try:
            result = convert(args.value, args.from_unit, args.to_unit)
            print(f"Convertation result: {result} {args.to_unit}")
        except validation_error as e:
            print(f"Convertation error: {e}", file=sys.stderr)
            sys.exit(2)
        sys.exit(0)


if __name__ == "__main__":
    main()