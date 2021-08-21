from __future__ import annotations
from .leaderboard import Leaderboard
from .helpers import heading
from typing import Dict, List
from random import choice


class Battleship:
    def __init__(self, board: Dict[str, List[int]], leaderboard: Leaderboard):
        self.leaderboard: Leaderboard = leaderboard
        self.height: int = board["height"][2]
        self.width: int = board["width"][2]
        self.ships: int = board["ships"][2]
        self.user_board: List[List[str]] = []
        self.hits_board: List[List[str]] = []
        self.cpu_board: List[List[str]] = []
        self.create_boards()
        self.create_ships(self.user_board)
        self.print_boards()

    def create_boards(self) -> None:
        for y in range(self.height):
            self.user_board.append(['.' for x in range(self.width)])
            self.hits_board.append(['.' for x in range(self.width)])
            self.cpu_board.append(['.' for x in range(self.width)])


    def print_boards(self) -> None:
        print(heading(self.leaderboard.username))
        
        print(
            ' ' * self.width, 'Your Board',
            ' ' * (self.width * 3), 'CPU Board', '\n'
        )

        print(
            ' ' * 3, ''.join(f'{str(x):3s}' for x in range(self.width)),
            ' ' * 5,
            ' ' * 3, ''.join(f'{str(x):3s}' for x in range(self.width)),
        )

        for i, row in enumerate(zip(self.user_board, self.hits_board)):
            print(
                f'{str(i):3s}', ''.join(f'{y:3s}' for y in row[0]),
                ' ' * 5,
                f'{str(i):3s}', ''.join(f'{y:3s}' for y in row[1]),
            )

        print('\n')

    def create_ships(self, board: List[List[str]]) -> None:
        submarine: str = 'S' * 2
        destroyer: str = 'D' * 3
        cruiser: str = 'C' * 3
        battleship: str = 'B' * 4
        carrier: str = 'A' * 5
        ships: List[str] = [submarine, destroyer, cruiser, battleship, carrier]

        for i in range(self.ships):
            collision: bool = True
            ship = choice(ships)

            while collision:
                collision = True
                x = choice([i for i in range(self.width)])
                y = choice([i for i in range(self.height)])
                
                if choice([True, False]):
                    if x + len(ship) > self.width:
                        x = self.width - len(ship)
                    
                    for a in range(len(ship)):
                        if board[x+a][y] != '.':
                            continue

                    for j in range(len(ship)):
                        board[x+j][y] = ship[j]
                else:
                    if y + len(ship) > self.height:
                        y = self.height - len(ship)

                    for b in range(len(ship)):
                        if board[x][y+b] != '.':
                            continue

                    for k in range(len(ship)):
                        board[x][y+k] = ship[k]
                
                collision = False




class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
