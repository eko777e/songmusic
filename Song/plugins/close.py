from pyrogram import filters
from Song import app


@app.on_callback_query(filters.regex("close"))
async def forceclose(client, query):
    callback_data = query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    user_id = callback_request
    if query.from_user.id != int(user_id):
        return await query.answer("🤷🏻 **Bunu bağlamağ üçün icazən yoxdur.**", show_alert=True)
    await query.message.delete()
