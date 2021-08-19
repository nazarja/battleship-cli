from __future__ import annotations
import typing


class Game:
    """ the main game logic """
    def __init__(self):
        self.start()

    def start(self) -> None:
        self.welcome_message()
        self.get_nickname()

    def welcome_message(self) -> None:
        print()

    def get_nickname(self) -> None:
        nickname = input('Please enter a nickname: \n')