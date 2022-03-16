from saver import User

from .time_score import get_current_score_msk


class ScoreUser(User):
    def __init__(self, id: int | str, name: str, score: int | str = 0,
                 last_change: int | str = get_current_score_msk()):
        super().__init__(id, name)
        super().set_prefix("<USER>")
        self.__score = int(score)
        self.__last_change = int(last_change)

    def __repr__(self) -> str:
        return f'{self.get_name()}: {self.__score} очков'

    def __str__(self) -> str:
        return f'{self.get_prefix()} {self.get_id()} {self.get_name()} {self.get_score()} {self.get_last_change()}'

    @classmethod
    def parse_user(cls, user_info):
        if not user_info.startswith(cls.get_class_prefix()):
            return None

        user_info = user_info.split()[1:]
        id = user_info[0]
        name = ' '.join(user_info[1:-2])
        score = user_info[-2]
        last_change = user_info[-1]

        return cls(id, name, score, last_change)

    def get_score(self) -> int:
        return self.__score

    def add_score(self, score: int):
        self.__score += score

    def set_score(self, score: int) -> None:
        self.__score = score

    def get_last_change(self) -> int:
        return self.__last_change

    def on_enter(self) -> int:
        current_score = get_current_score_msk()
        self.__last_change = current_score
        return self.__last_change

    def on_exit(self) -> int:
        current_score = get_current_score_msk()
        change = current_score - self.__last_change

        self.__score += change
        self.__last_change = current_score

        return change


