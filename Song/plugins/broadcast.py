import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from Song import app
from config import OWNER_ID, BOT_ID
from database import get_served_chats, add_served_chat, get_served_users, add_served_user, remove_served_chat, remove_served_user, add_premium, get_premium, remove_premium
from Song.helpers.broadcast import errors_chats, errors_users, send_errors, extract_chat_ids, extract_user_ids, remove_errors


@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    return await message.reply(f"**⚡Məlumatlar:**\n**👥Qruplar:** {served_chats}\n**👤İstifadəçilər:** {served_users}")


@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_message(client, message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("🔥Reklama hazıram...")
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if "-chat" in query:
            query = query.replace("-chat", "")
    await message.reply_text("⏳Reklam prosesi başladı")
    if "-chat" in message.text:
        sent_chats = 0
        pin = 0
        chats = []
        premium = []
        pre = await get_premium()
        for chat in pre:
            premium.append(int(chat["chat_id"]))
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            if i in premium:
                continue
            try:
                if message.reply_to_message:
                    m = await app.forward_messages(i, y, x)
                else:
                    m = await app.send_message(i, text=query)
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        continue
                sent_chats += 1
                await asyncio.sleep(1)
            except FloodWait as fw:
                flood_time = int(fw.x)
                await asyncio.sleep(flood_time)
            except Exception as e:
                errors_chats(i, str(e))
                continue
        await message.reply_text(f"👥{sent_chats} qrupa {pin} sabitləmə ilə göndərildi")
        await send_errors(client, "errors_chats.txt", message.chat.id)
    if "-user" in message.text:
        sent_users = 0
        users = []
        susers = await get_served_users()
        for user in susers:
            users.append(int(user["user_id"]))
        for i in users:
            try:
                if message.reply_to_message:
                    m = await app.forward_messages(i, y, x)
                else:
                    m = await app.send_message(i, text=query)
                sent_users += 1
                await asyncio.sleep(1)
            except FloodWait as fw:
                flood_time = int(fw.x)
                await asyncio.sleep(flood_time)
            except Exception as e:
                errors_users(i, str(e))
                continue
        await message.reply_text(f"👤{sent_users} istifadəçiyə göndərildi")
        await send_errors(client, "errors_users.txt", message.chat.id)
    return await message.reply_text("✅Reklam prosesi bitdi")


@app.on_message(filters.command("delete_id") & filters.user(OWNER_ID))
async def delete_ids(client, message):
    if message.reply_to_message and message.reply_to_message.document:
        file_path = await message.reply_to_message.download()
    else:
        if len(message.command) < 2:
            return await message.reply_text("🔥Hazıram...")
        query = message.text.split(None, 1)[1]
        if "-user" in query:
            query = query.replace("-user", "")
        if "-chat" in query:
            query = query.replace("-chat", "")
        return await message.reply_text("🔗Fayla cavab verin")
    await message.reply_text("⏳Silmə prosesi başladı")
    if "-chat" in message.text:
        id_list = extract_chat_ids(file_path)
        deleted_count = 0
        for id in id_list:
            deleted = await remove_served_chat(id)
            if deleted:
                deleted_count += 1
        remove_errors(file_path, "errors_chats.txt")
        return await message.reply_text(f"✅Fayldan {deleted_count} chat silindi")
    if "-user" in message.text:
        id_list = extract_user_ids(file_path)
        deleted_count = 0
        for id in id_list:
            deleted = await remove_served_user(id)
            if deleted:
                deleted_count += 1
        remove_errors(file_path, "errors_users.txt")
        return await message.reply_text(f"✅Fayldan {deleted_count} user silindi")


@app.on_message(filters.command("premium") & filters.group & filters.user(OWNER_ID))
async def premium_add(client, message):
    added = await add_premium(message.chat.id)
    if added:
        return await message.reply_text("⭐Bu qrup, premium qruplar siyahısına əlavə edildi")
    else:
        return await message.reply_text("❌Bu qrup, zatən premium qruplar siyahısında var")


@app.on_message(filters.command("del_premium_id") & filters.private & filters.user(OWNER_ID))
async def premium_remove_id(client, message):
    chat_id = int(message.text.split()[1])
    deleted = await remove_premium(chat_id)
    if deleted:
        return await message.reply_text(f"✅ `{chat_id}` premium qruplar siyahısından silindi")
    else:
        return await message.reply_text(f"❌ `{chat_id}` premium qruplar siyahısında yoxdur")


@app.on_message(filters.command("get_premium") & filters.private & filters.user(OWNER_ID))
async def premium_get(client, message):
    premium_chats = await get_premium()
    if premium_chats:
        response_text = "⭐Premium qruplar:\n"
        for index, chat in enumerate(premium_chats, 1):
            chat_info = await app.get_chat(chat['chat_id'])
            chat_name = chat_info.title
            response_text += f"{index}. `{chat['chat_id']}` => {chat_name}\n"
        return await message.reply_text(response_text)
    else:
        return await message.reply_text("❌Premium qrup yoxdur")


@app.on_message(filters.command("get_premium_id") & filters.private & filters.user(OWNER_ID))
async def premium_get_id(client, message):
    premium_chats = await get_premium()
    if premium_chats:
        response_text = "⭐Premium qruplar:\n"
        for index, chat in enumerate(premium_chats, 1):
            response_text += f"{index}. `{chat['chat_id']}`\n"
        return await message.reply_text(response_text)
    else:
        return await message.reply_text("❌Premium qrup yoxdur")


@app.on_message(filters.command("del_premium") & filters.group & filters.user(OWNER_ID))
async def premium_remove(client, message):
    deleted = await remove_premium(message.chat.id)
    if deleted:
        return await message.reply_text(f"✅Bu qrup, premium qruplar siyahısından silindi")
    else:
        return await message.reply_text(f"❌Bu qrup, premium qruplar siyahısında yoxdur")


@app.on_message(filters.command("test") & filters.private  & filters.user(BOT_ID))
async def test_private(client, message):
    return await add_served_user(message.chat.id)
