from __future__ import annotations
from posix import environ
from typing import List
import os
import json
import gspread
from google.oauth2.service_account import Credentials


class Leaderboard:
    """ groups together methods to deal with google sheets """
    def __init__(self):
        self.scope: List[str] = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]

        self.creds = Credentials.from_service_account_file(
            os.environ.get('CREDS') if os.environ.get('CREDS') else 'creds.json'
        )
        self.scoped_creds = self.creds.with_scopes(self.scope)
        self.client = gspread.authorize(self.scoped_creds)
        self.sheet = self.client.open('Battleship')
        self.leaderboard: List[str] = self.sheet.worksheet('leaderboard').get_all_values()
