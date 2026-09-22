def validate(tokens):
    priorities = {'+': 1, '-': 1, '*': 2, '/': 2, '//':2, "%":2}
    operators_stack = []
    output_queue = []
    for token_type, token_value in tokens:
        if token_type == "NUMBER":
            output_queue.append((token_type, token_value))

        # Открывающую скобку всегда помещаем в стек операторов
        elif token_type == "LPAREN":
            operators_stack.append((token_type, token_value))

        # При встрече закрывающей скобки переносим операторы из стека в очередь до открывающей скобки
        elif token_type == "RPAREN":
            # Выталкиваем операторы, пока не упремся в открывающую скобку
            while operators_stack and operators_stack[-1][0] != "LPAREN":
                output_queue.append(operators_stack.pop())

            # Удаляем открывающую скобку из стека (в итоговое выражение скобки не попадают)
            operators_stack.pop()

        # Обработка бинарных операторов
        elif token_type == "OPERATOR":
            # Выталкиваем из стека операторы с бóльшим или равным приоритетом
            while (operators_stack and
                   operators_stack[-1][0] == "OPERATOR" and
                   priorities[operators_stack[-1][1]] >= priorities[token_value]):
                output_queue.append(operators_stack.pop())

            # Помещаем текущий оператор в стек
            operators_stack.append((token_type, token_value))

    # Переносим все оставшиеся в стеке операторы в выходную очередь
    while operators_stack:
        output_queue.append(operators_stack.pop())

    return output_queue


# --- Пример проверки ---
# Входной поток токенов для выражения: 3 + 4 * ( 2 - 1 )
input_tokens = [
    ("NUMBER", "3"),
    ("OPERATOR", "+"),
    ("NUMBER", "4"),
    ("OPERATOR", "*"),
    ("LPAREN", "("),
    ("NUMBER", "2"),
    ("OPERATOR", "-"),
    ("NUMBER", "1"),
    ("RPAREN", ")"),
]

result = validate(input_tokens)

print("Входные токены:")
print(input_tokens)
print("\nПостфиксный список токенов:")
print(result)