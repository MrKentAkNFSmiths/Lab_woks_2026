# from tokenizer import tokenize
from .errors import (
    consecutive_operators_error,
    division_by_zero_error,
    empty_expression_error,
    missing_operand_error,
)


def validate(tokens: list[tuple[str, str | int | float]]) -> list[tuple[str, str | int | float]]:
    """Преобразует список токенов обычного выражения в обратную польскую нотацию (ОПН) и проверяет синтаксис.

    Функция реализует алгоритм сортировочной станции для построения ОПН, а так же проверяет правильность самого выражения.

    Args:
        tokens (list[tuple[str, str | int | float]]): Список входных токенов вида (token_type, token_value).

    Returns:
        list[tuple[str, str | int | float]]: Выходная очередь токенов в формате ОПН.

    Raises:
        empty_expression_error: Если передан пустой список токенов.
        missing_operand_error: Если пропущен операнд, либо скобки не сбалансированы.
        consecutive_operators_error: Если два бинарных оператора следуют подряд.
    """
    if not tokens: #Проверка на наличие выражения
        raise empty_expression_error()

    priorities = {'+': 1, '-': 1, '*': 2, '/': 2, '//': 2, "%": 2, '^': 3}# словарь приоритетов операторов
    operators_stack = []
    output_queue = []
    prev_type = None # Запись предыдущего оператора, для проверки с нынешним
    #Идем по алгоритму shuning_yard
    for i, (token_type, token_value) in enumerate(tokens):
        if token_type == "number":
            output_queue.append((token_type, token_value))

        elif token_type == "left_bracket":
            operators_stack.append((token_type, token_value))

        elif token_type == "right_bracket":
            if prev_type == "operator":
                raise missing_operand_error("Missing operand before closing bracket")

            found_left_bracket = False
            while operators_stack:
                top_type, top_val = operators_stack.pop()
                if top_type == "left_bracket":
                    found_left_bracket = True
                    break
                output_queue.append((top_type, top_val))

            if not found_left_bracket:
                raise missing_operand_error("Extra or unbalanced closing bracket")

        elif token_type == "operator":
            if i == 0 or i == len(tokens) - 1:
                raise missing_operand_error(f"Missing operand for operator  '{token_value}'")
            if prev_type == "operator":
                raise consecutive_operators_error("Two binary operators in a row")

            if prev_type == "left_bracket":
                raise missing_operand_error(f"Missing operand before operator '{token_value}'")

            while (operators_stack and
                   operators_stack[-1][0] == "operator" and
                   priorities.get(operators_stack[-1][1], 0) >= priorities.get(token_value, 0)):
                output_queue.append(operators_stack.pop())

            operators_stack.append((token_type, token_value))

        prev_type = token_type

    while operators_stack:
        top_type, top_val = operators_stack.pop()
        if top_type == "left_bracket":
            raise missing_operand_error("Opening bracket is not closed")
        output_queue.append((top_type, top_val))

    return output_queue


def calculate(input_queue: list[tuple[str, str | int | float]]) -> int | float:
    """Вычисляет значение математического выражения, представленного в ОПН.

    Вычисление выполняется с помощью стека и дальнейшей его обработки, то есть операнд -> действие над числами этим операндом


    Args:
        input_queue (list[tuple[str, str | int | float]]): Очередь токенов в формате ОПН.

    Returns:
        int | float: Числовой результат вычисления выражения.

    Raises:
        division_by_zero_error: При попытке деления, целочисленного деления или взятия остатка на ноль.
    """
    stack = []
    for token_type, token_value in input_queue:
        if token_type == "number":
            stack.append(token_value)
        elif token_type == "operator":
            second_number = stack.pop()
            first_number = stack.pop()
            if token_value in ("/", "//", "%") and second_number == 0:
                raise division_by_zero_error("Zero division")
            if token_value == "+":
                stack.append(first_number + second_number)
            elif token_value == "-":
                stack.append(first_number - second_number)
            elif token_value == "*":
                stack.append(first_number * second_number)
            elif token_value == "/":
                stack.append(first_number / second_number)
            elif token_value == "//":
                stack.append(first_number // second_number)
            elif token_value == "%":
                stack.append(first_number % second_number)
            elif token_value == "^":
                stack.append(first_number ^ second_number)
    return stack[0]