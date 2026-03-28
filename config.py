"""
˹ʀᴇᴍ˼ Bot Configuration
Constants, links, and formatting templates
"""

import os

# ============== BOT IDENTITY ==============
BOT_NAME = "˹ʀᴇᴍ˼"
BOT_USERNAME = "@RemNanoBot"
DEVELOPER_NAME = "YorichiiPrime"
DEVELOPER_ID = 7728424218

# ============== LINKS ==============
CHANNEL_LINK = "https://t.me/+g9uDSVO-mTI0Nzc9"
GROUP_LINK = "https://t.me/kingchaos7"
DEV_PROFILE = "https://t.me/YorichiiPrime"

# ============== API KEYS ==============
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")

# ============== AESTHETIC FORMATTING ==============
class Format:
    """Aesthetic formatting templates - Telegram Compatible"""
    
    @staticmethod
    def box(content: str, title: str = "") -> str:
        """Create a formatted box around content - Works in Telegram"""
        if title:
            return f"╔═══❰ {title} ❱═══╗\n{content}\n╚════════════════╝"
        return f"╔════════════════╗\n{content}\n╚════════════════╝"
    
    @staticmethod
    def section(title: str) -> str:
        """Create a section header"""
        return f"\n┌─❰ {title} ❱─┐"
    
    @staticmethod
    def separator() -> str:
        """Create a separator line"""
        return "━━━━━━━━━━━━━━━"

# ============== MESSAGES ==============
class Messages:
    """Bot message templates"""
    
    START_TEXT = """{box}

✨ **Welcome to {bot_name}** ✨

🤖 Your ultimate anime & group management companion!

📊 **Bot Statistics:**
├ 👥 Groups: `{groups}`
├ 👤 Users: `{users}`
└ ⚡ Commands: `{commands}`

💫 **Features:**
├ 🔍 Anime Search
├ 👤 Character Info
├ 📺 Airing Schedule
├ ⚙️ Group Management
└ 🛡️ Anti-Raid Protection

➕ Add me to your group for full power!"""

    HELP_TEXT = """{box}

📖 **Help Menu**

**User Commands:**
├ /start - Start the bot
├ /help - Show this menu
├ /anime `<name>` - Search anime
├ /character `<name>` - Search character
├ /airing - Currently airing
├ /top - Top anime
└ /profile - Your profile

**Admin Commands:**
├ /mute - Mute user (reply)
├ /unmute - Unmute user
├ /kick - Kick user
├ /ban - Ban user
├ /unban - Unban user
├ /warn - Warn user
├ /purge `<n>` - Delete messages
├ /pin - Pin message
├ /unpin - Unpin message
└ /lock - Lock chat

**Owner Commands:**
├ /settings - Group settings
├ /welcome - Toggle welcome
├ /goodbye - Toggle goodbye
├ /captcha - Toggle captcha
├ /filter - Add filter
├ /stopfilter - Remove filter
└ /promote - Promote admin

**Dev Commands:**
├ /setstartvideo - Set start video
├ /sethelpimg - Set help image
├ /devstats - Bot statistics
├ /broadcast - Broadcast msg
├ /backup - Backup database
└ /restart - Restart bot"""

    ANIME_NOT_FOUND = "❌ Anime not found. Please check the name and try again."
    CHARACTER_NOT_FOUND = "❌ Character not found. Please check the name and try again."
    NO_PERMISSION = "⛔ You don't have permission to use this command."
    GROUP_ONLY = "👥 This command only works in groups."
    PRIVATE_ONLY = "💬 This command only works in private chat."
    REPLY_REQUIRED = "↩️ Please reply to a message to use this command."
    PROCESSING = "⏳ Processing..."
    SUCCESS = "✅ Success!"
    ERROR = "❌ An error occurred. Please try again."

