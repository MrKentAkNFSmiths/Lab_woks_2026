import sys
import argparse

from calculator import calculate, reverse_polish_notation
from tokenizer import tokenize
from converter import convert
# Импортируй свои готовые функции сюда
# from .calculator import calculate
# from .converter import convert_units

def mock_calculate(expression: str):
    expression = tokenize(expression)
    expression = reverse_polish_notation(expression)
    expression = calculate(expression)
    return f"Результат вычисления '{expression}'"


def mock_convert(values):
    convert_answer = convert(values)

    return f"Конвертация: {convert_answer}"


def main():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="CLI calculator and converter of units"
    )

    # Создаем парсер для подкоманд
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")

    # --- Подкоманда: calc ---
    calc_parser = subparsers.add_parser("calc", help="Make calculation")
    calc_parser.add_argument(
        "expression",
        type=str,
        help="Mathematical expression, example: (2+3*5)%7"
    )

    # --- Подкоманда: convert ---
    convert_parser = subparsers.add_parser("convert", help="Convert units")
    convert_parser.add_argument(
        "values",
        type=list,
        help="type VALUE and units FROM and TO which convertion will be made"
    )
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Исходная единица измерения"
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Целевая единица измерения"
    )

    # Если скрипт запущен без аргументов, принудительно выводим help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Маршрутизация и вывод
    if args.command == "calc":
        try:
            result = mock_calculate(args.expression)
            print(result)
        except Exception as e:
            print(f"Ошибка вычисления: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "convert":
        try:
            result = mock_convert(args.values, args.from_unit, args.to_unit)
            print(result)
        except Exception as e:
            print(f"Ошибка конвертации: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()