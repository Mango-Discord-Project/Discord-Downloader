import logging
import os
import json

import requests
import pretty_errors

logging.basicConfig(level=logging.INFO)

API_VERSION = 10
API_BASE_URL = f"https://discord.com/api/v{API_VERSION}"


def create_dirs(dirs: str):
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    logging.info(f'Create dirs: "{dirs}"')
    return dirs


def get_guild_object(guild_id: int, token: str) -> dict:
    return requests.get(
        url=f"{API_BASE_URL}/guilds/{guild_id}", headers={"Authorization": token}
    ).json()


def save_information(file_path: str, information: dict | list):
    with open(file=f"{file_path}.json", mode="w", encoding="utf-8") as file_ref:
        json.dump(obj=information, fp=file_ref, indent=2)
    logging.info(f'Save emoji file on "{file_path}/emoji_info.json"')


class GuildDownloader:
    object_type: str
    image_format_mapping: tuple[str] | dict[int, str]
    format_key: str
    assets_url: str
    filename_type: str = "name"

    def __init__(
        self,
        guild_id: int,
        token: str,
    ) -> None:
        self.save_path = create_dirs(f"./data/{self.object_type}/{guild_id}")
        self.object_list = get_guild_object(guild_id, token)[self.object_type]
        logging.info(f"Get {object} list")
        save_information(
            f"{self.save_path}/{self.object_type}_information", self.object_list
        )

    def run(self):
        logging.info(f"Download {self.object_type} task start...")
        for object in self.object_list:
            filename = f"{object[self.filename_type]}.{self.image_format_mapping[object[self.format_key]]}"
            image_bytes = requests.get(self.assets_url.format(object["id"])).content
            with open(file=f"{self.save_path}/{filename}", mode="wb") as file_ref:
                file_ref.write(image_bytes)
            logging.info(f"Save file success, {filename = }")
        logging.info(f"Download {self.object_type} task done...")


class EmojiDownloader(GuildDownloader):
    object_type = "emojis"
    image_format_mapping = "png", "apng"
    format_key = "animated"
    assets_url = "https://cdn.discordapp.com/emojis/{}?size=4096&quality=lossless"


class StickersDownloader(GuildDownloader):
    object_type = "stickers"
    image_format_mapping = ("", "png", "apng", "json", "gif")
    format_key = "format_type"
    assets_url = "https://media.discordapp.net/stickers/{}?size=4096"


__all__ = ["EmojiDownloader", "StickersDownloader"]
