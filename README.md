# Discord Downloader

---

## How To Use

```py
import downloader

downloader.EmojiDownloader(
    guild_id = ...,
    token = "...", # Your Discord Account Token
    filename_type = "name" # Optional, Must be in ["name", "id"]
).run() # run the program

downloader.StickerDownloader(
    ... # The available arguments are the same as "downloader.EmojiDownloader"
).run()
```