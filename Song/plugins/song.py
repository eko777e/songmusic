from pyrogram import filters
from pyrogram.enums import ChatType
from Song import app, loop
from Song.helpers.song import YouTubeAPI
from database import add_served_user, add_served_chat
from Song.helpers.inline import song_markup

ytapi = YouTubeAPI()

@app.on_message(filters.command("song") & ~filters.forwarded)
@app.on_edited_message(filters.command("song") & ~filters.forwarded)
async def command_song(client, message):
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)
        if message.sender_chat:
            return await message.reply_text(
                "❌ Siz bu qrupunda **anonim** adminsiniz\n✅ Admin hüquqlarından istifadəçi hesabına qayıdaraq, yenidən cəhd edin"
            )

    if len(message.command) < 2:
        return await message.reply_text("👀 **İstifadə**:\n\n🎧 /song (YouTube linki və yaxud musiqi adı)")

    query = " ".join(message.command[1:])
    mystic = await message.reply_text("🔍 **Musiqi axtarılır...**")

    url = get_url(query)
    if url:
        result = await loop.run_in_executor(None, get_yt_info_query, url)
    else:
        result = await loop.run_in_executor(None, get_yt_info_query, query)

    if not result:
        return await mystic.edit("❌ **Musiqi tapılmadı**")

    title, duration_min, thumb, videoid, link = result
    if str(duration_min) == "None" or duration_min == 0:
        return await mystic.edit("❌ **Canlı musiqiləri yükləmək olmur**")

    await mystic.edit("⬇️ **Musiqi yüklənir...**")

    # Musiqini yüklə
    downloaded_file, status = await ytapi.download(link, mystic, video=False)
    if not status or not downloaded_file:
        return await mystic.edit("❌ **Musiqi yüklənmədi**")

    await mystic.delete()
    buttons = song_markup(videoid, message.from_user.id)

    # Faylı göndər
    await message.reply_audio(
        audio=downloaded_file,
        title=title,
        caption=f"🎵 **Başlıq**: [{title}]({link})\n\n⏰ **Müddət**: {duration_min}\n\n🤖 **Bot:** @SongAzRobot",
        thumb=thumb,
        reply_markup=buttons
    )
