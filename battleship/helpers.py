from __future__ import annotations
import typing


def isNotNumber(input: str) -> bool:
    """ checks if input string contains any non digit characters """
    return any(c.isdigit() for c in input)