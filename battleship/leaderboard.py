from __future__ import annotations
import os
import json
import gspread
from typing import List
from google.oauth2.service_account import Credentials
from .helpers import get_score_as_int, heading, input_error, display_quit_info
from bcrypt import gensalt, hashpw, checkpw


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
        display_quit_info()

        while True:
            print('Enter New Username')
            username_input: str = input(': ')

            if username_input == 'quit':
                return 0
            elif len(username_input) < 3:
                input_error('Invalid input, Username must be more than 3 characters', 2)
                continue
            elif self.get_user(username_input) == []:
                print(heading())
                display_quit_info()

                while True:
                    print('Please enter a password')
                    password_input: str = input(': ')

                    if password_input == 'quit':
                        return 0
                    elif len(password_input) < 5:
                        input_error('Invalid, Password must be more than 5 characters.', 2)
                        continue
                    else:
                        self.user: str = username_input
                        password: bytes = hashpw(bytes(password_input, 'utf-8'), gensalt())
                        self.worksheet.append_row([username_input.capitalize(), str(password), 0, 0])
                        self.get_leaderboard()
                        return 1
            else:
                input_error('Invalid input, Username is already is use.', 2)
                continue

    def returning_user(self) -> int:
        print(heading())
        display_quit_info()

        while True:
            print('Enter New Username')
            user_input: str = input(': ')
            user: List[str] = self.get_user(user_input)

            if user_input == 'quit':
                return 0
            elif user == []:
                input_error('User not found, please try again.', 2)
                continue
            else:
                print(heading())
                display_quit_info()

                while True:
                    print('Enter Your Password.')
                    password_input = input(': ')
                    
                    if checkpw(bytes(password_input, 'utf-8'), bytes(user[1][2:-1], 'utf-8')):
                        self.user: List[str] = user
                        return 1
                    else:
                        input_error('Incorrect password, please try again.', 2)
                
    def get_leaderboard(self):
        self.leaderboard = self.worksheet.get_all_values()[1:]

    def get_top(self) -> List[List[str]]:
        return sorted(self.leaderboard.copy(), key=get_score_as_int, reverse=True)[:10]

    def get_user(self, username: str) -> List[str]:
        for entry in self.leaderboard:
            if username.capitalize() == entry[0]:
                return entry

        return []
