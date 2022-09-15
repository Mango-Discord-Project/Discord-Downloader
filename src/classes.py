import requests as req

class Item:
    def __init__(self, token: str, url: str) -> None:
        self.token = token
        self.url = url
        
        # check token is useable
        respond: req.Request = req.get('https://discord.com/api/v9/users/@me', headers={'authorization': token})
        if not respond.ok:
            raise ValueError(f'Token cannot connect to discord Server')
    
    def check_online(self):
        return req.get('https://discord.com/api/v9/users/@me', headers={'authorization': self.token}).ok

__all__ = [Item]