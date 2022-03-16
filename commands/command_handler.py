import discord


class CommandHandler:
    def __init__(self, client: discord.Client, prefix: str):
        self.__client = client
        self.__prefix = prefix
        self.__commands: dict = {}

    def add_command(self, command_name: str, answer) -> None:
        self.__commands[command_name] = answer

    def delete_command(self, command_name: str) -> None:
        del self.__commands[command_name]

    def get_command(self, command_name: str):
        return self.__commands.get(command_name, None)

    def __getitem__(self, command_name: str):
        return self.__commands.get(command_name, None)

    def get_all_commands(self):
        return self.__commands.copy()

    def set_prefix(self, prefix: str) -> None:
        self.__prefix = prefix

    def get_prefix(self) -> str:
        return self.__prefix

    async def answer(self, message: discord.Message) -> None:
        if not message.content.startswith(self.__prefix):
            return

        split_message = message.content.split()
        current_command = self.get_command(split_message[0][1:])

        if current_command is None:
            return
        try:
            await current_command(self.__client, message, *split_message[1:])
        except Exception as e:
            print(f'Ошибка при ответе на {current_command.__name__}: {e}')
