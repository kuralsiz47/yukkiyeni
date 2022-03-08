from config import ASSISTANT_PREFIX
from Yukki import BOT_NAME, BOT_USERNAME
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_TEXT = f"""
✨ **Merhaba MENTION !**

**Kullanabilirsiniz [{BOT_NAME}](https://t.me/{BOT_USERNAME}) Grup Görüntülü Sohbetinizde Müzik veya Video oynatmak için.**

💡 **Bot'un tüm komutlarını ve nasıl çalıştıklarını öğrenin. ➤ 📚 Komutlar düğmesi**
"""

COMMANDS_TEXT = f"""
✨ **Merhaba MENTION !**

**Komutlarımı öğrenmek için aşağıdaki düğmelere tıklayın.**
"""

START_BUTTON_GROUP = InlineKeyboardMarkup(
    [   
        [
            InlineKeyboardButton(
                text="📚 Komut", callback_data="command_menu"
            ),
            InlineKeyboardButton(
                text="🔧 Ayarlar", callback_data="settingm"
            ),                                   
        ],
        [
            InlineKeyboardButton(
                text="📣 Resmi Kanal", url="https://t.me/Sohbetdestek"
            ),
            InlineKeyboardButton(
                text="💬 Destek Grubu", url="https://t.me/BotDestekGrubu"
            ),                       
        ],        
    ]
)

START_BUTTON_PRIVATE = InlineKeyboardMarkup(
    [   [
            InlineKeyboardButton(
                text="➕ Beni Gruba Ekle ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
            ),            
        ],
        [   
            InlineKeyboardButton(
                text="📚 Komut", callback_data="command_menu"
            ),                       
        ],
        [
            InlineKeyboardButton(
                text="📣 Resmi Kanal", url="https://t.me/Sohbetdestek"
            ),
            InlineKeyboardButton(
                text="💬 Destek Grubu", url="https://t.me/BotDestekGrubu"
            ),                       
        ],        
    ]
)

COMMANDS_BUTTON_USER = InlineKeyboardMarkup(
    [   [
            InlineKeyboardButton(
                text="Yönetici Komutları", callback_data="admin_cmd"
            ),
            InlineKeyboardButton(
                text="Bot Komutları", callback_data="bot_cmd"
            ),            
        ],
        [
            InlineKeyboardButton(
                text="Komutları Yürüt", callback_data="play_cmd"
            ),            
            InlineKeyboardButton(
                text="Ek Komutlar", callback_data="extra_cmd"
            ),                                   
        ],
        [
            InlineKeyboardButton(
                text="↪️ Geri", callback_data="command_menu"
            ),
            InlineKeyboardButton(
                text="🔄 Kapat", callback_data="close_btn"
            ),            
        ],                
    ]
)

COMMANDS_BUTTON_SUDO = InlineKeyboardMarkup(
    [   [
            InlineKeyboardButton(
                text="Yönetici Komutları", callback_data="admin_cmd"
            ),
            InlineKeyboardButton(
                text="Bot Komutları", callback_data="bot_cmd"
            ),            
        ],
        [
            InlineKeyboardButton(
                text="Komutları Yürüt", callback_data="play_cmd"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Ek Komutlar", callback_data="extra_cmd"
            ),                                   
        ],
        [
            InlineKeyboardButton(
                text="↪️ Geri", callback_data="command_menu"
            ),
            InlineKeyboardButton(
                text="🔄 Kapat", callback_data="close_btn"
            ),            
        ],                
    ]
)

BACK_BUTTON = InlineKeyboardMarkup(
    [   [
            InlineKeyboardButton(
                text="↪️ Geri", callback_data="advanced_cmd"
            ),
            InlineKeyboardButton(
                text="🔄 Kapat", callback_data="close_btn"
            ),            
        ],                        
    ]
)

SUDO_BACK_BUTTON = InlineKeyboardMarkup(
    [   [
            InlineKeyboardButton(
                text="Diğer Sudo Komutları", url="https://t.me/BotDestekGrubu"
            ),                        
        ],
        [
            InlineKeyboardButton(
                text="↪️ Geri", callback_data="advanced_cmd"
            ),
            InlineKeyboardButton(
                text="🔄 Kapat", callback_data="close_btn"
            ),            
        ],                        
    ]
)


ADMIN_TEXT = f"""
İşte yardım **Yönetici Komutları:**


--**YALNIZCA SESİ YÖNETEN YÖNET KOMUTLARI:**--

/durdur 
- Sesli sohbette çalan müziği duraklatma.

/devam 
- Sesli sohbette duraklatılmış müziği sürdürme.

/atla 
- Sesli sohbette geçerli müzik çalmayı atlama

/son 
- Müzik çalmayı durdurma.


--**Yetkili Kullanıcılar Listesi:**--

**{BOT_NAME} yönetici komutlarını kullanmak isteyen yönetici olmayan kullanıcılar için ek bir özelliğe sahiptir**
- Kimlik doğrulama kullanıcıları, Yönetici Hakları olmadan bile Sesli Sohbetleri atlayabilir, duraklatabilir, durdurabilir, sürdürebilir.


/auth [Kullanıcı Adı veya İletiyi Yanıtlama] 
- Grubun AUTH LİSTESİ'ne kullanıcı ekleme.

/unauth [Kullanıcı Adı veya İletiyi Yanıtlama] 
- Kullanıcıyı grubun AUTH Listesinden kaldırma.

/authusers 
- Grubun AUTH LIST'ini denetleyin.
"""

