from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ Qrupa əlavə et", url="https://t.me/UzeyirMusic_Bot?startgroup=true")
        ],
        [
            InlineKeyboardButton("🔮 Yeniliklər", url="https://t.me/Neptun_Sohbet1"),
            InlineKeyboardButton("🧑🏼‍🔧 Dəstək", url="https://t.me/Neptun_Sohbet")
        ],
        [
            InlineKeyboardButton("💡 Komandalar", callback_data="cbhelp")
        ]
    ]
)


help_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ Qrupa əlavə et", url="https://t.me/UzeyirMusic_Bot?startgroup=true")
        ]
    ]
)


help_cb_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕Qrupa əlavə et", url="https://t.me/UzeyirMusic_Bot?startgroup=true")
        ],
        [
            InlineKeyboardButton("🔙 Geri", callback_data="cbstart")
        ]
    ]
)


group_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔮 Yeniliklər", url="https://t.me/Neptun_Sohbet1"),
            InlineKeyboardButton("🧑🏼‍🔧 Dəstək", url="https://t.me/Neptun_Sohbet")
        ]
    ]
)


def song_markup(videoid, user_id):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🎵 Yüklə", callback_data=f"download {videoid}|{user_id}"),
                InlineKeyboardButton(text="🔐 Bağla", callback_data=f"close {user_id}")
            ]
        ]
    )
    return buttons


channel_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🎧 PlayList", url="https://t.me/UzeyirPlaylist"),
        ]
    ]
)