# ============== EMOJIS ==============
class Emojis:
    """Emoji constants"""
    BOT = "🤖"
    USER = "👤"
    GROUP = "👥"
    ADMIN = "👮"
    OWNER = "👑"
    DEV = "⚡"
    ANIME = "🎬"
    CHARACTER = "👤"
    SEARCH = "🔍"
    SETTINGS = "⚙️"
    BACK = "◀️"
    CLOSE = "❌"
    HOME = "🏠"
    HELP = "❓"
    MUSIC = "🎵"
    CHANNEL = "📢"
    SUPPORT = "💬"
    ADD = "➕"
    CHECK = "✅"
    CROSS = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    FIRE = "🔥"
    STAR = "⭐"
    HEART = "❤️"
    ARROW = "➡️"
    LOADING = "⏳"
    LOCK = "🔒"
    UNLOCK = "🔓"
    PIN = "📌"
    UNPIN = "📍"
    KICK = "👢"
    BAN = "🚫"
    MUTE = "🔇"
    UNMUTE = "🔊"
    WARN = "⚠️"
    PURGE = "🗑️"

# ============== CALLBACK DATA ==============
class CallbackData:
    """Callback data constants"""
    HELP = "help"
    MUSIC = "music"
    CHANNEL = "channel"
    SUPPORT = "support"
    DEV = "dev"
    ADD_GROUP = "add_group"
    BACK_START = "back_start"
    BACK_HELP = "back_help"
    CLOSE = "close"
    ANIME_SEARCH = "anime_search"
    CHARACTER_SEARCH = "character_search"
    TOP_ANIME = "top_anime"
    AIRING = "airing"
    PROFILE = "profile"
    SETTINGS = "settings"
    WELCOME_TOGGLE = "welcome_toggle"
    GOODBYE_TOGGLE = "goodbye_toggle"
    CAPTCHA_TOGGLE = "captcha_toggle"
    ANTIRAID_TOGGLE = "antiraid_toggle"
    # Admin callbacks
    ADMIN_MUTE = "admin_mute"
    ADMIN_UNMUTE = "admin_unmute"
    ADMIN_KICK = "admin_kick"
    ADMIN_BAN = "admin_ban"
    ADMIN_WARN = "admin_warn"
    ADMIN_PURGE = "admin_purge"
    ADMIN_PIN = "admin_pin"
    ADMIN_LOCK = "admin_lock"
    # Dev callbacks
    DEV_STATS = "dev_stats"
    DEV_BROADCAST = "dev_broadcast"
    DEV_BACKUP = "dev_backup"
    DEV_RESTART = "dev_restart"
    DEV_SETVIDEO = "dev_setvideo"
    DEV_SETIMG = "dev_setimg"
    # Music callbacks
    MUSIC_PLAY = "music_play"
    MUSIC_PAUSE = "music_pause"
    MUSIC_SKIP = "music_skip"
    MUSIC_QUEUE = "music_queue"
    # Profile callbacks
    PROFILE_STATS = "profile_stats"
    PROFILE_ACHIEVEMENTS = "profile_achievements"
    PROFILE_SETTINGS = "profile_settings"
    PROFILE_HISTORY = "profile_history"

