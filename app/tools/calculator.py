"""Evaluate arithmetic without executing arbitrary Python."""

import ast
import operator

# Map syntax-tree operator nodes to the functions that implement them.
_ALLOWED = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_calculate(expression: str):
    """Evaluate a basic arithmetic expression supplied by the model.

    The string is parsed into a syntax tree and walked by hand. Names, calls,
    and attribute access are rejected. Exponents and huge results are capped.
    """
    tree = ast.parse(expression, mode="eval")

    def visit(node):
        """Return the numeric value of one allowed syntax node."""
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
            left = visit(node.left)
            right = visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent too large")
            return _ALLOWED[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
            return _ALLOWED[type(node.op)](visit(node.operand))
        raise ValueError("Only basic arithmetic is allowed")

    result = visit(tree)
    if abs(result) > 1e100:
        raise ValueError("Result too large")
    return result
