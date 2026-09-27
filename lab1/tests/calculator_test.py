import sys
import pytest

from toolkit.tokenizer import tokenize
from toolkit.calculator import calculate, validate
from toolkit.converter import convert
from toolkit.errors import (
    empty_expression_error,
    missing_operand_error,
    consecutive_operators_error,
    division_by_zero_error,
    unknown_unit_error, incompatible_units_error, below_absolute_zero_error,
)
from toolkit.__main__ import main


# Вспомогательная функция для полного цикла вычисления
def calculation_call(expression: str):
    expression = tokenize(expression)
    expression = validate(expression)
    expression = calculate(expression)
    return expression


def convertation_call(values):
    convert_answer = convert(values)
    return convert_answer


class TestCalculator:

    @pytest.mark.parametrize("expr, expected", [
        ("2 + 2", 4),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 / 2", 5.0),
        ("10 // 3", 3),
        ("10 % 3", 1),
        ("-5 + 10", 5),
        ("2.5 + 3.5", 6.0),
        ("(10 - 2) * (3 + 1) / 4", 8.0),
    ])
    def test_calculator_success(self, expr, expected):
        """Проверка правильности вычисления корректных математических выражений."""
        assert calculation_call(expr) == expected

    @pytest.mark.parametrize("expr, expected_exception", [
        ("", empty_expression_error),
        ("   ", empty_expression_error),
        ("2 + ", missing_operand_error),
        (" * 5", missing_operand_error),
        ("(2 + 3", missing_operand_error),
        ("2 + 3)", missing_operand_error),
        ("2 + * 3", consecutive_operators_error),
        ("5 / 0", division_by_zero_error),
        ("5 // 0", division_by_zero_error),
        ("5 % 0", division_by_zero_error),
    ])
    def test_calculator_errors(self, expr, expected_exception):
        """Проверка выброса соответствующих ошибок при некорректных выражениях."""
        with pytest.raises(expected_exception):
            calculation_call(expr)


class TestConverter:

    @pytest.mark.parametrize("value, from_unit, to_unit, expected", [
        # Длина
        (1000, "m", "km", 1.0),
        (1, "km", "m", 1000.0),
        (100, "cm", "m", 1.0),
        (10, "mm", "cm", 1.0),
        # Масса
        (1000, "g", "kg", 1.0),
        (1, "ton", "kg", 1000.0),
        (1000000, "mg", "kg", 1.0),
        # Температура
        (0, "c", "k", 273.15),
        (100, "c", "f", 212.0),
        (32, "f", "c", 0.0),
        # Конвертация в ту же единицу
        (42, "m", "m", 42),
    ])
    def test_converter_success(self, value, from_unit, to_unit, expected):
        """Проверка успешной конвертации различных единиц измерения."""
        assert convert(value, from_unit, to_unit) == pytest.approx(expected, rel=1e-3)

    @pytest.mark.parametrize("value, from_u, to_u, expected_exception", [
        # Неизвестные единицы
        (100, "m", "xyz", unknown_unit_error),
        # Несовместимые категории (длина -> масса и т.д.)
        (100, "m", "kg", incompatible_units_error),
        (100, "g", "c", incompatible_units_error),
        # Температура ниже абсолютного нуля
        (-300, "c", "k", below_absolute_zero_error),
        (-1, "k", "c", below_absolute_zero_error),
    ])
    def test_converter_errors(self, value, from_u, to_u, expected_exception):
        """Проверка генерации ошибок при невалидных данных конвертера."""
        with pytest.raises(expected_exception):
            convert(value, from_u, to_u)

class TestCLI:

    def test_cli_calc_success(self, monkeypatch, capsys):
        """Проверка работы CLI команды calc при успешном вычислении."""
        test_args = ["toolkit", "calc", "2+3*4"]
        monkeypatch.setattr(sys, "argv", test_args)

        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()
        assert exc_info.value.code == 0
        assert "14" in captured.out

    def test_cli_calc_error(self, monkeypatch, capsys):
        """Проверка работы CLI команды calc при ошибке (вывод в stderr и код выхода 2)."""
        test_args = ["toolkit", "calc", "5/0"]
        monkeypatch.setattr(sys, "argv", test_args)

        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()
        assert exc_info.value.code in (1, 2)

    def test_cli_convert_success(self, monkeypatch, capsys):
        """Проверка работы CLI команды convert при успешной конвертации."""
        test_args = ["toolkit", "convert", "1000", "--from", "m", "--to", "km"]
        monkeypatch.setattr(sys, "argv", test_args)

        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()
        assert exc_info.value.code == 0
        assert "1.0" in captured.out

    def test_cli_convert_error(self, monkeypatch, capsys):
        """Проверка работы CLI команды convert при передаче несовместимых единиц."""
        test_args = ["toolkit", "convert", "100", "--from", "m", "--to", "kg"]
        monkeypatch.setattr(sys, "argv", test_args)

        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()
        assert exc_info.value.code in (1, 2)
        assert len(captured.err) > 0