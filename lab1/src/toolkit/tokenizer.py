from .errors import consecutive_operators_error, invalid_character_error


def tokenize(expr: str) -> list[tuple[str, str | int | float]]:
    """Преобразует строку с математическим выражением в список структурированных токенов.

    Функция выполняет посимвольный разбор строки с использованием конечного автомата,
    распознает целые и дробные числа, унарные и бинарные операторы, а также скобки.

    Args:
        expr (str): Строка с математическим выражением (например, "(2 + 3.5) * -7").

    Returns:
        list[tuple[str, str | int | float]]: Список токенов вида (token_type, token_value).
            Возможные типы токенов:
            - 'number': числовое значение (int или float)
            - 'operator': бинарный или унарный оператор ('+', '-', '*', '/', '//', '%', '^')
            - 'left_bracket': открывающая скобка '('
            - 'right_bracket': закрывающая скобка ')'

    Raises:
        invalid_character_error: Если выражение содержит запрещенные символы или точки в неверном формате.
        consecutive_operators_error: Если два бинарных оператора идут подряд без операнда.
    """
    expr = expr.replace('//', '\0')
    tokens = []
    state = 'start'
    current_token = ''
    can_be_unary = True
    prev_type = None

    def token_append():
        """Вспомогательная функция для сохранения числа из накопителя current_token в список токенов."""
        if current_token.endswith('.'): # число не может заканчиваться точкой
            raise invalid_character_error("Decimal point must be followed by digits")

        if state == 'fractional_number':
            return tokens.append(('number', float(current_token)))
        else:
            return tokens.append(('number', int(current_token)))

    for char in expr:

        if char == '\0':
            char = '//'
        if char.isspace():
            continue
        if (char.isdigit() == 0) and (char not in ('+', '-', '*', '/', '^', '%', '//', '(', ')', '.', ' ')):
            raise invalid_character_error("Invalid character")

        if state == 'start':
            if char.isdigit() or char in ['+', '-'] and can_be_unary:
                state = 'number'
                current_token = char
                can_be_unary = False
            elif char == '.':
                raise invalid_character_error("Standalone or leading decimal point is not allowed")
            elif char in ['+', '-', '*', '/', '^', '%', '//']:
                if prev_type == "operator":
                    raise consecutive_operators_error("Two binary operators in a row")
                tokens.append(('operator', char))
                prev_type = 'operator'
                can_be_unary = True
            elif char == '(':
                tokens.append(('left_bracket', char))
                can_be_unary = True
                prev_type = 'left_bracket'
            elif char == ')':
                tokens.append(('right_bracket', char))
                prev_type = 'right_bracket'
                can_be_unary = False

        elif state == 'number':
            if char.isdigit():
                current_token += char
            elif char == '.':
                state = 'fractional_number'
                current_token += char
            elif char in ['+', '-', '*', '/', '^', '%', '//']:
                token_append()
                tokens.append(('operator', char))
                current_token = ''
                state = 'start'
                can_be_unary = True
                prev_type = 'operator'
            elif char == ')':
                token_append()
                tokens.append(('right_bracket', char))
                current_token = ''
                state = 'start'
                can_be_unary = False
                prev_type = 'right_bracket'

        elif state == 'fractional_number':
            if char.isdigit():
                current_token += char
            elif char == '.': # Проверка на вторую точку в дробном числе
                raise invalid_character_error("Multiple decimal points in number")
            elif char in ['+', '-', '*', '/', '^', '%', '//']:
                token_append()
                tokens.append(('operator', char))
                current_token = ''
                state = 'start'
                can_be_unary = True
            elif char == ')':
                token_append()
                tokens.append(('right_bracket', char))
                current_token = ''
                state = 'start'
                can_be_unary = False
            prev_type = 'number'

    if state in ('number', 'fractional_number') and current_token:
        token_append()
        prev_type = 'number'
    return tokens