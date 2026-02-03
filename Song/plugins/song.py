from pyrogram import filters
from pyrogram.enums import ChatType
from Song import app, loop
from Song.helpers.song import get_url, get_yt_info_query
from database import add_served_user, add_served_chat
from Song.helpers.inline import song_markup


@app.on_message(filters.command("song") & ~filters.forwarded)
@app.on_edited_message(filters.command("song") & ~filters.forwarded)
async def command_song(client, message):
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)
        if message.sender_chat:
            return await message.reply_text("❌ Siz bu qrupunda **anonim** adminsiniz\n✅ Admin hüquqlarından istifadəçi hesabına qayıdaraq, yenidən cəhd edin")
    if len(message.command) < 2:
        return await message.reply_text("👀 **İstifadə**:\n\n🎧 /song (YouTube linki və yaxud musiqi adı)")
    query = " ".join(message.command[1:])
    mystic = await message.reply_text("🔍 **Musiqi axtarılır...**")
    url = get_url(query)
    if url:
        result = await loop.run_in_executor(None, get_yt_info_query, url)
        if result:
            title, duration_min, thumb, videoid, link = result
            if str(duration_min) == "None" or duration_min == 0:
                return await mystic.edit("❌ **Canlı musiqiləri yükləmək olmur**")
            await mystic.delete()
            buttons = song_markup(videoid, message.from_user.id)
            return await message.reply_photo(photo=thumb, caption=f"🎵 **Başlıq**: [{title}]({link})\n\n⏰ **Müddət**: {duration_min}\n\n🤖 **Bot:** @SongAzRobot", reply_markup=buttons)
        else:
            return await mystic.edit("❌ **Musiqi tapılmadı**")
    else:
        result = await loop.run_in_executor(None, get_yt_info_query, query)
        if result:
            title, duration_min, thumb, videoid, link = result
            if str(duration_min) == "None" or duration_min == 0:
                return await mystic.edit("❌ **Canlı musiqiləri yükləmək olmur**")
            await mystic.delete()
            buttons = song_markup(videoid, message.from_user.id)
            return await message.reply_photo(photo=thumb, caption=f"🎵 **Başlıq**: [{title}]({link})\n\n⏰ **Müddət**: {duration_min}\n\n🤖 **Bot:** @SongAzRobot", reply_markup=buttons)
        else:
            return await mystic.edit("❌ **Musiqi tapılmadı**")
