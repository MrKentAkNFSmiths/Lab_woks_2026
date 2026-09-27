# from tokenizer import tokenize
from .errors import (
    consecutive_operators_error,
    division_by_zero_error,
    empty_expression_error,
    missing_operand_error,
)


def validate(tokens):
    if not tokens:
        raise empty_expression_error()


    priorities = {'+': 1, '-': 1, '*': 2, '/': 2, '//': 2, "%": 2}
    operators_stack = []
    output_queue = []
    prev_type = None

    for i, (token_type, token_value) in enumerate(tokens):
        if token_type == "number":
            output_queue.append((token_type, token_value))


        elif token_type == "left_bracket":
            operators_stack.append((token_type, token_value))

        elif token_type == "right_bracket":
            # Нельзя закрывать скобку сразу после оператора: (2 + )
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
            # Оператор не может находиться на первом или последнем месте
            if i == 0 or i == len(tokens) - 1:
                raise missing_operand_error(f"Missing operand for operator  '{token_value}'")

            # Два бинарных оператора подряд
            if prev_type == "operator":
                raise consecutive_operators_error("Two binary operators in a row")

            # Оператор идет сразу после открывающей скобки: ( + 2)
            if prev_type == "left_bracket":
                raise missing_operand_error(f"Missing operand before operator '{token_value}'")

            while (operators_stack and
                   operators_stack[-1][0] == "operator" and
                   priorities[operators_stack[-1][1]] >= priorities[token_value]):
                output_queue.append(operators_stack.pop())

            operators_stack.append((token_type, token_value))

        prev_type = token_type

    # Опустошаем стек и проверяем, не остались ли незакрытые скобки
    while operators_stack:
        top_type, top_val = operators_stack.pop()
        if top_type == "left_bracket":
            raise missing_operand_error("Opening bracket is not closed")
        output_queue.append((top_type, top_val))

    return output_queue

def calculate(input_queue):
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
            if token_value == "-":
                stack.append(first_number - second_number)
            if token_value == "*":
                stack.append(first_number * second_number)
            if token_value == "/":
                stack.append(first_number / second_number)
            if token_value == "//":
                stack.append(first_number // second_number)
            if token_value == "%":
                stack.append(first_number % second_number)
            if token_value == "^":
               stack.append(first_number ^ second_number)
    return stack[0]









