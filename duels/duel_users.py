from saver import User

from random import randint


class DuelUser(User):
    def __init__(self, id: int | str, name: str, wins: int | str = 0, games: int | str = 0):
        super().__init__(id, name)
        super().set_prefix("<DUELUSER>")
        self.__wins = int(wins)
        self.__games = int(games)

    def __repr__(self) -> str:
        return f'{self.get_name()}: {self.get_wins()} побед из {self.get_games()} игр.'

    def __str__(self) -> str:
        return f'{self.get_prefix()} {self.get_id()} {self.get_name()} {self.get_wins()} {self.get_games()}'

    @classmethod
    def parse_user(cls, user_info):
        if not user_info.startswith(cls.get_class_prefix()):
            return None

        user_info = user_info.split()[1:]
        id = user_info[0]
        name = ' '.join(user_info[1:-2])
        wins = user_info[-2]
        games = user_info[-1]

        return cls(id, name, wins, games)

    def roll(self) -> int:
        return randint(0, 100)

    def duel_result(self, enemy, winner) -> None:
        self.add_game(self == winner)

    def add_game(self, win: bool = False) -> None:
        self.__games += 1
        self.__wins += int(win)

    def get_wins(self) -> int:
        return self.__wins

    def get_games(self) -> int:
        return self.__games

    def get_winrate(self) -> int:
        if self.get_games() == 0:
            return 0
        return int(self.get_wins() / self.get_games() * 100)
