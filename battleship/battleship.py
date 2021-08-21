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
        self.num_ships: int = board["ships"][2]
        self.user_board: List[List[str]] = []
        self.hits_board: List[List[str]] = []
        self.cpu_board: List[List[str]] = []

        self.ships: Dict[str, List[str]] = {
            "names": ['Submarine', 'Destroyer', 'Crusier', 'Battleship', 'Aircraft Carrier'][:self.num_ships],
            "codes": ['A', 'B', 'C', 'D', 'S'],
            "chars": ['S' * 2, 'D' * 3, 'C' * 3, 'B' * 4, 'A' * 5][:self.num_ships],
            "length": ['2', '3', '3', '4', '5'][:self.num_ships]
        }

        self.start()


    def start(self) -> None:
        self.create_boards()
        self.create_user_board(self.user_board)
        self.create_cpu_board(self.cpu_board)

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
                f'{str(i):3s}', ''.join(f'{self.colorize_char(y):3s}' for y in row[0]),
                ' ' * 5,
                f'{str(i):3s}', ''.join(f'{self.colorize_char(y):3s}' for y in row[1]),
            )

        print('\n')

    def colorize_char(self, c: str) -> str:
        if c in self.ships['codes']:
            return Colors.GREEN + c + ' ' * 2 + Colors.ENDC
        return c

    def create_user_board(self, board: List[List[str]]) -> None:
        print(heading(self.leaderboard.username))

        print(f'Place your {self.num_ships} ships')
        
        for index, ship in enumerate(self.ships["names"]):
            print(f'Place your {ship}, it is {self.ships["length"][index]} long')
            user_input = input(': ')



    def create_cpu_board(self, board: List[List[str]]) -> None:
        for i in range(self.num_ships):
            ship = self.ships["chars"][i]

            while True:
                collision: bool = False
                x = choice([i for i in range(self.width)])
                y = choice([i for i in range(self.height)])

                if choice([True, False]):
                    if x + len(ship) > self.width:
                        x = self.width - len(ship)
                    
                    for a in range(len(ship)):
                        if board[x+a][y] != '.':
                            collision = True
                    
                    if collision:
                        continue

                    for j in range(len(ship)):
                        board[x+j][y] = ship[j]
                else:
                    if y + len(ship) > self.height:
                        y = self.height - len(ship)

                    for a in range(len(ship)):
                        if board[x][y+a] != '.':
                            collision = True
                    
                    if collision:
                        continue

                    for k in range(len(ship)):
                        board[x][y+k] = ship[k]
                
                break


class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    YELLOW = '\u001b[33m'
    RED = '\033[91m'
    BLACK = '\u001b[30m'
    ENDC = '\033[0m'
