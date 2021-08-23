from __future__ import annotations
import time
from functools import reduce
from .leaderboard import Leaderboard
from .helpers import heading, input_error, input_message, Colors
from typing import Dict, List, Callable, Tuple
from random import choice
# from itertools import product, starmap


class Battleship:
    def __init__(self, board: Dict[str, List[int]], leaderboard: Leaderboard, restart: Callable, show_options: Callable):
        self.leaderboard: Leaderboard = leaderboard
        self.height: int = board["height"][2]
        self.width: int = board["width"][2]
        self.cpu_hits: int = 0
        self.player_hits: int = 0
        self.player_misses: int = 0
        self.player_score: int = 0
        self.restart: Callable = restart
        self.show_options: Callable = show_options
        self.num_ships: int = board["ships"][2]
        self.user_board: List[List[str]] = []
        self.hits_board: List[List[str]] = []
        self.cpu_board: List[List[str]] = []
        self.cpu_last_hit: List[int] = []
        self.direction_str: Dict[str, str] = {'h': 'horizontal', 'v': 'vertical'}
        self.heading: str = (
            f'{self.leaderboard.username} | '
            f' {Colors.BLUE}hits{Colors.ENDC}: {self.player_hits}'
            f' - {Colors.BLUE}misses{Colors.ENDC}: {self.player_misses}'
            f' - {Colors.BLUE}score{Colors.ENDC}: {self.player_score}'
        )
        self.ships: Dict[str, List[str]] = {
            "names": ['Submarine', 'Destroyer', 'Crusier', 'Battleship', 'Aircraft Carrier'][:self.num_ships],
            "codes": ['A', 'B', 'C', 'D', 'S'],
            "chars": ['S' * 2, 'D' * 3, 'C' * 3, 'B' * 4, 'A' * 5][:self.num_ships],
            "length": ['2', '3', '3', '4', '5'][:self.num_ships]
        }

    def start(self) -> None:
        self.create_boards()
        self.choose_board_creation()
        self.play()

    def choose_board_creation(self):
        print(heading(self.leaderboard.username))

        print('Create board \'manual\' or \'auto\'\n')

        user_input: str = ''

        while True:
            user_input = input('manual or auto: ')
            if user_input.lower() not in ['manual', 'auto']:
                input_error('Invalid input, Choices are \'manual\' or \'auto\'', 1)
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
        print(heading(self.heading))

        print(
            ' ' * self.width, 'Your Board',
            ' ' * (self.width * 3), 'CPU Board', '\n'
        )

        print(
            ' ' * 3, ''.join(f'{str(x):3s}' for x in range(self.width)),
            ' ' * 5,
            ' ' * 3, ''.join(f'{str(x):3s}' for x in range(self.width)),
            # ' ' * 5,
            # ' ' * 3, ''.join(f'{str(x):3s}' for x in range(self.width)),
        )

        for i, row in enumerate(zip(self.user_board, self.hits_board, self.cpu_board)):
            print(
                f'{str(i):3s}', ''.join(f'{self.colorize_char(y):3s}' for y in row[0]),
                ' ' * 5,
                f'{str(i):3s}', ''.join(f'{self.colorize_char(y):3s}' for y in row[1]),
                # ' ' * 5,
                # f'{str(i):3s}', ''.join(f'{self.colorize_char(y):3s}' for y in row[2]),
            )

        print('\n')

    def colorize_char(self, c: str) -> str:
        if c in self.ships['codes']:
            return Colors.CYAN + c + ' ' * 2 + Colors.ENDC
        elif c == '🟏':
            return Colors.RED + '🟏' + ' ' * 2 + Colors.ENDC
        elif c == '×':
            return Colors.ORANGE + '×' + ' ' * 2 + Colors.ENDC
        return c

    def auto_create_board(self, board: List[List[str]]) -> None:
        for i in range(self.num_ships):
            ship: str = self.ships["chars"][i]

            while True:
                x: int = choice([i for i in range(self.width)])
                y: int = choice([i for i in range(self.height)])
                h_or_v: str = 'h' if choice([True, False]) else 'v'

                if self.validate_placement(y, x, int(self.ships["length"][i]), h_or_v, board):
                    self.place_ship(y, x, int(self.ships["length"][i]), ship[0], h_or_v, board)
                    break

    def create_user_board(self) -> None:
        print(heading(self.leaderboard.username))
       
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
                        input_message('', 2)
                        break
                
                print(f'Enter the {self.direction_str[direction_input]} y, x coordinates. Seperated by a comma.')
                user_input = input('y, x: ')
                
                if user_input == 'quit':
                    self.restart()
                
                user_input = [c.strip() for c in user_input.split(',')]

                if len(user_input) != 2:
                    input_error('Please enter co-ords in the correct format: y, x', 2)
                    continue
                elif user_input[0].isdigit() and user_input[1].isdigit():
                    if self.validate_placement(int(user_input[0]), int(user_input[1]), int(length), direction_input, self.user_board):
                        self.place_ship(int(user_input[0]), int(user_input[1]), int(length), ship[0], direction_input, self.user_board)
                        break
                    else:
                        input_error('Ship cannot be placed there, please try again', 2)
                else:
                    input_error('Please enter co-ords in the correct format: y, x', 2)
                    continue

    def validate_placement(self, y: int, x: int, length: int, direction_input: str, board: List[List[str]]) -> bool:
        if direction_input == 'h':
            if x + length <= self.width:
                for i in range(length):
                    if board[y][x+i] != '.':
                        return False
            else:
                return False
        else:
            if y + length <= self.height:
                for i in range(length):
                    if board[y+i][x] != '.':
                        return False
            else:
                return False
        return True

    def place_ship(self, y: int, x: int, length: int, char: str, direction_input: str, board: List[List[str]]) -> None:
        for i in range(length):
            if direction_input == 'h':
                board[y][x+i] = char
            else:
                board[y+i][x] = char
    
    def play(self) -> None:
        self.print_boards()
        turns: List[Callable] = [self.player_turn, self.cpu_turn]
        user_input: str = ''

        print('Choose \'heads\' or \'tails\'')
        while True:
            user_input = input(': ')
            if user_input.lower() not in ['heads', 'tails']:
                input_error('Invalid input, please choose \'heads\' or \'tails\'', 1)
                continue
            else:
                if user_input != choice(['heads', 'tails']):
                    turns = [turns[1], turns[0]]
                    input_message('You lost the coin toss, CPU goes first', 2)
                else:
                    input_message('You won the coin toss, You go first', 2)
                break
        
        while True:
            self.print_boards()
            if turns[0]():
                break
            self.print_boards()
            if turns[1]():
                break

        self.print_boards()
        self.show_winner()
        self.show_options()

    def player_turn(self) -> bool:
        print('Enter your co-ords to fire in the format: y, x')
        while True:
            user_input = input('Your Turn: ')

            if user_input == 'quit':
                self.restart()

            user_input = [c.strip() for c in user_input.split(',')]
            
            if len(user_input) != 2:
                input_error('Please enter co-ords in the correct format: y, x', 1)
            elif user_input[0].isdigit() and user_input[1].isdigit():
                if int(user_input[0]) > (self.height - 1) or int(user_input[1]) > (self.width - 1):
                    input_error(f'Invalid input,is  y up to {self.height - 1} and x up to {self.width - 1}', 1)
                    continue

                y = int(user_input[0])
                x = int(user_input[1])
                pos = self.cpu_board[y][x]
                
                if pos in ['×', '🟏']:
                    input_message('You have already fired there', 1)
                    continue
                if pos in self.ships["codes"]:
                    character: str = '🟏'
                    self.hits_board[y][x] = character
                    self.cpu_board[y][x] = character
                    self.player_hits += 1
                    self.player_score += 20
                    self.update_heading()
                    input_message('You have hit a boat!', 2)
                else:
                    character: str = '×'
                    self.hits_board[y][x] = character
                    self.cpu_board[y][x] = character
                    self.player_misses += 1
                    self.player_score -= 5
                    self.update_heading()
                    input_message('You have missed!', 2)
                break
            else:
                input_error('Please enter co-ords in the correct format: y, x', 1)
                continue

        if self.check_win():
            return True
        return False

    def cpu_turn(self) -> int:
        print('CPU is firing...')
        print('CPU Turn: ')

        while True:
            y: int = choice([x for x in range(self.height)])
            x: int = choice([x for x in range(self.width)])

            if self.cpu_last_hit != []:
                neighbours = self.get_neighbours(self.cpu_last_hit[0], self.cpu_last_hit[1])
                y, x = choice(neighbours)

            try:
                pos = self.user_board[y][x]
            except IndexError:
                continue

            if pos in ['×', '🟏']:
                continue
            if pos in self.ships["codes"]:
                character: str = '🟏'
                self.user_board[y][x] = character
                self.cpu_hits += 1
                self.cpu_last_hit = [y, x]
                input_message('CPU has hit your boat!', 2)
            else:
                character: str = '×'
                self.user_board[y][x] = character
                self.cpu_last_hit = []
                input_message('CPU has missed!', 2)
            break

        if self.check_win():
            return True
        return False

    def get_neighbours(self, y: int, x: int) -> List[Tuple[int, int]]:
        def remove_cells(t: tuple):
            if t[0] > self.width or t[0] < 0:
                return False
            if t[1] > self.height or t[1] < 0:
                return False
            return True

        cells = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        # cells = starmap(lambda a, b: (x + a, y + b), product((0, -1, +1), (0, -1, +1)))
        # cells = list(cells)[1:]
        return list(filter(remove_cells, cells))

    def check_win(self) -> bool:
        num_of_boat_tiles: int = reduce(lambda a, b: a + b, [int(i) for i in self.ships['length']])
        return True if num_of_boat_tiles in [self.cpu_hits, self.player_hits] else False

    def show_winner(self) -> None:
        print(heading(self.heading))
        player_won: bool = self.player_hits > self.cpu_hits
        if self.player_score < 0:
            self.player_score = 0

        if player_won:
            print(
                f'\nCongratulations {self.leaderboard.username}, You WON!!\n'
                f'\nYou had {self.player_hits} Hits and {self.player_misses} Misses\n'
                f'\nYour final score is {self.player_score} points\n'
            )
            self.leaderboard.update_user_score(self.leaderboard.username, self.player_score)
            time.sleep(5)
        else:
            print('CPU Won, please try again...')
            time.sleep(3)

    def update_heading(self) -> None:
        self.heading: str = (
            f'{self.leaderboard.username} | '
            f' {Colors.BLUE}hits{Colors.ENDC}: {self.player_hits}'
            f' - {Colors.BLUE}misses{Colors.ENDC}: {self.player_misses}'
            f' - {Colors.BLUE}score{Colors.ENDC}: {self.player_score}'
        )
