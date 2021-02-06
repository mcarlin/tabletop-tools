import json
from typing import Any, Dict
from decimal import Decimal


def to_unix(text: str) -> str:
    return text.replace("\r\n", "\n")


def _quantize(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.0001"))


def _encode_decimal(obj):
    if isinstance(obj, Decimal):
        return float(_quantize(obj))
    raise TypeError(
        f"xxxObject of type {obj.__class__.__name__} " f"is not JSON serializable"
    )


def format_json(value: Dict[Any, Any]) -> str:
    return (
        json.dumps(
            value,
            indent=2,
            separators=(",", ": "),
            ensure_ascii=False,
            default=_encode_decimal,
        )
        + "\n"
    )


def _decode_decimal(val: str) -> Decimal:
    dec = _quantize(Decimal(val))
    if dec.is_zero():
        return Decimal(0.0)
    return dec


def parse_json(value: str) -> Dict[Any, Any]:
    return json.loads(value, parse_float=_decode_decimal)
