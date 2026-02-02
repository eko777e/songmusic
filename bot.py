import os
from pyrogram import enums, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
    Message,
)
from Song.config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT, PLAYLIST_CHANNEL, PLAYLIST_URL, BOT_USERNAME
from Song.Music.Youtube import YouTubeAPI
from Song.utils.decorators.language import language, languageCB
YouTube = YouTubeAPI()

import yt_dlp
app = Client(
    "MusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


async def search_youtube(query: str, limit: int = 10):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
        results = []
        for entry in info.get("entries", []):
            results.append({
                "title": entry.get("title"),
                "id": entry.get("id"),
                "duration": entry.get("duration"),
                "thumbnail": entry.get("thumbnail"),
            })
        return results


@app.on_message(
    filters.command(["song", "video"]) & filters.group & ~BANNED_USERS
)
@language
async def song_commad_group(client, message: Message, _):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["SG_B_1"],
                    url=f"https://t.me/RoseXTaggerBot?start=song",
                ),
            ]
        ]
    )
    await message.reply_text(_["song_1"], reply_markup=upl)

@app.on_message(
    filters.command(["musiqi"]) & filters.private & ~BANNED_USERS
)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    mystic = await message.reply_text(_["play_1"])

    if url:
        if not await YouTube.exists(url):
            return await mystic.edit_text(_["song_5"])
        try:
            title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(url)
        except:
            return await mystic.edit_text(_["play_3"])
    else:
        if len(message.command) < 2:
            return await mystic.edit_text(_["song_2"])
        query = message.text.split(None, 1)[1]
        try:
            title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
        except:
            return await mystic.edit_text(_["play_3"])

    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )

    yturl = f"https://www.youtube.com/watch?v={vidid}"
    try:
        file_path, status = await YouTube.download(
            yturl,
            mystic,
            songaudio=True,
            songvideo=None,
            title=None,
        )
    except Exception as e:
        return await mystic.edit_text(_["song_9"].format(e))

    if not status or not file_path:
        return await mystic.edit_text(_["song_10"])

    thumb_image_path = await client.download_media(thumbnail)
    duration = duration_sec

    med = InputMediaAudio(
        media=file_path,
        caption=f"🎵 Başlıq: {title}\n\n🤖 Bot: @SongAzRobot",
        thumb=thumb_image_path,
        title=title,
        performer="@SongAzRobot"
    )
    await mystic.edit_text(_["song_11"])
    await app.send_chat_action(
        chat_id=message.chat.id,
        action=enums.ChatAction.UPLOAD_AUDIO,
    )
    try:
        await message.reply_media_group([med])
    except Exception:
        return await mystic.edit_text(_["song_10"])
    os.remove(file_path)


@app.on_message(
    filters.command(["musiq", "video"]) & filters.private & ~BANNED_USERS
)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
            )
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎵 Audio",
                    callback_data=f"song_download audio|{vidid}",
                ),
                InlineKeyboardButton(
                    text="🎬 Video",
                    callback_data=f"song_download video|{vidid}",
                ),
            ]
        ]
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])
    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 Audio",
                callback_data=f"song_download audio|{vidid}",
            ),
            InlineKeyboardButton(
                text="🎬 Video",
                callback_data=f"song_download video|{vidid}",
            ),
        ]
    ]
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    
@app.on_message(
    filters.command(["song"]) & filters.private & ~BANNED_USERS
)
@language
async def song_search_results(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(_["song_2"])
    
    query = message.text.split(None, 1)[1]
    mystic = await message.reply_text(_["play_1"])
    
    try:
        results = await search_youtube(query, limit=10)
    except Exception as e:
        return await mystic.edit_text(_["play_3"] + f"\n\nError: {e}")
    
    if not results:
        return await mystic.edit_text(_["song_5"])
    
    # Mətn hissəsi: 1. Musiqi adı, 2. Musiqi adı...
    text_lines = []
    buttons = []
    row = []
    for idx, result in enumerate(results, start=1):
        text_lines.append(f"{idx}. {result['title']}")
        row.append(
            InlineKeyboardButton(
                text=str(idx),
                callback_data=f"song_choose {result['id']}"
            )
        )
        # hər 5 düymədən sonra yeni sətir
        if len(row) == 5:
            buttons.append(row)
            row = []
    # qalıq düymələr varsa əlavə et
    if row:
        buttons.append(row)
    
    await mystic.delete()
    return await message.reply_text(
        "\n".join(text_lines),
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@app.on_callback_query(filters.regex(pattern=r"song_choose") & ~BANNED_USERS)
@languageCB
async def song_choose_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Seçildi...")
    except:
        pass
    
    vidid = CallbackQuery.data.split(None, 1)[1]
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    
    mystic = await CallbackQuery.edit_message_text(_["play_2"])
    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(yturl)
    except:
        return await mystic.edit_text(_["play_3"])
    
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )
    
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 Audio",
                callback_data=f"song_download audio|{vidid}",
            ),
            InlineKeyboardButton(
                text="🎬 Video",
                callback_data=f"song_download video|{vidid}",
            ),
        ]
    ]
    await mystic.delete()
    return await CallbackQuery.message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@app.on_callback_query(filters.regex(pattern=r"song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Yüklənir..")
    except:
        pass

    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    try:
        file_path, status = await YouTube.download(
            yturl,
            mystic,
            songaudio=True if stype == "audio" else None,
            songvideo=True if stype == "video" else None,
            title=None,
        )
    except Exception as e:
        return await mystic.edit_text(_["song_9"].format(e))

    if not status or not file_path:
        return await mystic.edit_text(_["song_10"])

    title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(yturl)
    thumb_image_path = await CallbackQuery.message.download()

    if stype == "video":
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_VIDEO,
        )
        try:
            # İstifadəçiyə göndər
            await app.send_video(
                chat_id=CallbackQuery.message.chat.id,
                video=file_path,
                caption=title,
                thumb=thumb_image_path,
                supports_streaming=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🎧 Playlist", url=PLAYLIST_URL)]]
                )
            )
            # Playlist kanalına göndər
            await app.send_video(
                chat_id=PLAYLIST_CHANNEL,
                video=file_path,
                caption=title,
                thumb=thumb_image_path,
                supports_streaming=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("➕ Məni qrupa əlavə et", url=f"https://t.me/{BOT_USERNAME}?start=group")]]
                )
            )
        except Exception as e:
            return await mystic.edit_text(_["song_10"] + f"\n\nError: {e}")
        os.remove(file_path)

    elif stype == "audio":
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_AUDIO,
        )
        try:
            # İstifadəçiyə göndər
            await app.send_audio(
                chat_id=CallbackQuery.message.chat.id,
                audio=file_path,
                caption=f"🎵 Başlıq: {title}\n\n🤖 Bot: @{BOT_USERNAME}",
                thumb=thumb_image_path,
                title=title,
                performer=f"@{BOT_USERNAME}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🎧 Playlist", url=PLAYLIST_URL)]]
                )
            )
            # Playlist kanalına göndər
            await app.send_audio(
                chat_id=PLAYLIST_CHANNEL,
                audio=file_path,
                caption=f"🎵 Başlıq: {title}\n\n🤖 Bot: @{BOT_USERNAME}",
                thumb=thumb_image_path,
                title=title,
                performer=f"@{BOT_USERNAME}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("➕ Məni qrupa əlavə et", url=f"https://t.me/{BOT_USERNAME}?start=group")]]
                )
            )
            await mystic.delete()
        except Exception as e:
            return await mystic.edit_text(_["song_10"] + f"\n\nError: {e}")
        os.remove(file_path)

app.run()
