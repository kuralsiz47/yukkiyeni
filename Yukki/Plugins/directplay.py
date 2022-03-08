import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)
from youtube_search import YoutubeSearch

import Yukki
from Yukki import (BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN,
                   MUSIC_BOT_NAME, app, db_mem)
from Yukki.Core.PyTgCalls.Converter import convert
from Yukki.Core.PyTgCalls.Downloader import download
from Yukki.Core.PyTgCalls.Tgdownloader import telegram_download
from Yukki.Database import (get_active_video_chats, get_video_limit,
                            is_active_video_chat)
from Yukki.Decorators.assistant import AssistantAdd
from Yukki.Decorators.checker import checker
from Yukki.Decorators.logger import logging
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (livestream_markup, playlist_markup, search_markup,
                          search_markup2, url_markup, url_markup2)
from Yukki.Utilities.changers import seconds_to_min, time_to_seconds
from Yukki.Utilities.chat import specialfont_to_normal
from Yukki.Utilities.stream import start_stream, start_stream_audio
from Yukki.Utilities.theme import check_theme
from Yukki.Utilities.thumbnails import gen_thumb
from Yukki.Utilities.url import get_url
from Yukki.Utilities.videostream import start_stream_video
from Yukki.Utilities.youtube import (get_yt_info_id, get_yt_info_query,
                                     get_yt_info_query_slider)

from Yukki.Plugins.custom.func import mplay_stream, vplay_stream