BOT_TEXT = """
İşte yardım **Bot Komutları:**


/start 
- Müzik Bot'ını başlat.

/help 
- Komutların ayrıntılı açıklamalarını içeren Komutlar Yardımcısı Menüsünü Alıp Al.

/settings 
- Bir grubun Ayarlar panosunu alıp alın. Kimlik Doğrulama Kullanıcıları Modu'nu yönetebilirsiniz. Buradan Komut modu.

/ping
- Bot ping ve Kontrol Ram, Cpu vb Müzik Bot istatistikleri."""

PLAY_TEXT = """
İşte yardım fo **Oynat Komut:**


--**Youtube ve Telegram Dosyaları:**--

/play __[Müzik Adı]__(Bot Youtube'da arama yapacak)
/play __[Youtube Bağlantıyı veya Çalma Listesini izleme]__
/play __[Video, Canlı, M3U8 Bağlantıları]__
/play __[Ses veya Video Dosyasını Yanıtlama]__
/oynat __[Şarkıları Hızlı ve Seri Dinlemek içindir.]__
/izle ___[Görüntülü Video izlemenize olanak tanır.]__
- Elde ettiğiniz satır içi Düğmeler'i seçerek Sesli Sohbette Video veya Müzik Akışı sağlar. 


--**Çalma Listeleri:**--

/playplaylist 
- Kaydedilmiş Çalma Listenizi oynatmaya başlayın.

/playlist 
- Sunucularda Kayıtlı Çalma Listenizi Denetleme.

/delmyplaylist
- Çalma listenizdeki kaydedilmiş müzikleri silme

/delgroupplaylist
- Grubunuzun çalma listesindeki kaydedilmiş müzikleri silme [Yönetici Hakları Gerektirir.]
"""

SUDO_TEXT = f"""
İşte yardımı **Sudo Komutları:**

**<u>Sudo Kullanıcıları Ekle Kaldır:</u>**
/addsudo [Kullanıcı adı veya Kullanıcıya yanıt verme]
/delsudo [Kullanıcı adı veya Kullanıcıya yanıt verme]

**<u>Bot Komutları:</u>**
/restart - Botu Yeniden Başlat. 
/update - Bot'ı Güncelleştir.
/stats - Bot istatistiklerini kontrol edin

**<u>Kara Listeye Alma İşlemi:</u>**
/blacklistchat [CHAT_ID] - Müzik Bot kullanarak herhangi bir sohbeti kara listeye alma
/whitelistchat [CHAT_ID] - Müzik Bot'un kullanılmasından kara listeye alınan herhangi bir sohbeti beyaz listeye alma

**<u>Yayın İşlevi:</u>**
/reklam [İleti veya İletiyi Yanıtlama] - Yayın iletisi.
/broadcast_pin [İleti veya İletiyi Yanıtlama] - İletiyi pin ile yayınla [Devre Dışı Bildirimleri].
/broadcast_pin_loud [İleti veya İletiyi Yanıtlama] - İletiyi pin ile yayınla [Etkin Bildirimler].

**<u>Gban İşlevi:</u>**
/gban [Kullanıcı adı veya Kullanıcıya yanıt verme] - Bot'un Sunulan Sohbetleri'nde bir kullanıcıyı genel olarak yasaklama ve kullanıcının bot komutlarını kullanmasını engelleme.
/ungban [Kullanıcı adı veya Kullanıcıya yanıt verme] - Kullanıcıyı Bot'un GBan Listesinden kaldırma.
"""

EXTRA_TEXT = """
İşte yardım **Ek Komutlar:**


/lyrics [Müzik Adı]
- Web'de belirli bir Müzik için Şarkı Sözlerini Arar.

/sudolist 
- Music Bot'un Sudo Kullanıcılarını Kontrol Edin

/bul [Parça Adı] or [YT Bağlantısı]
- Bot üzerinden youtube'dan mp3 veya mp4 formatlarında herhangi bir parça indirin.

/queue
- Müzik Sıra Listesini Denetle.
"""

BASIC_TEXT = """
💠 **Temel Komutlar:**

/start - botu başlatmak
/help - yardım iletisi alma
/play - sesli'de şarkı veya video oynatmak url daha fazlası
/oynat - şarkıları doğrudan sesli'de çalma seri çalar.
/spotify - spotify'dan şarkı çalmak
/resso - resso'dan şarkı çalmak
/lyrics - şarkının sözlerini almak
/ping - bota ping
/playlist - çalma listenizi çalma
/bul - şarkıyı müzik veya video olarak indirme
/settings - grubun ayarları
/queue - sıraya alınan şarkıyı alma
"""

BASIC_BACK_BUTTON = InlineKeyboardMarkup(
    [   [
            InlineKeyboardButton(
                text="↪️ Geri", callback_data="command_menu"
            ),
            InlineKeyboardButton(
                text="🔄 Kapat", callback_data="close_btn"
            ),            
        ],                        
    ]
)

COMMAND_MENU_BUTTON = InlineKeyboardMarkup(
    [   [
            InlineKeyboardButton(
                text="🔍 Temel Komutlar", callback_data="basic_cmd"
            ),                                   
        ],
        [
            InlineKeyboardButton(
                text="📚 Gelişmiş Komutlar", callback_data="advanced_cmd"
            ),
        ],
        [
            InlineKeyboardButton(
                text="↪️ Geri", callback_data="open_start_menu"
            ),
            InlineKeyboardButton(
                text="🔄 Kapat", callback_data="close_btn"
            ),            
        ],                        
    ]
)
