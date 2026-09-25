def tokenize(expr):
    tokens = []
    state = 'start'
    current_token = ''

    can_be_unary = True
    def token_append():
        if state == 'fractional_number':
            return tokens.append(('number', float(current_token)))
        else:
            return tokens.append(('number', int(current_token)))

    for char in expr:
        if char.isspace():
            continue
        if state == 'start':
            if char.isdigit():
                state = 'number'
                current_token = char
                can_be_unary = False
            elif char in ['+', '-'] and can_be_unary:
                state = 'number'
                current_token = char
                can_be_unary = False
            elif char in ['+', '-', '*', '/', '^', '%', '//']:
                tokens.append(('operator', char))
                can_be_unary = True
            elif char == '(':
                tokens.append(('left_bracket', char))
                can_be_unary = True
            elif char == ')':
                tokens.append(('right_bracket', char))
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
            elif char == ')':
                token_append()
                tokens.append(('right_bracket', char))
                current_token = ''
                state = 'start'
                can_be_unary = False

        elif state == 'fractional_number':
            if char.isdigit():
                current_token += char
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


    if state in ('number', 'fractional_number') and current_token:
        token_append()

    return tokens


