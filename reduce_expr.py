from typing import List, Optional, Tuple


def reduce_expression_step(expr: List[str]) -> List[str]:
    def evaluate_simple_expression(tokens: List[str]) -> List[str]:
        for i in range(len(tokens)):
            if tokens[i] in ("*", "/"):
                left = float(tokens[i - 1])
                right = float(tokens[i + 1])
                result = left * right if tokens[i] == "*" else left / right
                return tokens[: i - 1] + [str(result)] + tokens[i + 2 :]

        for i in range(len(tokens)):
            if tokens[i] in ("+", "-"):
                left = float(tokens[i - 1])
                right = float(tokens[i + 1])
                result = left + right if tokens[i] == "+" else left - right
                return (
                    tokens[: i - 1]
                    + [str(int(result)) if result.is_integer() else str(result)]
                    + tokens[i + 2 :]
                )
        return tokens

    def find_innermost_parentheses(tokens: List[str]) -> Optional[Tuple[int, int]]:
        stack = []
        for i, token in enumerate(tokens):
            if token == "(":
                stack.append(i)
            elif token == ")":
                start = stack.pop()
                return start, i
        return None

    expr = clean_unnecessary_parentheses(expr)

    paren_indices = find_innermost_parentheses(expr)
    if paren_indices:
        start, end = paren_indices
        inside_expr = expr[start + 1 : end]
        reduced_inside = evaluate_simple_expression(inside_expr)
        expr = expr[: start + 1] + reduced_inside + expr[end:]
        expr = clean_unnecessary_parentheses(expr)
        return expr

    expr = evaluate_simple_expression(expr)
    expr = clean_unnecessary_parentheses(expr)

    return expr


def clean_unnecessary_parentheses(tokens: List[str]) -> List[str]:
    stack = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "(":
            stack.append(i)
        elif tokens[i] == ")":
            start = stack.pop()
            if start + 2 == i:
                tokens = tokens[:start] + tokens[start + 1 : i] + tokens[i + 1 :]
                i -= 2
        i += 1
    return tokens
