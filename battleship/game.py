from __future__ import annotations
from typing import List
from battleship.helpers import isNotNumber
import time
import sys


class Game:
    """ the main game logic """
    def __init__(self):
        pass

    def start(self) -> None:
        self.welcome_message()
        self.show_options()

    def welcome_message(self) -> None:
        border: str = '\n' + '=' * 80 + '\n'
        print(
            border +
            '\n    Get Ready To Play Battleship !! \n' +
            '\n    - A turn based battleship game where you\'ll play against the cpu. \n' +
            '\n    - Your mission is to sink all of the cpu\'s ships. \n' +
            border
        )

    def show_options(self) -> None:
        options: List[str] = ['Play Battleship', 'View Top 10 Leaderboard', 'View Your Highest Score', 'Quit']
        valid_option: bool = False

        print('~~ MENU ~~ \n')
        
        for index, option in enumerate(options, start=1):
            print(f'{index}. {option}')

        print('\nPlease Choose An Option (1 - 4)')
        while not valid_option:
            user_input = input(': ')

            if isNotNumber and user_input not in ['1', '2', '3', '4']:
                sys.stdout.write("\033[F") 
                print('Invalid input, please try again.')
                time.sleep(2)
                sys.stdout.write("\033[F") 
                sys.stdout.write("\033[K")
                continue
            
            valid_option = True
            self.selected_option = int(user_input)
