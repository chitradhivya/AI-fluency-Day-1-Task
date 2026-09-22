"""Tools available to the AI agent."""

import ast
import operator

from config import VEHICLES


def get_vehicle_service_record(vehicle_code: str) -> str:
    """Look up the service record for one vehicle."""

    code = vehicle_code.strip().upper()

    vehicle = VEHICLES.get(code)

    if vehicle is None:
        return f"Unknown vehicle code: {vehicle_code}"

    return str(vehicle)


# Safe calculator.
# Only numbers and + - * / are allowed.
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(
        node.value, (int, float)
    ):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.operand)
        )

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression."""

    try:
        result = _evaluate(
            ast.parse(expression, mode="eval").body
        )

        return str(result)

    except Exception as error:
        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {
    "get_vehicle_service_record": get_vehicle_service_record,
    "calculator": calculator,
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_vehicle_service_record",
            "description": (
                "Get the private service record for one vehicle. "
                "Use a vehicle code such as CAR101."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "vehicle_code": {
                        "type": "string"
                    }
                },
                "required": ["vehicle_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Evaluate a basic arithmetic expression "
                "using +, -, *, / and brackets."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


if __name__ == "__main__":
    print(
        "get_vehicle_service_record('CAR101') ->",
        get_vehicle_service_record("CAR101")
    )

    print(
        "calculator('8500 + 6200') ->",
        calculator("8500 + 6200")
    )

    print(
        "calculator('9100 - 6200') ->",
        calculator("9100 - 6200")
    )