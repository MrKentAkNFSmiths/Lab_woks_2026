import sys
import argparse

from .calculator import calculate
from .tokenizer import tokenize
from .converter import convert

def calculation_call(expression: str):
    expression = tokenize(expression)
    expression = calculate(expression)
    return expression


def convertation_call(values):
    convert_answer = convert(values)
    return convert_answer


def main():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="CLI calculator and converter of units",
        usage="""
  python -m toolkit calc "EXPRESSION"
  python -m toolkit convert VALUE --from UNIT --to UNIT
  python -m toolkit --help""",
        epilog="""
How to use:
---------------------------------------------------------
  calc:
    Выполняет математические вычисления. Математическое 
    выражение обязательно нужно оборачивать в кавычки, 
    чтобы терминал правильно распознал спецсимволы.
    Example: python -m toolkit calc "(2+3*5)/7"

  convert:
    Конвертирует единицы измерения. Требует передать 
    само число и два обязательных флага: --from и --to.
    Пример: python -m toolkit convert 1500 --from m --to km
---------------------------------------------------------""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    calc_parser = subparsers.add_parser("calc", help="Make calculation")
    calc_parser.add_argument(
        "expression",
        type=str,
        help="Mathematical expression, example: (2+3*5)/7"
    )

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

    # Если скрипт запущен без аргументов, принудительно выводим help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.command == "calc":
        try:
            result = calculation_call(args.expression)
            print(f"Calculation result{result}")
        except Exception as e:
            print(f"Ошибка вычисления: {e}", file=sys.stderr)
            sys.exit(1)


    elif args.command == "convert":
        try:

            result = convert(args.value, args.from_unit, args.to_unit)

            print(f"Convertation result: {result} {args.to_unit}")

        except ValueError as e:

            print(f"Ошибка конвертации: {e}", file=sys.stderr)

            sys.exit(1)


if __name__ == "__main__":
    main()

