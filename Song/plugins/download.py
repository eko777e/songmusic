from pyrogram import filters
from pyrogram.enums import ChatAction
from Song import app, loop
from Song.helpers.song import youtube_search, download_thumbnail, download_song, add_metadata, remove_files
from config import OWNER_ID, LOG_GROUP_ID, PLAYLIST_ID
from database import check
from Song.helpers.inline import channel_markup


@app.on_callback_query(filters.regex("download"))
async def download_cb(client, query):
    callback_data = query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if query.from_user.id != int(user_id):
        return await query.answer("❌ **Öz musiqinizi axtarın, bu düymədən istifadə etməyə icazəniz yoxdur**", show_alert=True)
    link = f"https://youtu.be/{videoid}"
    await query.message.delete()
    title, name, artist, duration_min, thumbnail = await loop.run_in_executor(None, youtube_search, link)
    thumb_name = await loop.run_in_executor(None, download_thumbnail, name, thumbnail)
    if str(duration_min) == "None" or duration_min == 0:
        return await app.send_message(chat_id=query.message.chat.id, text="❌ **Canlı musiqiləri yükləmək olmur**")
    m = await app.send_message(chat_id=query.message.chat.id, text="🎵 **Musiqi yüklənilir...**")
    audio_file = await loop.run_in_executor(None, download_song, link, name)
    duration_seconds = int(duration_min.split(':')[0]) * 60 + int(duration_min.split(':')[1])
    await m.edit("🎧 **Musiqi sizə göndərilir...**")
    await app.send_chat_action(chat_id=query.message.chat.id, action=ChatAction.UPLOAD_AUDIO)
    add_metadata(audio_file, title, artist, thumb_name)
    await app.send_audio(chat_id=query.message.chat.id, audio=audio_file, performer="@SongAzRobot", thumb=thumb_name, duration=duration_seconds, caption=f"🎵 **Başlıq:** [{title}]({link})\n\n🤖 **Bot:** @SongAzRobot", reply_markup=channel_markup)
    await m.delete()
    await app.send_message(chat_id=LOG_GROUP_ID, text=f"👤 {query.from_user.mention}, `{title}` musiqisini yüklədi.")
    share = await check(title)
    if share:
        await app.send_audio(chat_id=PLAYLIST_ID, audio=audio_file, performer="@SongAzRobot", thumb=thumb_name, duration=duration_seconds, caption=f"🎵 **Başlıq:** [{title}]({link})\n\n🤖 **Bot:** @SongAzRobot")
    remove_files(audio_file, thumb_name)
