from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕Qrupa əlavə et", url="https://t.me/UzeyirMusic_Bot?startgroup=true")
        ],
        [
            InlineKeyboardButton("Kanal", url="https://t.me/Neptun_Sohbet1"),
            InlineKeyboardButton("🆘Kömək", url="https://t.me/Neptun_Sohbet")
        ],
        [
            InlineKeyboardButton("💡Əmrlər", callback_data="cbhelp")
        ]
    ]
)


help_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕Qrupa əlavə et", url="https://t.me/UzeyirMusic_Bot?startgroup=true")
        ],
        [
            InlineKeyboardButton("Kanal", url="https://t.me/Neptun_Sohbet1"),
            InlineKeyboardButton("🆘Kömək", url="https://t.me/Neptun_Sohbet")
        ]
    ]
)


help_cb_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕Qrupa əlavə et", url="https://t.me/UzeyirMusic_Bot?startgroup=true")
        ],
        [
            InlineKeyboardButton("Kanal", url="https://t.me/Neptun_Sohbet1"),
            InlineKeyboardButton("🆘Kömək", url="https://t.me/Neptun_Sohbet")
        ],
        [
            InlineKeyboardButton("🔙Geri", callback_data="cbstart")
        ]
    ]
)


group_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Kanal", url="https://t.me/Neptun_Sohbet1"),
            InlineKeyboardButton("🆘Kömək", url="https://t.me/Neptun_Sohbet")
        ]
    ]
)


def song_markup(videoid, user_id):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🎵Yüklə", callback_data=f"download {videoid}|{user_id}"),
                InlineKeyboardButton(text="❌Bağla", callback_data=f"close {user_id}")
            ]
        ]
    )
    return buttons


channel_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🎵PlayList", url="https://t.me/UzeyirPlaylist"),
        ]
    ]
)
