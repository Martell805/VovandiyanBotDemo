import discord

from .role_post import RolePost


class RolePostHandler:
    def __init__(self, client: discord.Client):
        self.client = client
        self.__posts: dict[int: RolePost] = {}

    def add_post(self, post_info: dict) -> None:
        self.__posts[post_info['id']] = RolePost(self.client, post_info['id'], post_info['reactions'])

    def remove_post(self, post_id: int) -> None:
        del self.__posts[post_id]

    def get_post(self, post_id: int) -> RolePost:
        return self.__posts[post_id]

    def __getitem__(self, post_id: int) -> RolePost | None:
        if post_id in self.__posts:
            return self.__posts[post_id]
        return None

    def get_all_posts(self) -> dict[int: RolePost]:
        return self.__posts.copy()

    def reset_posts(self) -> None:
        self.__posts = {}

    async def on_add(self, payload) -> None:
        for post in self.__posts.values():
            await post.on_add(payload)

    async def on_remove(self, payload) -> None:
        for post in self.__posts.values():
            await post.on_remove(payload)
