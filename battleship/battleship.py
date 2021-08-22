from __future__ import annotations
import time
from .leaderboard import Leaderboard
from .helpers import heading, input_error, Colors
from typing import Dict, List, Callable
from random import choice


class Battleship:
    def __init__(self, board: Dict[str, List[int]], leaderboard: Leaderboard, restart: Callable):
        self.leaderboard: Leaderboard = leaderboard
        self.height: int = board["height"][2]
        self.width: int = board["width"][2]
        self.cpu_hits = 0
        self.hits = 0
        self.misses = 0
        self.restart = restart
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
        self.play()

    def choose_board_creation(self):
        print(heading(self.leaderboard.username))

        print('~~ You can manually place your ships or auto create your board ~~\n')
        print('Manual or Auto Create Board?\n')

        user_input: str = ''

        while True:
            user_input = input('manual or auto: ')
            if user_input.lower() not in ['manual', 'auto']:
                input_error('Invalid input, Choices are manual or auto', 1)
                continue
            else:
                break
        
        if user_input.lower() == 'manual':
            self.create_user_board()
            self.auto_create_board(self.cpu_board)
            self.print_boards()
        else:
            self.auto_create_board(self.cpu_board)
            self.auto_create_board(self.user_board)

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
        print('\n - Type "quit" to return to the menu \n')
        time.sleep(2)
       
        for index, ship in enumerate(self.ships["names"]):
            length: str = self.ships["length"][index]
            direction_input: str = 'h'
            direction_absent: bool = True

            while True:
                self.print_boards()

                print(f'- Place your {ship}, it is {length} lengths long\n')

                while direction_absent:
                    print('Place ship horizontal ⇄, or vertical ⇅, ?')
                    direction_input: str = input('h or v: ')

                    if direction_input == 'quit':
                        self.restart()
                    elif direction_input.lower() not in ['h', 'v']:
                        input_error('Invalid input, options are: h or v', 2)
                        continue
                    else:
                        direction_absent = False
                        input_error('', 2)
                        break
                
                print(f'Enter the {self.direction_str[direction_input]} x, y coordinates. Seperated by a comma.')
                user_input = input('x , y: ')
                
                if user_input == 'quit':
                    self.restart()
                
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
    
    def play(self) -> None:
        self.print_boards()
        turns: List[Callable] = [self.player_turn, self.cpu_turn]
        user_input: str = ''

        print('Choose heads or tails')
        while True:
            user_input = input(': ')
            if user_input.lower() not in ['heads', 'tails']:
                input_error('Invalid input, please choose \'heads\' or \'tails\'', 1)
                continue
            else:
                if user_input != choice(['heads', 'tails']):
                    turns = [turns[1], turns[0]]
                    input_error('You lost the coin toss, CPU goes first', 2)
                else:
                    input_error('You won the coin toss, You go first', 2)
                break    
        
        while True:
            self.print_boards()

            if not turns[0]():
                break

            if not turns[1]():
                break

    def player_turn(self) -> int:
        print('Enter your coords to fire in the format: x, y')
        while True:
            user_input = input('Your Turn: ')

            if user_input == 'quit':
                self.restart()

            user_input = [c.strip() for c in user_input.split(',')]
            
            if len(user_input) != 2:
                input_error('Please enter coords in the correct format: x , y', 1)
            elif user_input[0].isdigit() and user_input[1].isdigit():
                x = int(user_input[0])
                y = int(user_input[1])
                pos = self.cpu_board[x][y]
                
                if pos != '.':
                    input_error('You have already fired there', 1)
                    continue
                if pos in self.ships["chars"]:
                    pos = Colors.RED + '✴️' + Colors.ENDC
                    input_error('You have hit a boat!', 2)
                else:
                    pos = Colors.ORANGE + '⚬' + Colors.ENDC
                    input_error('You have missed!', 2)
                break
            else:
                input_error('Please enter coords in the correct format: X , Y', 1)
                continue

        return 0

    def cpu_turn(self) -> int:
        input('CPU Turn: ')
        input_error('', 2)
        return 1

    def update_board(self, board: List[List[str]], x: int, y: int) -> str:
        # check if tile already used

        # update tile

        # return status
        return ''