# ============== DATABASE TABLES ==============
DB_TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username VARCHAR(255),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            command_count INT DEFAULT 0,
            is_premium BOOLEAN DEFAULT FALSE
        )
    """,
    "groups": """
        CREATE TABLE IF NOT EXISTS groups (
            group_id BIGINT PRIMARY KEY,
            group_name VARCHAR(255),
            owner_id BIGINT,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            welcome_enabled BOOLEAN DEFAULT TRUE,
            goodbye_enabled BOOLEAN DEFAULT FALSE,
            captcha_enabled BOOLEAN DEFAULT FALSE,
            captcha_mode VARCHAR(20) DEFAULT 'button',
            antiraid_enabled BOOLEAN DEFAULT FALSE,
            antiraid_limit INT DEFAULT 10,
            lock_enabled BOOLEAN DEFAULT FALSE,
            filter_enabled BOOLEAN DEFAULT TRUE,
            welcome_text TEXT DEFAULT 'Welcome {mention} to {group_name}!',
            goodbye_text TEXT DEFAULT 'Goodbye {mention}!',
            welcome_media VARCHAR(255),
            settings TEXT DEFAULT '{}'
        )
    """,
    "group_members": """
        CREATE TABLE IF NOT EXISTS group_members (
            id SERIAL PRIMARY KEY,
            group_id BIGINT,
            user_id BIGINT,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            warn_count INT DEFAULT 0,
            is_muted BOOLEAN DEFAULT FALSE,
            mute_until TIMESTAMP,
            messages_count INT DEFAULT 0,
            UNIQUE(group_id, user_id)
        )
    """,
    "user_sessions": """
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id SERIAL PRIMARY KEY,
            user_id BIGINT,
            chat_id BIGINT,
            message_id BIGINT,
            current_menu VARCHAR(50) DEFAULT 'start',
            session_data TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "bot_config": """
        CREATE TABLE IF NOT EXISTS bot_config (
            config_key VARCHAR(50) PRIMARY KEY,
            config_value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "captcha_sessions": """
        CREATE TABLE IF NOT EXISTS captcha_sessions (
            session_id SERIAL PRIMARY KEY,
            user_id BIGINT,
            chat_id BIGINT,
            message_id BIGINT,
            captcha_type VARCHAR(20),
            captcha_answer VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            verified BOOLEAN DEFAULT FALSE
        )
    """,
    "filters": """
        CREATE TABLE IF NOT EXISTS filters (
            filter_id SERIAL PRIMARY KEY,
            group_id BIGINT,
            keyword VARCHAR(255),
            response TEXT,
            created_by BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "logs": """
        CREATE TABLE IF NOT EXISTS logs (
            log_id SERIAL PRIMARY KEY,
            group_id BIGINT,
            admin_id BIGINT,
            action VARCHAR(50),
            target_id BIGINT,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
}

# ============== DEFAULT VALUES ==============
DEFAULT_WELCOME_VIDEO = None
DEFAULT_HELP_IMAGE = None

# ============== JIKAN API ==============
JIKAN_BASE_URL = "https://api.jikan.moe/v4"

# ============== RENDER CONFIG ==============
RENDER_PORT = int(os.getenv("PORT", 8080))
KEEP_ALIVE_INTERVAL = 300  # 5 minutes

# ============== ROLE CHECKS ==============
def is_dev(user_id: int) -> bool:
    """Check if user is developer"""
    return user_id == DEVELOPER_ID

def is_owner(bot, chat_id: int, user_id: int) -> bool:
    """Check if user is group owner"""
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        return chat_member.status == 'creator'
    except:
        return False

def is_admin(bot, chat_id: int, user_id: int) -> bool:
    """Check if user is admin (includes owner)"""
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ['creator', 'administrator']
    except:
        return False

def can_restrict(bot, chat_id: int, user_id: int) -> bool:
    """Check if user can restrict members"""
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        if chat_member.status == 'creator':
            return True
        if chat_member.status == 'administrator':
            return chat_member.can_restrict_members or False
        return False
    except:
        return False

def can_delete(bot, chat_id: int, user_id: int) -> bool:
    """Check if user can delete messages"""
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        if chat_member.status == 'creator':
            return True
        if chat_member.status == 'administrator':
            return chat_member.can_delete_messages or False
        return False
    except:
        return False

def can_pin(bot, chat_id: int, user_id: int) -> bool:
    """Check if user can pin messages"""
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        if chat_member.status == 'creator':
            return True
        if chat_member.status == 'administrator':
            return chat_member.can_pin_messages or False
        return False
    except:
        return False

def can_promote(bot, chat_id: int, user_id: int) -> bool:
    """Check if user can promote members"""
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        if chat_member.status == 'creator':
            return True
        if chat_member.status == 'administrator':
            return chat_member.can_promote_members or False
        return False
    except:
        return False
