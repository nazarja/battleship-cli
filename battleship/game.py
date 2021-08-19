from __future__ import annotations
from battleship.leaderboard import Leaderboard
from typing import List
from battleship.helpers import isNotNumber
import time
import sys


class Game:
    """ the main game logic """
    def __init__(self):
        self.leaderboard = Leaderboard()
        self.username = None

    def start(self) -> None:
        self.welcome_message()
        self.login()
        self.show_options()

    def welcome_message(self) -> None:
        border: str = '\n' + '=' * 80 + '\n'
        print(
            border +
            '\n    Get Ready To Play Battleship !! \n' +
            '\n    - A turn based battleship game where you\'ll play against the cpu. \n' +
            '\n    - Including: Leaderboards, Menu\'s and User Generated Board Config \n' +
            border
        )

    def login(self) -> None:
        options: List[str] = ['Login With Password', 'Enter New Username', 'Quit']
        option: str = self.display_menu(options, 'LOGIN')
      
        if option == '1':
            print('LOGGING IN')
        elif option == '2':
            print('CREATE NEW USER')
        else:
            sys.exit()

    def show_options(self) -> None:
        options: List[str] = ['Play Battleship', 'View Top 10 Leaderboard', 'View Your Highest Score', 'Quit']
        option: str = self.display_menu(options, 'GAME')
        
        if option == '1':
            print('PLAY GAME')
        elif option == '2':
            print('TOP 10 LEADERBOARD')
        elif option == '3':
            print('TVIEW HIGHEST SCORE')
        else:
            sys.exit()

    def display_menu(self, options: List[str], menu_text: str) -> str:
        valid_option: bool = False

        print(f'~~ {menu_text} MENU~~ \n')

        for index, option in enumerate(options, start=1):
            print(f'{index}. {option}')

        print(f'\nPlease Choose an Option (1 - {len(options)})')
        while not valid_option:
            user_input: str = input(': ')

            if not isNotNumber(user_input) and user_input not in [str(x) for x in range(len(options))]:
                sys.stdout.write("\033[F") 
                print('Invalid input, please try again.')
                time.sleep(2)
                sys.stdout.write("\033[F\033[K")
                continue

            valid_option = True
            return user_input
        return '0'
