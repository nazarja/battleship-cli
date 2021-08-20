from __future__ import annotations
import os
from typing import List
from .leaderboard import Leaderboard
from .helpers import isNotNumber, heading, input_error


class Game:
    def __init__(self):
        self.leaderboard = Leaderboard()

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
            print('PLAY GAME')
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

            if not isNotNumber(user_input) or user_input not in [str(x) for x in range(1, len(options) + 1)]:
                input_error('Invalid input, please try again.', 1)
                continue

            valid_option = True

        return user_input

    def restart(self) -> None:
        os.system('clear')
        self.leaderboard = Leaderboard()
        self.start()
