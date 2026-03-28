"""
˹ʀᴇᴍ˼ Bot Buttons Module
All inline keyboard layouts
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    CallbackData, 
    CHANNEL_LINK, 
    GROUP_LINK, 
    DEV_PROFILE,
    BOT_USERNAME
)


class Buttons:
    """Inline keyboard button layouts"""
    
    # ============== START MENU ==============
    
    @staticmethod
    def start_menu() -> InlineKeyboardMarkup:
        """Main start menu buttons"""
        keyboard = [
            [
                InlineKeyboardButton("❓ Help", callback_data=CallbackData.HELP),
                InlineKeyboardButton("🎵 Mimi Tunes", callback_data=CallbackData.MUSIC)
            ],
            [
                InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK),
                InlineKeyboardButton("💬 Support", url=GROUP_LINK)
            ],
            [
                InlineKeyboardButton("👑 My Lord", url=DEV_PROFILE),
                InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{BOT_USERNAME.replace('@', '')}?startgroup=true")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== HELP MENU ==============
    
    @staticmethod
    def help_menu() -> InlineKeyboardMarkup:
        """Help menu with back button"""
        keyboard = [
            [
                InlineKeyboardButton("🔍 Anime Search", callback_data=CallbackData.ANIME_SEARCH),
                InlineKeyboardButton("👤 Character", callback_data=CallbackData.CHARACTER_SEARCH)
            ],
            [
                InlineKeyboardButton("📺 Airing", callback_data=CallbackData.AIRING),
                InlineKeyboardButton("⭐ Top Anime", callback_data=CallbackData.TOP_ANIME)
            ],
            [
                InlineKeyboardButton("👤 Profile", callback_data=CallbackData.PROFILE),
                InlineKeyboardButton("⚙️ Settings", callback_data=CallbackData.SETTINGS)
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_START),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== BACK BUTTONS ==============
    
    @staticmethod
    def back_to_start() -> InlineKeyboardMarkup:
        """Simple back to start button"""
        keyboard = [[
            InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_START),
            InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
        ]]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_to_help() -> InlineKeyboardMarkup:
        """Back to help menu button"""
        keyboard = [[
            InlineKeyboardButton("◀️ Back to Help", callback_data=CallbackData.BACK_HELP),
            InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
        ]]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== ANIME MENU ==============
    
    @staticmethod
    def anime_menu() -> InlineKeyboardMarkup:
        """Anime search menu"""
        keyboard = [
            [
                InlineKeyboardButton("🔍 Search Anime", switch_inline_query_current_chat="/anime "),
                InlineKeyboardButton("📺 This Season", callback_data=CallbackData.AIRING)
            ],
            [
                InlineKeyboardButton("⭐ Top Anime", callback_data=CallbackData.TOP_ANIME),
                InlineKeyboardButton("🎬 Upcoming", switch_inline_query_current_chat="/upcoming")
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_HELP)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def anime_result(mal_id: int, trailer_url: str = None) -> InlineKeyboardMarkup:
        """Anime result with trailer button"""
        keyboard = []
        
        if trailer_url:
            keyboard.append([
                InlineKeyboardButton("▶️ Watch Trailer", url=trailer_url),
                InlineKeyboardButton("🔗 MAL Page", url=f"https://myanimelist.net/anime/{mal_id}")
            ])
        else:
            keyboard.append([
                InlineKeyboardButton("🔗 MAL Page", url=f"https://myanimelist.net/anime/{mal_id}")
            ])
        
        keyboard.append([
            InlineKeyboardButton("◀️ Back", callback_data=CallbackData.ANIME_SEARCH),
            InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def character_result(mal_id: int) -> InlineKeyboardMarkup:
        """Character result buttons"""
        keyboard = [
            [
                InlineKeyboardButton("🔗 MAL Page", url=f"https://myanimelist.net/character/{mal_id}")
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.CHARACTER_SEARCH),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== SETTINGS MENU ==============
    
    @staticmethod
    def settings_menu(welcome: bool = True, goodbye: bool = False, 
                      captcha: bool = False, antiraid: bool = False) -> InlineKeyboardMarkup:
        """Group settings menu"""
        welcome_emoji = "✅" if welcome else "❌"
        goodbye_emoji = "✅" if goodbye else "❌"
        captcha_emoji = "✅" if captcha else "❌"
        antiraid_emoji = "✅" if antiraid else "❌"
        
        keyboard = [
            [
                InlineKeyboardButton(f"{welcome_emoji} Welcome", callback_data=CallbackData.WELCOME_TOGGLE),
                InlineKeyboardButton(f"{goodbye_emoji} Goodbye", callback_data=CallbackData.GOODBYE_TOGGLE)
            ],
            [
                InlineKeyboardButton(f"{captcha_emoji} Captcha", callback_data=CallbackData.CAPTCHA_TOGGLE),
                InlineKeyboardButton(f"{antiraid_emoji} Anti-Raid", callback_data=CallbackData.ANTIRAID_TOGGLE)
            ],
            [
                InlineKeyboardButton("📝 Filters", callback_data="filters"),
                InlineKeyboardButton("⚡ Anti-Raid Config", callback_data="antiraid_config")
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_HELP),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== CAPTCHA MENU ==============
    
    @staticmethod
    def captcha_button(captcha_id: int) -> InlineKeyboardMarkup:
        """Captcha verification button"""
        keyboard = [[
            InlineKeyboardButton("✅ I'm Human", callback_data=f"captcha_verify:{captcha_id}")
        ]]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def captcha_math(options: list, captcha_id: int) -> InlineKeyboardMarkup:
        """Math captcha with options"""
        keyboard = []
        row = []
        
        for i, option in enumerate(options):
            row.append(InlineKeyboardButton(
                str(option), 
                callback_data=f"captcha_math:{captcha_id}:{option}"
            ))
            if (i + 1) % 2 == 0:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        return InlineKeyboardMarkup(keyboard)
    
    # ============== ADMIN MENU ==============
    
    @staticmethod
    def admin_menu() -> InlineKeyboardMarkup:
        """Admin actions menu"""
        keyboard = [
            [
                InlineKeyboardButton("🔇 Mute", callback_data=CallbackData.ADMIN_MUTE),
                InlineKeyboardButton("🔊 Unmute", callback_data=CallbackData.ADMIN_UNMUTE)
            ],
            [
                InlineKeyboardButton("👢 Kick", callback_data=CallbackData.ADMIN_KICK),
                InlineKeyboardButton("🚫 Ban", callback_data=CallbackData.ADMIN_BAN)
            ],
            [
                InlineKeyboardButton("⚠️ Warn", callback_data=CallbackData.ADMIN_WARN),
                InlineKeyboardButton("🗑️ Purge", callback_data=CallbackData.ADMIN_PURGE)
            ],
            [
                InlineKeyboardButton("📌 Pin", callback_data=CallbackData.ADMIN_PIN),
                InlineKeyboardButton("🔒 Lock", callback_data=CallbackData.ADMIN_LOCK)
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_HELP),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== DEV MENU ==============
    
    @staticmethod
    def dev_menu() -> InlineKeyboardMarkup:
        """Developer menu"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Stats", callback_data=CallbackData.DEV_STATS),
                InlineKeyboardButton("📢 Broadcast", callback_data=CallbackData.DEV_BROADCAST)
            ],
            [
                InlineKeyboardButton("💾 Backup", callback_data=CallbackData.DEV_BACKUP),
                InlineKeyboardButton("🔄 Restart", callback_data=CallbackData.DEV_RESTART)
            ],
            [
                InlineKeyboardButton("🎬 Set Start Video", callback_data=CallbackData.DEV_SETVIDEO),
                InlineKeyboardButton("🖼️ Set Help Image", callback_data=CallbackData.DEV_SETIMG)
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_START),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== CONFIRMATION BUTTONS ==============
    
    @staticmethod
    def confirm_action(action: str, target_id: int) -> InlineKeyboardMarkup:
        """Confirm/cancel action buttons"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data=f"confirm:{action}:{target_id}"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== PAGINATION ==============
    
    @staticmethod
    def pagination(current_page: int, total_pages: int, prefix: str) -> InlineKeyboardMarkup:
        """Pagination buttons"""
        keyboard = []
        row = []
        
        if current_page > 1:
            row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"{prefix}:{current_page - 1}"))
        
        row.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="noop"))
        
        if current_page < total_pages:
            row.append(InlineKeyboardButton("Next ➡️", callback_data=f"{prefix}:{current_page + 1}"))
        
        keyboard.append(row)
        keyboard.append([
            InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_HELP),
            InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    # ============== CLOSE ONLY ==============
    
    @staticmethod
    def close_only() -> InlineKeyboardMarkup:
        """Just a close button"""
        keyboard = [[
            InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
        ]]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== URL BUTTONS ==============
    
    @staticmethod
    def url_button(text: str, url: str) -> InlineKeyboardMarkup:
        """Single URL button"""
        keyboard = [[
            InlineKeyboardButton(text, url=url)
        ]]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== TRAILER BUTTON ==============
    
    @staticmethod
    def trailer_button(trailer_url: str, mal_id: int) -> InlineKeyboardMarkup:
        """Trailer and MAL link buttons"""
        keyboard = [
            [
                InlineKeyboardButton("▶️ Watch Trailer", url=trailer_url),
                InlineKeyboardButton("🔗 MAL", url=f"https://myanimelist.net/anime/{mal_id}")
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.ANIME_SEARCH),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== MUSIC MENU ==============
    
    @staticmethod
    def music_menu() -> InlineKeyboardMarkup:
        """Music/Mimi Tunes menu"""
        keyboard = [
            [
                InlineKeyboardButton("🎵 Play", callback_data=CallbackData.MUSIC_PLAY),
                InlineKeyboardButton("⏸️ Pause", callback_data=CallbackData.MUSIC_PAUSE)
            ],
            [
                InlineKeyboardButton("⏭️ Skip", callback_data=CallbackData.MUSIC_SKIP),
                InlineKeyboardButton("🔁 Queue", callback_data=CallbackData.MUSIC_QUEUE)
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_START),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== PROFILE MENU ==============
    
    @staticmethod
    def profile_menu() -> InlineKeyboardMarkup:
        """User profile menu"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Stats", callback_data=CallbackData.PROFILE_STATS),
                InlineKeyboardButton("🏆 Achievements", callback_data=CallbackData.PROFILE_ACHIEVEMENTS)
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data=CallbackData.PROFILE_SETTINGS),
                InlineKeyboardButton("📜 History", callback_data=CallbackData.PROFILE_HISTORY)
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_HELP),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== BROADCAST MENU ==============
    
    @staticmethod
    def broadcast_menu() -> InlineKeyboardMarkup:
        """Broadcast options menu"""
        keyboard = [
            [
                InlineKeyboardButton("📢 All Groups", callback_data="broadcast_groups"),
                InlineKeyboardButton("👤 All Users", callback_data="broadcast_users")
            ],
            [
                InlineKeyboardButton("◀️ Back", callback_data=CallbackData.BACK_START),
                InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ============== FILTER MANAGEMENT ==============
    
    @staticmethod
    def filter_menu(filters: list) -> InlineKeyboardMarkup:
        """Filter management menu"""
        keyboard = []
        
        # Show existing filters
        for filt in filters[:10]:  # Limit to 10 filters
            keyboard.append([
                InlineKeyboardButton(
                    f"🗑️ {filt['keyword']}", 
                    callback_data=f"filter_delete:{filt['filter_id']}"
                )
            ])
        
        keyboard.append([
            InlineKeyboardButton("➕ Add Filter", callback_data="filter_add"),
            InlineKeyboardButton("🗑️ Clear All", callback_data="filter_clear")
        ])
        
        keyboard.append([
            InlineKeyboardButton("◀️ Back", callback_data=CallbackData.SETTINGS),
            InlineKeyboardButton("❌ Close", callback_data=CallbackData.CLOSE)
        ])
        
        return InlineKeyboardMarkup(keyboard)
