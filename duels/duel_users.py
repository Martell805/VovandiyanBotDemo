from saver import User

from random import randint


class DuelUser(User):
    def __init__(self, id: int | str, name: str, wins: int | str = 0, games: int | str = 0, win_streak: int | str = 0):
        super().__init__(id, name)
        super().set_prefix("<DUELUSER>")
        self.__wins = int(wins)
        self.__games = int(games)
        self.__win_streak = int(win_streak)

    def __repr__(self) -> str:
        return f'{self.get_name()}: {self.get_wins()} побед из {self.get_games()} игр. ' \
               f'Серия побед - {self.get_win_streak()}'

    def __str__(self) -> str:
        return f'{self.get_prefix()} {self.get_id()} {self.get_name()} {self.get_wins()} {self.get_games()} ' \
               f'{self.get_win_streak()}'

    @classmethod
    def parse_user(cls, user_info):
        if not user_info.startswith(cls.get_class_prefix()):
            return None

        user_info = user_info.split()[1:]
        id = user_info[0]
        name = ' '.join(user_info[1:-3])
        wins = user_info[-3]
        games = user_info[-2]
        win_streak = user_info[-1]

        return cls(id, name, wins, games, win_streak)

    def roll(self) -> int:
        return randint(0, 100)

    def duel_result(self, enemy, winner) -> None:
        self.add_game(self == winner)

    def add_game(self, win: bool = False) -> None:
        self.__games += 1
        if win:
            self.__wins += 1
            self.__win_streak += 1
        else:
            self.__win_streak = 0

    def get_wins(self) -> int:
        return self.__wins

    def get_games(self) -> int:
        return self.__games

    def get_winrate(self) -> int:
        if self.get_games() == 0:
            return 0
        return int(self.get_wins() / self.get_games() * 100)

    def get_win_streak(self) -> int:
        return self.__win_streak
