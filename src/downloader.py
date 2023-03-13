import logging
import os
import typing
import requests
import json


logging.basicConfig(level=logging.INFO)

API_VERSION = 10
API_BASE_URL = f"https://discord.com/api/v{API_VERSION}"


def download_emoji(
    guild_id: int,
    token: str,
    save_path: str = "./data/emojis",
    filename_type: str = "name",
) -> None:
    # Create dirs
    save_path = f"{save_path}/{guild_id}"
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    logging.info(f"Create dirs: \"{save_path}\"")

    # Get emoji list
    emoji_list: list[dict] = requests.get(
        url=f"{API_BASE_URL}/guilds/{guild_id}", headers={"Authorization": token}
    ).json()["emojis"]
    logging.info("Get emoji list")

    # Save emoji information
    with open(
        file=f"{save_path}/emoji_info.json", mode="w", encoding="utf-8"
    ) as file_ref:
        json.dump(obj=emoji_list, fp=file_ref, indent=2)
    logging.info(f"Save emoji file on \"{save_path}/emoji_info.json\"")

    # Data mapping
    image_format_mapping = ["png", "apng"]

    # Save files
    logging.info("Download emoji task start...")
    for emoji_object in emoji_list:
        filename = f"{emoji_object[filename_type]}.{image_format_mapping[emoji_object['animated']]}"
        image_bytes = requests.get(
            f"https://cdn.discordapp.com/emojis/{emoji_object['id']}?size=4096&quality=lossless"
        ).content
        with open(file=f"{save_path}/{filename}", mode="wb") as file_ref:
            file_ref.write(image_bytes)
        logging.info(f"Save file success, {filename = }")
    logging.info("Download emoji task done...")


__all__ = ["download_emoji"]
