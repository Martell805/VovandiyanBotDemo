from .time_score import get_current_score_msk


class User:
    def __init__(self, id: int | str, name: str, score: int | str = 0, last_change: int = get_current_score_msk()):
        self.id = int(id)
        self.score = int(score)
        self.name = name
        self.last_change = last_change

    def __repr__(self) -> str:
        return f'<USER> {self.id}. {self.name}: {self.score} очков'

    def __str__(self) -> str:
        return f'<USER> {self.id} {self.name} {self.score} {self.last_change}'

    def on_enter(self) -> int:
        current_score = get_current_score_msk()
        self.last_change = current_score
        return self.last_change

    def on_exit(self) -> int:
        current_score = get_current_score_msk()
        change = current_score - self.last_change

        self.score += change
        self.last_change = current_score

        return change
