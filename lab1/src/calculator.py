from tokenizer import tokenize

def validate(tokens):
    priorities = {'+': 1, '-': 1, '*': 2, '/': 2, '//':2, "%":2}
    operators_stack = []
    output_queue = []
    for token_type, token_value in tokens:
        if token_type == "number":
            output_queue.append((token_type, token_value))

        elif token_type == "left_bracket":
            operators_stack.append((token_type, token_value))

        elif token_type == "right_bracket":
            while operators_stack and operators_stack[-1][0] != "left_bracket":
                output_queue.append(operators_stack.pop())
            operators_stack.pop()


        elif token_type == "operator":
            while (operators_stack and
                   operators_stack[-1][0] == "operator" and
                   priorities[operators_stack[-1][1]] >= priorities[token_value]):
                output_queue.append(operators_stack.pop())


            operators_stack.append((token_type, token_value))

    while operators_stack:
        output_queue.append(operators_stack.pop())

    return output_queue

def calculate(input_queue : list):
    stack = []
    for token_type, token_value in input_queue:
        if token_type == "number":
            stack.append(token_value)
        elif token_type == "operator":
            second_number = stack.pop()
            first_number = stack.pop()
            if token_value == "+":
                stack.append(first_number+second_number)
            if token_value == "-":
                stack.append(first_number-second_number)
            if token_value == "*":
                stack.append(first_number*second_number)
            if token_value == "/":
                stack.append(first_number/second_number)
            if token_value == "//":
                stack.append(first_number//second_number)
            if token_value == "%":
                stack.append(first_number%second_number)
    return stack[0]

a = input()
tokens = tokenize(a)
print(tokens)
b = validate(tokens)
print(b)
print(calculate(b))








