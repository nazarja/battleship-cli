from __future__ import annotations
import time
from .leaderboard import Leaderboard
from .helpers import heading, input_error, isNotNumber
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
        self.direction_str: Dict[str, str] = {'h': 'horizontal', 'v': 'vertical'}
        self.ships: Dict[str, List[str]] = {
            "names": ['Submarine', 'Destroyer', 'Crusier', 'Battleship', 'Aircraft Carrier'][:self.num_ships],
            "codes": ['A', 'B', 'C', 'D', 'S'],
            "chars": ['S' * 2, 'D' * 3, 'C' * 3, 'B' * 4, 'A' * 5][:self.num_ships],
            "length": ['2', '3', '3', '4', '5'][:self.num_ships]
        }

        self.start()

    def start(self) -> None:
        self.create_boards()
        self.choose_board_creation()

    def choose_board_creation(self):
        print(heading(self.leaderboard.username))

        print('~~ You can manually place your ships or auto create your board ~~\n')
        print('Manual or Auto Create Board?\n')

        user_input: str = ''

        while True:
            user_input = input('m or a: ')
            if user_input.lower() not in ['m', 'a']:
                input_error('Invalid input, Choices are m or a', 1)
                continue
            else:
                break
        
        if user_input.lower() == 'm':
            self.create_user_board()
            self.auto_create_board(self.cpu_board)
            self.print_boards()
        else:
            self.auto_create_board(self.cpu_board)
            self.auto_create_board(self.user_board)
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
                f'{str(i):3s}', ''.join(f'{self.colorize_char(y):3s}' for y in row[0]),
                ' ' * 5,
                f'{str(i):3s}', ''.join(f'{self.colorize_char(y):3s}' for y in row[1]),
            )

        print('\n')

    def colorize_char(self, c: str) -> str:
        if c in self.ships['codes']:
            return Colors.BLUE + c + ' ' * 2 + Colors.ENDC
        return c

    def auto_create_board(self, board: List[List[str]]) -> None:
        for i in range(self.num_ships):
            ship: str = self.ships["chars"][i]

            while True:
                x: int = choice([i for i in range(self.width)])
                y: int = choice([i for i in range(self.height)])
                h_or_v: str = 'h' if choice([True, False]) else 'v'

                if self.validate_placement(x, y, int(self.ships["length"][i]), h_or_v, board):
                    self.place_ship(x, y, int(self.ships["length"][i]), ship[0], h_or_v, board)
                    break

    def create_user_board(self) -> None:
        print(heading(self.leaderboard.username))

        print(f'\n~~ Place your {self.num_ships} ships ~~ \n')
        print(f'\nx is horizontal, y is vertical \n')
        print(f'\nEnter your input in the format: x , y')
        
        time.sleep(3)
        
        for index, ship in enumerate(self.ships["names"]):
            length: str = self.ships["length"][index]
            direction_input: str = 'h'
            direction_absent: bool = True

            while True:
                self.print_boards()

                print(f'Place your {ship}, it is {length} lengths long\n')

                while direction_absent:
                    print('Place ship horizontal or vertical?')
                    direction_input: str = input('h or v: ')

                    if direction_input.lower() not in ['h', 'v']:
                        input_error('Invalid input, options are: h or v', 2)
                        continue
                    else:
                        direction_absent = False
                        input_error('', 2)
                        break
                
                print(f'Enter the {self.direction_str[direction_input]} x, y coordinates. Seperated by a comma.')
                user_input = input('x , y: ')
                user_input = [c.strip() for c in user_input.split(',')]

                if len(user_input) != 2:
                    input_error('Please enter coords in the correct format: x , y', 2)
                    continue
                elif user_input[0].isdigit() and user_input[1].isdigit():
                    if self.validate_placement(int(user_input[0]), int(user_input[1]), int(length), direction_input, self.user_board):
                        self.place_ship(int(user_input[0]), int(user_input[1]), int(length), ship[0], direction_input, self.user_board)
                        break
                    else:
                        input_error('Ship cannot be placed there, please try again', 2)
                else:
                    input_error('Please enter coords in the correct format: X , Y', 2)
                    continue

    def validate_placement(self, x: int, y: int, length: int, direction_input: str, board: List[List[str]]) -> bool:
        if direction_input == 'v':
            if x + length < self.width:
                for i in range(length):
                    if board[x+i][y] != '.':
                        return False
            else:
                return False
        else:
            if y + length < self.height:
                for i in range(length):
                    if board[x][y+i] != '.':
                        return False
            else:
                return False
        return True

    def place_ship(self, x: int, y: int, length: int, char: str, direction_input: str, board: List[List[str]]) -> None:
        for i in range(length):
            if direction_input == 'v':
                board[x+i][y] = char
            else:
                board[x][y+i] = char


class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    YELLOW = '\u001b[33m'
    RED = '\033[91m'
    BLACK = '\u001b[30m'
    ENDC = '\033[0m'
