import argparse
import sys

from toolkit.errors import validation_error

from .calculator import calculate, validate
from .converter import convert
from .tokenizer import tokenize


def calculation_call(expression: str):
    expression = tokenize(expression)
    expression = validate(expression)
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

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

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

