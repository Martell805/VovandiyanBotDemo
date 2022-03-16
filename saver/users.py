class User:
    def __init__(self, id: int | str, name: str):
        self.__id = int(id)
        self.__name = name
        self.__prefix = "<USER>"

    def __repr__(self) -> str:
        return f'{self.get_prefix()} {self.get_id()}. {self.get_name()}'

    def __str__(self) -> str:
        return f'{self.get_prefix()} {self.get_id()} {self.get_name()}'

    def get_prefix(self) -> str:
        return self.__prefix

    def set_prefix(self, prefix: str) -> None:
        self.__prefix = prefix

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    @classmethod
    def get_class_prefix(cls):
        return cls(0, "").get_prefix()

    @classmethod
    def parse_user(cls, user_info):
        if not user_info.startswith(cls.get_class_prefix()):
            return None

        user_info = user_info.split()[1:]
        id = user_info[0]
        name = ' '.join(user_info[1:-2])

        return cls(id, name)
