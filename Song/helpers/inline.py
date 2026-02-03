from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ Qrupa əlavə et", url="https://t.me/SongAzRobot?startgroup=true")
        ],
        [
            InlineKeyboardButton("🔮 Yeniliklər", url="https://t.me/BotAzNews"),
            InlineKeyboardButton("🧑🏼‍🔧 Dəstək", url="https://t.me/DestekAz")
        ],
        [
            InlineKeyboardButton("📚 Komandalar", callback_data="cbhelp")
        ]
    ]
)


help_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ Qrupa əlavə et", url="https://t.me/SongAzRobot?startgroup=true")
        ]
    ]
)


help_cb_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ Qrupa əlavə et", url="https://t.me/SongAzRobot?startgroup=true")
        ],
        [
            InlineKeyboardButton("🔙 Geri", callback_data="cbstart")
        ]
    ]
)


group_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔮 Yeniliklər", url="https://t.me/BotAzNews"),
            InlineKeyboardButton("🧑🏼‍🔧 Dəstək", url="https://t.me/DestekAz")
        ]
    ]
)


def song_markup(videoid, user_id):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🎧 Yüklə", callback_data=f"download {videoid}|{user_id}"),
                InlineKeyboardButton(text="🔐 Bağla", callback_data=f"close {user_id}")
            ]
        ]
    )
    return buttons


channel_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🎧 Playlist", url="https://t.me/SongPlayliste"),
        ]
    ]
)
