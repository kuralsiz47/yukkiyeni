import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import LOG_SESSION, OWNER_ID, SUDO_USERS
from Yukki import BOT_ID, BOT_USERNAME, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Yukki.Database import (add_gban_user, add_off, add_on, add_sudo,
                            get_active_chats, get_served_chats, get_sudoers,
                            is_gbanned_user, remove_active_chat,
                            remove_gban_user, remove_served_chat, remove_sudo,
                            set_video_limit)

__MODULE__ = "SudoUsers"
__HELP__ = """


/sudolist 
    Bot'un sudo kullanıcı listesini kontrol edin. 


**Not:**
Only for Sudo Users. 


/addsudo [Kullanıcı adı veya Kullanıcıya yanıt verme]
- Bot'un Sudo Kullanıcılarına Kullanıcı Eklemek İçin.

/delsudo [Kullanıcı adı veya Kullanıcıya yanıt verme]
- To Remove A User from Bot's Sudo Users.

/maintenance [enable / disable]
- Etkinleştirildiğinde Bot bakım moduna geçer. Artık kimse müzik çalamaz.!

/logger [enable / disable]
- Etkinleştirildiğinde Bot, aranan sorguları günlükçü grubunda günlüğe kaydeder.

/clean
- Temp Dosyalarını ve Günlüklerini Temizle.
"""
# Sudo Kullanıcıları Ekle!


@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Kullanıcının iletisini yanıtlama veya kullanıcı adı verme/user_id."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                f"{user.mention} zaten bir SUDO kullanıcısı."
            )
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"Eklendi **{user.mention}** Sudo Kullanıcılarına."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        else:
            await message.reply_text("Failed")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            f"{message.reply_to_message.from_user.mention} zaten bir SUDO kullanıcısı."
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        await message.reply_text(
            f"Eklendi **{message.reply_to_message.from_user.mention}** Sudo Kullanıcılarına"
        )
        os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    else:
        await message.reply_text("Failed")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER_ID))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Kullanıcının iletisini yanıtlama veya kullanıcı adı verme/user_id."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id not in SUDOERS:
            return await message.reply_text(f"Bot'un Sudo'sunun bir parçası değil.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(
                f"Kaldırıldı **{user.mention}** Kaynak {MUSIC_BOT_NAME}'un Sudo."
            )
            return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        await message.reply_text(f"Yanlış bir şey oldu..")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in SUDOERS:
        return await message.reply_text(
            f"Bir parçası değil {MUSIC_BOT_NAME}'un Sudo."
        )
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(
            f"Kaldırıldı **{mention}** Kaynak {MUSIC_BOT_NAME}'un Sudo."
        )
        return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    await message.reply_text(f"Yanlış bir şey oldu..")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "⭐️<u> **Sahipler:**</u>\n"
    sex = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            sex += 1
        except Exception:
            continue
        text += f"{sex}➤ {user}\n"
    smex = 0
    for count, user_id in enumerate(sudoers, 1):
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n⭐️<u> **Sudo Kullanıcıları:**</u>\n"
                sex += 1
                text += f"{sex}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("Sudo Kullanıcısı Yok")
    else:
        await message.reply_text(text)


### Video Sınırı


@app.on_message(
    filters.command(["set_video_limit", f"set_video_limit@{BOT_USERNAME}"])
    & filters.user(SUDOERS)
)
async def set_video_limit_kid(_, message: Message):
    if len(message.command) != 2:
        usage = "**Kullanım:**\n/set_video_limit [İzin verilen sohbet sayısı]"
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    try:
        limit = int(state)
    except:
        return await message.reply_text(
            "Sınırı Ayarlamak İçin Lütfen Sayısal Sayılar Kullanın."
        )
    await set_video_limit(141414, limit)
    await message.reply_text(
        f"Video Aramaları En Fazla Tanımlı Sınırı {limit} Sohbet."
    )


## Bakım Yukki


@app.on_message(filters.command("maintenance") & filters.user(SUDOERS))
async def maintenance(_, message):
    usage = "**Kullanım:**\n/maintenance [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("Bakım için Etkinleştirildi")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("Bakım Modu Devre Dışı")
    else:
        await message.reply_text(usage)


## Günlükçü


