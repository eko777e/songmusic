import os
import re
import random
from dotenv import load_dotenv
from pyrogram import filters

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

SONG_DOWNLOAD_DURATION = int(os.getenv("SONG_DOWNLOAD_DURATION", "180"))
SONG_DOWNLOAD_DURATION_LIMIT = time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00")
PLAYLIST_CHANNEL = "UzeyirPlaylist"
PLAYLIST_URL = "https://t.me/UzeyirPlaylist"
BOT_USERNAME = "UzeyirMusic_Bot"
OWNER_IDS = [8493825254]
    
BANNED_USERS = filters.user()

class Config:

    API_ID = int(os.getenv("API_ID", "24168862"))
    API_HASH = os.getenv("API_HASH", "916a9424dd1e58ab7955001ccc0172b3")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7887939438:AAGOEqFr0zC1c6MbYYmT13idY2THTmtfzx4")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "RoseXTaggerBot")
    BOT_NAME = os.getenv("BOT_NAME", "𝐑𝐨𝐬𝐞")
    OWNER_ID = int(os.getenv("OWNER_ID", "7426096650"))
    OWNER_NAME = os.getenv("OWNER_NAME", "AxtarmaTagYoxdu")
    GONDERME_TURU = os.getenv("GONDERME_TURU", "False").lower() == "true"
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://agautevdragitevsvh:pJSptT6jE0pcw9a4@cluster0.de4uc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1003666475868"))
    PLAYLIST_NAME = os.getenv("PLAYLIST_NAME", "SongAzPlayList")
    PLAYLIST_ID = int(os.getenv("PLAYLIST_ID", "-1003365978180"))
    BAN_GROUP = int(os.getenv("BAN_GROUP", "-1003365978180"))
    HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "HRKU-AAdPH7_nWkFVf8RyVBkkCjtONJc7sbRbCacmP7eUTOcA_____wOZSRzZHeuk")
    HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "xmusic")
    ALIVE_NAME = os.getenv("ALIVE_NAME", "𝐑𝐨𝐬𝐞")
    CHANNEL = os.getenv("CHANNEL", "RoseRobotlar")
    SUPPORT = os.getenv("SUPPORT", "botlarreklamqrupu")
    ALIVE_IMG = os.getenv("ALIVE_IMG", "https://files.catbox.moe/ilzsce.jpg")
    START_IMG = os.getenv("START_IMG", "https://files.catbox.moe/ilzsce.jpg")
    COMMAND_PREFIXES = os.getenv("COMMAND_PREFIXES", "/ ! .").split()
