from pyrogram import filters
from Song import app, loop
from Song.helpers.song import get_url, get_yt_info_query
from Song.helpers.inline import song_markup


@app.on_message(filters.text & filters.private & ~filters.command("song") & ~filters.forwarded)
@app.on_edited_message(filters.text & filters.private & ~filters.command("song") & ~filters.forwarded)
async def text_song(client, message):
    if message.text.startswith("/"):
        return
    query = message.text
    url = get_url(query)
    if url:
        if is_tiktok_url(url) or is_instagram_url(url):
            loading = await message.reply_text("📥 **Video yüklənir...**")
            path = await loop.run_in_executor(None, download_social_video, url)
            if not path:
                return await loading.edit("❌ Bu video deyil.\n✅ Yalnız TikTok və Instagram videoları yükləyə bilirəm")
            await loading.delete()
            return await message.reply_video(video=path, caption="✅Budur\n Video uğurla yükləndi.")
        if is_youtube_url(url):
            mystic = await message.reply_text("🔍 **Musiqi axtarılır...**")
            result = await loop.run_in_executor(None, get_yt_info_query, url)
            if not result:
                return await mystic.edit("❌ **Musiqi tapılmadı**")
            title, duration_min, thumb, videoid, link = result
            if str(duration_min) == "None" or duration_min == 0:
                return await mystic.edit("❌ **Canlı musiqiləri yükləmək olmur**")
            await mystic.delete()
            buttons = song_markup(videoid, message.from_user.id)
            return await message.reply_photo(photo=thumb, caption=f"🎵 **Başlıq**: [{title}]({link})\n\n⏰ **Müddət**: {duration_min}\n\n🤖 **Bot:** @SongAzRobot", reply_markup=buttons)
        return await message.reply_text("❌ **Bu link dəstəklənmir.**")
    mystic = await message.reply_text("🔍 **Musiqi axtarılır...**")
    result = await loop.run_in_executor(None, get_yt_info_query, query)
    if not result:
        return await mystic.edit("❌ **Musiqi tapılmadı**")
    title, duration_min, thumb, videoid, link = result
    if str(duration_min) == "None" or duration_min == 0:
        return await mystic.edit("❌ **Canlı musiqiləri yükləmək olmur**")
    await mystic.delete()
    buttons = song_markup(videoid, message.from_user.id)
    return await message.reply_photo(photo=thumb, caption=f"🎵 **Başlıq**: [{title}]({link})\n\n⏰ **Müddət**: {duration_min}\n\n🤖 **Bot:** @SongAzRobot", reply_markup=buttons)
