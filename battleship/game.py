from __future__ import annotations
import os
from typing import List, Dict, Type
from .leaderboard import Leaderboard
from.battleship import Battleship
from .helpers import isNotNumber, heading, input_error


class Game:
    def __init__(self):
        self.leaderboard: Leaderboard = Leaderboard()
        self.start()
        # Battleship({
        #     'height': [6, 10, 6],
        #     'width': [6, 10, 6],
        #     'ships': [3, 5, 3]
        # }, self.leaderboard, self.restart, self.show_options)

    def start(self) -> None:
        self.welcome_message()
        self.login()

    def welcome_message(self) -> None:
        print(
            '\n' + '=' * 80 + '\n' +
            '\nGET READY TO PLAY BATTLESHIP !! \n' +
            '\nA turn based battleship game playing against the cpu. \n' +
            '\nObjective: \n' +
            '\n  - Sink all of the cpu\'s ships in as little moves as possible. \n' +
            '\nFeatures: \n' +
            '\n  - leaderboards, login, menus, configuarable board size \n' +
            '\n' + '=' * 80 + '\n'
        )

        input('Press enter to start ... \n')

    def login(self) -> None:
        options: List[str] = ['I\'m a New User', 'I\'m a Returning User', 'Quit']
        option: str = self.display_menu(options, 'LOGIN')
        response: int = 0
      
        if option == '1':
            response = self.leaderboard.new_user()
        elif option == '2':
            response = self.leaderboard.returning_user()
        else:
            self.restart()

        if response == 0:
            self.login()
        else:
            self.show_options()

    def show_options(self) -> None:
        options: List[str] = ['Play Battleship', 'View Top 10 Leaderboard', 'View Your Profile', 'Quit']
        option: str = self.display_menu(options, 'GAME')
        
        if option == '1':
            self.board_options()
        elif option == '2':
            self.leaderboard.get_top()
        elif option == '3':
            self.leaderboard.get_user_profile()
        else:
            self.restart()

        self.show_options()

    def display_menu(self, options: List[str], menu_text: str) -> str:
        valid_option: bool = False
        user_input: str = '0'

        print(heading(self.leaderboard.username))
        print(f'~~ {menu_text} MENU ~~ \n')

        for index, option in enumerate(options, start=1):
            print(f'{index}. {option}')

        print(f'\nPlease Choose an Option (1 - {len(options)})')

        while not valid_option:
            user_input: str = input(': ')

            if isNotNumber(user_input) and user_input not in [str(x) for x in range(1, len(options) + 1)]:
                input_error('Invalid input, please try again.', 1)
                continue

            valid_option = True

        return user_input

    def board_options(self) -> None:
        print(heading(self.leaderboard.username))
        print('~~ Board Dimensions ~~ \n')

        print('min-height:  6  -  min-width: 10  -  min-ships: 3')
        print('max-height:  6  -  max-width: 10  -  max-ships: 5')
        print('\n')

        board: Dict[str, List[int]] = {
            'height': [6, 10, 0],
            'width': [6, 10, 0],
            'ships': [3, 5, 0]
        }

        for key, value in board.items():
            while True:
                print(f'Enter the boards {key}')
                user_input: str = input(': ')

                if not isNotNumber(user_input):
                    if int(user_input) >= value[0] and int(user_input) <= value[1]:
                        board[key][2] = int(user_input)
                        print()
                        break
                
                input_error('Invalid input, please enter a valid number in range', 2)
        
        self.battleship: Battleship = Battleship(board, self.leaderboard, self.restart, self.show_options)
        self.battleship.start()
       
    def restart(self) -> None:
        os.system('clear')
        self.leaderboard = Leaderboard()
        self.start()
