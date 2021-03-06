from __future__ import annotations
import os
import time
import sys
from typing import List


class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    YELLOW = '\u001b[33m'
    RED = '\033[91m'
    BLACK = '\u001b[30m'
    ENDC = '\033[0m'


def isNotNumber(input: str) -> bool:
    return any(not c.isdigit() for c in input)


def get_score_as_int(x: List[str]) -> int:
    return int(x[3])


def heading(text: str) -> str:
    os.system('clear')
    return (
        '=' * 80 +
        f'\n    {Colors.YELLOW}BATTLESHIP{Colors.ENDC}' +
        (f' - Welcome, {text.capitalize()} \n' if text else '\n') +
        '=' * 80 + '\n'
    )


def output_message(message: str, times: int) -> None:
    sys.stdout.write("\033[F")
    print(f'{message}')
    time.sleep(2)
    sys.stdout.write("\033[F\033[K" * times)


def input_error(message: str, times: int) -> None:
    output_message(message, times)


def input_message(message: str, times: int) -> None:
    output_message(message, times)


def quit_text() -> str:
    return '- Enter \'quit\' to return to the menu. \n'
