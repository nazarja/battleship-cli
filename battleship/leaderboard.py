from __future__ import annotations
import os
import json
import gspread
from bcrypt import gensalt, hashpw
from google.oauth2.service_account import Credentials
from typing import List
from .helpers import get_score_as_int, heading, input_error


class Leaderboard:
    def __init__(self):
        self.scope: List[str] = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]

        if os.environ.get('CREDS'):
            self.creds = Credentials.from_service_account_info(json.loads(os.environ.get('CREDS')))
        else:
            self.creds = Credentials.from_service_account_file('creds.json')

        self.scoped_creds = self.creds.with_scopes(self.scope)
        self.client = gspread.authorize(self.scoped_creds)
        self.sheet = self.client.open('Battleship')
        self.worksheet = self.sheet.worksheet('leaderboard')
        self.get_leaderboard()

    def new_user(self) -> int:
        print(heading())
        print('~~ Enter \'quit()\' to return to the login menu. ~~ \n')

        while True:
            print('Enter New Username')
            username_input: str = input(': ')

            if username_input == 'quit()':
                return  0
            elif len(username_input) < 3:
                input_error('Invalid input, Username must be more than 3 characters', 2)
                continue
            
            if self.get_user(username_input) == []:
                print(heading())
                while True:
                    print('Please enter a password')
                    password_input: str = input(': ')

                    if password_input == 'quit()':
                        return 0
                    elif len(password_input) < 5:
                        input_error('Invalid, Password must be more than 5 characters.', 2)
                        continue
                    else:
                        password: bytes = hashpw(bytes(password_input, 'utf-8'), gensalt())
                        self.worksheet.append_row([username_input.capitalize(), str(password), 0, 0])
                        self.get_leaderboard()
                        return 1
            else:
                input_error('Invalid input, Username is already is use.', 2)
                continue

        return 0

    def returning_user(self) -> int:
        print(heading())

        user_input: str = input('Enter Your Username: \n')

        for entry in self.leaderboard:
            username: str = entry[0]
            if user_input.capitalize() == username:
                print(f'Welcome back, {username}')

        return 0
        
    def get_leaderboard(self):
        self.leaderboard = self.worksheet.get_all_values()[1:]

    def get_top(self) -> List[List[str]]:
        return sorted(self.leaderboard.copy(), key=get_score_as_int, reverse=True)[:10]

    def get_user(self, username: str) -> List[str]:
        for entry in self.leaderboard:
            if username.capitalize() == entry[0]:
                return entry

        return []