@app.on_message(
    filters.command(["oynat", f"oynat@{BOT_USERNAME}"]) & filters.group
)
@checker
@logging
@PermissionCheck
@AssistantAdd
async def mplayaa(_, message: Message):    
    await message.delete()
    if message.chat.id not in db_mem:
        db_mem[message.chat.id] = {}
    if message.sender_chat:
        return await message.reply_text(
            "Hey__Anonim yönetici__ bu Sohbet Grubunda!\nYönetici Haklarından Kullanıcı Hesabına Geri Dön."
        )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        mystic = await message.reply_text(
            "🔄 **Ses İşleniyor... Lütfen bekleyin!**"
        )
        try:
            read = db_mem[message.chat.id]["live_check"]
            if read:
                return await mystic.edit(
                    "Canlı Yayın Oynatıyor... Müzik çalmak için durdurun"
                )
            else:
                pass
        except:
            pass
        if audio.file_size > 1073741824:
            return await mystic.edit_text(
                "Ses Dosyası Boyutu 150 MB'den Az Olmalıdır"
            )
        duration_min = seconds_to_min(audio.duration)
        duration_sec = audio.duration
        if (audio.duration) > DURATION_LIMIT:
            return await mystic.edit_text(
                f"**Süre Sınırı Aşıldı**\n\n**İzin Verilen Süre: **{DURATION_LIMIT_MIN} minute(s)\n**Alınan Süre:** {duration_min} minute(s)"
            )
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file_name = path.join(path.realpath("downloads"), file_name)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(file_name))
            else file_name,
        )
        return await start_stream_audio(
            message,
            file,
            "smex1",
            "Telegram ile Verilen Ses",
            duration_min,
            duration_sec,
            mystic,
        )
    elif video:
        return await message.reply_text("Kullan /play veya /izle sesli sohbette video dosyalarını oynatma komutları bunlardır.")
    elif url:
        mystic = await message.reply_text("🔄 URL işleniyor... Lütfen bekleyin!")
        if not message.reply_to_message:
            query = message.text.split(None, 1)[1]
        else:
            query = message.reply_to_message.text
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
            views, 
            channel
        ) = get_yt_info_query(query)
        await mystic.delete()        
        MusicData = f"MusicStream {videoid}|{duration_min}|{message.from_user.id}"
        return await mplay_stream(message,MusicData)
    else:
        if len(message.command) < 2:
            buttons = playlist_markup(
                message.from_user.first_name, message.from_user.id, "abcd"
            )
            await message.reply_photo(
                photo="Utils/Playlist.jpg",
                caption=(
                    "**Kuklan:** /play [Müzik Adı veya Youtube Bağlantısı veya Sese Yanıt]\n\nÇalma Listelerini çalmak istiyorsanız! Aşağıdakilerden birini seçin."
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        mystic = await message.reply_text("🔍 **Sizin için arıyorum**...")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
            views, 
            channel
        ) = get_yt_info_query(query)
        await mystic.delete()
        MusicData = f"MusicStream {videoid}|{duration_min}|{message.from_user.id}"
        return await mplay_stream(message,MusicData)


@app.on_message(
    filters.command(["izle", f"izle@{BOT_USERNAME}"]) & filters.group
)
@checker
@logging
@PermissionCheck
@AssistantAdd
async def vplayaaa(_, message: Message):
    await message.delete()
    if message.chat.id not in db_mem:
        db_mem[message.chat.id] = {}
    if message.sender_chat:
        return await message.reply_text(
            "You're an __Anonymous Admin__ in this Chat Group!\nRevert back to User Account From Admin Rights."
        )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        return await message.reply_text("Kullanım /izle  sesli sohbette ses dosyalarını çalma komutları.")
    elif video:
        limit = await get_video_limit(141414)
        if not limit:
            return await message.reply_text(
                "**Görüntülü Aramalar İçin Sınır Tanımlanmadı**\n\nBot'ta İzin Verilen Maksimum Görüntülü Arama Sayısı İçin Bir Sınır Ayarlama /set_video_limit [Yalnızca Sudo Kullanıcıları]"
            )
        count = len(await get_active_video_chats())
        if int(count) == int(limit):
            if await is_active_video_chat(message.chat.id):
                pass
            else:
                return await message.reply_text(
                    "Pardon! Bot, CPU aşırı yükleme sorunları nedeniyle yalnızca sınırlı sayıda görüntülü aramaya izin verir. Diğer birçok sohbet şu anda görüntülü arama kullanıyor. Sese geçmeyi deneyin veya daha sonra yeniden deneyin"
                )
        mystic = await message.reply_text(
            "🔄 **Video İşleniyor... Lütfen bekleyin!**"
        )
        try:
            read = db_mem[message.chat.id]["live_check"]
            if read:
                return await mystic.edit(
                    "Canlı Yayın Oynatıyor... Müzik çalmak için durdurun"
                )
            else:
                pass
        except:
            pass
        file = await telegram_download(message, mystic)
        return await start_stream_video(
            message,
            file,
            "Telegram ile Verilen Video",
            mystic,
        )
    elif url:
        mystic = await message.reply_text("🔄 URL işleniyor... Lütfen bekleyin!")
        if not message.reply_to_message:
            query = message.text.split(None, 1)[1]
        else:
            query = message.reply_to_message.text
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
            views, 
            channel
        ) = get_yt_info_query(query)               
        
        VideoData = f"Choose {videoid}|{duration_min}|{message.from_user.id}"
        return await vplay_stream(message,VideoData,mystic)
    else:        
        if len(message.command) < 2:
            buttons = playlist_markup(
                message.from_user.first_name, message.from_user.id, "abcd"
            )
            await message.reply_photo(
                photo="Utils/Playlist.jpg",
                caption=(
                    "**Kullan:** /play [Müzik Adı veya Youtube Bağlantısı veya Sese Yanıt]\n\nÇalma Listelerini çalmak istiyorsanız! Aşağıdakilerden birini seçin."
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        mystic = await message.reply_text("🔄 İşleniyor... Lütfen bekleyin!")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
            views, 
            channel
        ) = get_yt_info_query(query)      
        VideoData = f"Choose {videoid}|{duration_min}|{message.from_user.id}"
        return await vplay_stream(message,VideoData,mystic)