@app.on_message(filters.command("logger") & filters.user(SUDOERS))
async def logger(_, message):
    if LOG_SESSION == "None":
        return await message.reply_text(
            "Günlükçü Hesabı Tanımlanmadı.\n\nPlease Seti <code>LOG_SESSION</code> var ve sonra günlüğe kaydetmeyi deneyin."
        )
    usage = "**Kullanım:**\n/logger [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 5
        await add_on(user_id)
        await message.reply_text("Etkin Günlüğe Kaydetme")
    elif state == "disable":
        user_id = 5
        await add_off(user_id)
        await message.reply_text("Günlüğe Kaydetme Devre Dışı")
    else:
        await message.reply_text(usage)


## Gban Modülü


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**Kullanım:**\n/gban [KULLANICI ADI | USER_ID]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "Kendini gban mı istiyorsun? Ne Kadar Aptalca!"
            )
        elif user.id == BOT_ID:
            await message.reply_text("Kendimi engellemeli miyim? Şaka gibi!")
        elif user.id in SUDOERS:
            await message.reply_text("Sudo kullanıcısını engellemek mi istiyorsunuz? Reis")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Küresel Yasaklamayı Başlat {user.mention}**\n\nBeklenen Süre : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Yeni Küresel Yasak {MUSIC_BOT_NAME}**__

**Köken:** {message.chat.title} [`{message.chat.id}`]
**Sudo Kullanıcısı:** {from_user.mention}
**Yasaklı Kullanıcı:** {user.mention}
**Yasaklanmış Kullanıcı Kimliği:** `{user.id}`
**Sohbet:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Kendini engellemek mi istiyorsun? Ne Kadar Aptalca!")
    elif user_id == BOT_ID:
        await message.reply_text("Kendimi engellemeli miyim? Şaka gibi..")
    elif user_id in sudoers:
        await message.reply_text("Sudo kullanıcısını engellemek mi istiyorsunuz? Reis..")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("Zaten Gbanned.")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Global Yasağını Başlatmak {mention}**\n\nBeklenen Süre : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Yeni Küresel Yasak {MUSIC_BOT_NAME}**__

**Köken:** {message.chat.title} [`{message.chat.id}`]
**Sudo Kullanıcısı:** {from_user_mention}
**Yasaklı Kullanıcı:** {mention}
**Yasaklanmış Kullanıcı Kimliği:** `{user_id}`
**Sohbet:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**Kullanım:**\n/ungban [KULLANICI ADI | USER_ID]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("Engelini kaldırmak istiyorsun.?")
        elif user.id == BOT_ID:
            await message.reply_text("Engelimi kaldırmalı mıyım??")
        elif user.id in sudoers:
            await message.reply_text("Sudo kullanıcıları engellenemiyor/unblocked.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("O zaten özgür, neden ona ban atalım ki?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"Ungbanned!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Engelini kaldırmak istiyorsun.?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Engelimi kaldırmalı mıyım? Ama engellenmedim.."
        )
    elif user_id in sudoers:
        await message.reply_text("Sudo kullanıcıları engellenemiyor..engellenemiyor.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("O zaten özgür, neden banlayayım?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"Ungbanned!")


# Yayın İletisi


@app.on_message(filters.command("broadcast_pin") & filters.user(SUDOERS))
async def broadcast_message_pin_silent(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**Yayınlanan İleti {sent}  Sohbetler {pin} Pins.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/broadcast [İLETİ] veya [İletiyi Yanıtlama]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Yayınlanan İleti {sent} Sohbetler ve {pin} Pins.**"
    )


@app.on_message(filters.command("broadcast_pin_loud") & filters.user(SUDOERS))
async def broadcast_message_pin_loud(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**Yayınlanan İleti {sent}  Sohbetler {pin} Pins.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/broadcast [İLETİ] veya [İletiyi Yanıtlama]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Yayınlanan İleti İçinde {sent} Sohbetler ve {pin} Pins.**"
    )


@app.on_message(filters.command("reklam") & filters.user(SUDOERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"**Yayınlanan İleti {sent} Sohbetler.**")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/reklam [İLETİ] veya [İletiyi Yanıtlama]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"**Yayınlanan İleti {sent} Sohbetler.**")


# Temizlik


@app.on_message(filters.command("clean") & filters.user(SUDOERS))
async def clean(_, message):
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await message.reply_text("Tümü başarıyla temizlendi **Temp** dir(s)!")
