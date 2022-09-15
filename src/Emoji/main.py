import os

from rich import print
from rich.console import Console
import requests as req
import pretty_errors

console = Console()

class EmojiRequester:
    def __init__(self, token: str, api_version: int = 9) -> None:
        self.token = token
        self.api = f'https://discord.com/api/v{api_version}'
        self.last_values = {}
        self.header = {'Authorization': self.token}
        self.root_dir = './src/Emoji/emojis'
        
        # check token is useable
        if not self.check_online():
            raise ValueError(f'Token cannot connect to discord Server')
        # check download folder path
        if not os.path.isdir(self.root_dir):
            os.mkdir(self.root_dir)
    
    def check_online(self):
        return self.request_get(f'/users/@me').ok
    
    def save_last_values(self, data: dict) -> dict:
        self.last_values |= {k: v for k, v in data.items() if k != 'self'}
        return data
    
    def get(self, type: str = 'list_guild_emojis', **kwargs):
        ...
        
    def request_get(self, url: str):
        return req.get(f'{self.api}{url}', headers=self.header)
        
    # def check_values(func):
    #     def wrapper(**kwargs):
    #         for k, v in kwargs.copy():
    #             if k == 'self':
    #                 continue
    #             if (v | kwargs['self'].last_values.get(k, default=False)) ^ 1: # not v and not k == not (v or k)
    #                 raise ValueError('guild_id not in cache')
    #         kwargs['self'].save_last_values(locals())    
    #         return func(**kwargs)
    #     return wrapper
    
    def list_guild_emojis(self, *, guild_id: int) -> list[dict]:
        return self.request_get(f'/guilds/{guild_id}/emojis').json()
    
    def get_guild_emoji(self, *, guild_id: int, emoji_id: int) -> dict:
        return self.request_get(f'/guilds/{guild_id}/emojis/{emoji_id}').json()
    
    def download_guild_all_emojis(self, *, guild_id: int, folder: str | None = None):
        if folder is None and not os.path.isdir(download_dir:=f'{self.root_dir}/{guild_id}'):
            os.mkdir(download_dir)
        
        success, failed = 0, 0
        for item in self.list_guild_emojis(guild_id=guild_id):
            try:
                image_format = 'gif' if item['animated'] else 'png'
                image_filename = f'{item["id"]}.{image_format}'
                
                image = req.get(f'https://cdn.discordapp.com/emojis/{image_filename}').content
                with open(f'{download_dir}/{image_filename}', 'wb') as file:
                    file.write(image)
            except Exception as error:
                console.log(f'error: {error}')
                failed += 1
            else:
                console.log(f'download {image_filename} successful, path: {download_dir}')
                success += 1
        console.log(f'tasks all finished, success: {success}, failed: {failed}')
