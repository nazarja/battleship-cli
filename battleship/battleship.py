from __future__ import annotations
import typings


class BattleShip:
    """ the battleship board and logic """
    def __init__(self, height: int, width: int, ships: int):
        self.height: int = height
        self.width: int = width
        self.ships: int = ships
