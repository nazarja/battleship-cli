from __future__ import annotations
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

        if os.environ.get('CREDS'):
            self.creds = json.loads(os.environ.get('CREDS'))
        else:
            self.creds = Credentials.from_service_account_file('creds.json')

        self.scoped_creds = self.creds.with_scopes(self.scope)
        self.client = gspread.authorize(self.scoped_creds)
        self.sheet = self.client.open('Battleship')
        self.leaderboard: List[str] = self.sheet.worksheet('leaderboard').get_all_values()
