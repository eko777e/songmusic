import re, os, requests, asyncio
from yt_dlp import YoutubeDL
from eyed3 import load
from eyed3.id3.frames import ImageFrame
from youtube_search import YoutubeSearch

# Heroku üçün mütləq /tmp istifadə olunur
ydl_opts = {
    "format": "bestaudio/best",
    "cookiefile": "music.txt",  # Əgər həqiqətən lazımdırsa
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "outtmpl": "/tmp/%(id)s.%(ext)s",
    "geo_bypass": True,
    "nocheckcertificate": True,
    "quiet": True,
    "no_warnings": True,
}


def get_url(query):
    if query.startswith("https://you") or query.startswith("https://www.you"):
        if "watch" in query:
            return query
        else:
            return re.sub(r'\?.*', '', query) if "?" in query else query
    return None


def get_yt_info_query(query: str):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        return None
    result = results[0]
    videoid = result.get("id")
    if not videoid:
        return None
    title = result.get("title", "Bilinməyən ad")
    duration_min = result.get("duration", "0:00")
    thumbnail = result["thumbnails"][0].split("?")[0]
    link = f"https://youtu.be/{videoid}"
    return title, duration_min, thumbnail, videoid, link


def youtube_search(link):
    results = YoutubeSearch(link, max_results=1).to_dict()
    if not results:
        return "Bilinməyən ad", "Bilinməyən ad", "Bilinməyən kanal", "0:00", "bot.jpg"
    title = results[0].get("title", "Bilinməyən ad")
    name = re.sub(r"\W+", " ", title)
    artist = results[0].get("channel", "Bilinməyən kanal")
    duration_min = results[0].get("duration", "0:00")
    thumbnail = results[0]["thumbnails"][0].split("?")[0]
    return title, name, artist, duration_min, thumbnail


def download_song(link, name):
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        filename = ydl.prepare_filename(info)
        # MP3 faylını /tmp-ə köçür
        audio_file = f"/tmp/{name}.mp3"
        possible_files = [
            filename.replace(".webm", ".mp3"),
            filename.replace(".m4a", ".mp3"),
            filename.replace(".mp4", ".mp3"),
        ]
        for f in possible_files:
            if os.path.exists(f):
                os.rename(f, audio_file)
                break
        return audio_file


def download_thumbnail(name, thumbnail):
    try:
        thumb_name = f"/tmp/{name}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        with open(thumb_name, "wb") as file:
            file.write(thumb.content)
    except:
        thumb_name = "/tmp/bot.jpg"
    return thumb_name


def add_metadata(audio_file, title, artist, thumb_name):
    audio = load(audio_file)
    if audio.tag is None:
        audio.initTag()
    audio.tag.title = title
    audio.tag.artist = artist
    audio.tag.album = title
    with open(thumb_name, "rb") as img_file:
        img_data = img_file.read()
        audio.tag.images.set(ImageFrame.FRONT_COVER, img_data, "image/jpeg")
    audio.tag.save()


def remove_files(audio_file, thumb_name):
    if os.path.exists(audio_file):
        os.remove(audio_file)
    if thumb_name.endswith(".jpg") and os.path.exists(thumb_name):
        os.remove(thumb_name)
