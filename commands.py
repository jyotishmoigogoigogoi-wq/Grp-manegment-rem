"""
˹ʀᴇᴍ˼ Bot Commands Module
All command handlers (user/admin/owner/dev)
"""

import requests
import random
import logging
from datetime import datetime, timedelta
from typing import Optional

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import (
    BOT_NAME, DEVELOPER_ID, JIKAN_BASE_URL,
    Messages, Format, Emojis, is_dev, is_owner, is_admin,
    can_restrict, can_delete, can_pin, can_promote
)
from database import db
from buttons import Buttons

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============== UTILITY FUNCTIONS ==============

def format_anime_info(anime: dict) -> str:
    """Format anime information for display"""
    title = anime.get('title', 'Unknown')
    title_jp = anime.get('title_japanese', 'N/A')
    episodes = anime.get('episodes', 'Unknown')
    score = anime.get('score', 'N/A')
    status = anime.get('status', 'Unknown')
    rating = anime.get('rating', 'N/A')
    synopsis = anime.get('synopsis', 'No synopsis available.')[:300]
    if len(anime.get('synopsis', '')) > 300:
        synopsis += "..."
    
    genres = ', '.join([g['name'] for g in anime.get('genres', [])]) or 'N/A'
    
    text = f"""
{Format.TOP_LEFT}{Format.HORIZONTAL * 33}{Format.TOP_RIGHT}
{Format.VERTICAL} {Emojis.ANIME} **{title}**{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} **Japanese:** {title_jp[:25]}{Format.VERTICAL}
{Format.VERTICAL} **Episodes:** {episodes}{Format.VERTICAL}
{Format.VERTICAL} **Score:** {Emojis.STAR} {score}{Format.VERTICAL}
{Format.VERTICAL} **Status:** {status}{Format.VERTICAL}
{Format.VERTICAL} **Rating:** {rating}{Format.VERTICAL}
{Format.VERTICAL} **Genres:** {genres[:25]}{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} **Synopsis:**{Format.VERTICAL}
{Format.VERTICAL} {synopsis[:30]}{Format.VERTICAL}
{Format.BOTTOM_LEFT}{Format.HORIZONTAL * 33}{Format.BOTTOM_RIGHT}
"""
    return text


def format_character_info(character: dict) -> str:
    """Format character information for display"""
    name = character.get('name', 'Unknown')
    name_jp = character.get('name_kanji', 'N/A')
    about = character.get('about', 'No information available.')[:300]
    if len(character.get('about', '')) > 300:
        about += "..."
    
    favorites = character.get('favorites', 0)
    
    text = f"""
{Format.TOP_LEFT}{Format.HORIZONTAL * 33}{Format.TOP_RIGHT}
{Format.VERTICAL} {Emojis.CHARACTER} **{name}**{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} **Kanji:** {name_jp[:25]}{Format.VERTICAL}
{Format.VERTICAL} {Emojis.HEART} Favorites: {favorites}{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} **About:**{Format.VERTICAL}
{Format.VERTICAL} {about[:30]}{Format.VERTICAL}
{Format.BOTTOM_LEFT}{Format.HORIZONTAL * 33}{Format.BOTTOM_RIGHT}
"""
    return text


def get_trailer_url(anime: dict) -> Optional[str]:
    """Get trailer URL from anime data"""
    trailer = anime.get('trailer', {})
    if trailer:
        youtube_id = trailer.get('youtube_id')
        if youtube_id:
            return f"https://youtube.com/watch?v={youtube_id}"
    return None


async def send_or_edit_message(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                               text: str, reply_markup=None, photo=None, video=None,
                               parse_mode=ParseMode.MARKDOWN) -> Optional[int]:
    """Send new message or edit existing based on session"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Get user session
    session = db.get_user_session(user_id, chat_id)
    
    if session and update.callback_query:
        # Edit existing message
        try:
            if photo:
                await update.callback_query.edit_message_caption(
                    caption=text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
            else:
                await update.callback_query.edit_message_text(
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
            return session['message_id']
        except Exception as e:
            logger.error(f"Error editing message: {e}")
    
    # Send new message
    try:
        if video:
            message = await context.bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        elif photo:
            message = await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        else:
            message = await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        
        # Save session
        db.set_user_session(user_id, chat_id, message.message_id, 'start')
        return message.message_id
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None


# ============== USER COMMANDS ==============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - DM only"""
    user = update.effective_user
    chat = update.effective_chat
    
    # Only allow in private chat
    if chat.type != 'private':
        return
    
    # Add/update user in database
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.increment_user_commands(user.id)
    
    # Get stats
    total_groups = db.get_total_groups()
    total_users = db.get_total_users()
    
    # Get start video from config
    start_video = db.get_config('start_video')
    
    # Create welcome message
    welcome_box = Format.box(
        f"{Emojis.BOT} Welcome to {BOT_NAME}\n"
        f"Your ultimate anime companion!",
        f" {BOT_NAME} {Emojis.BOT} "
    )
    
    stats_text = f"""
{welcome_box}

📊 **Bot Statistics:**
├ 👥 Groups: `{total_groups}`
├ 👤 Users: `{total_users}`
└ ⚡ Commands: Available

💫 **Features:**
├ 🔍 Anime Search
├ 👤 Character Info
├ 📺 Airing Schedule
├ ⚙️ Group Management
└ 🛡️ Anti-Raid Protection

➕ Add me to your group for full power!
"""
    
    # Send with video or text
    if start_video:
        message = await context.bot.send_video(
            chat_id=chat.id,
            video=start_video,
            caption=stats_text,
            reply_markup=Buttons.start_menu(),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        message = await context.bot.send_message(
            chat_id=chat.id,
            text=stats_text,
            reply_markup=Buttons.start_menu(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Save session
    db.set_user_session(user.id, chat.id, message.message_id, 'start')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user = update.effective_user
    chat = update.effective_chat
    
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.increment_user_commands(user.id)
    
    # Get help image from config
    help_img = db.get_config('help_image')
    
    help_box = Format.box("📖 Help Menu", " Help ")
    
    help_text = f"""
{help_box}

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
"""
    
    if chat.type == 'private':
        if help_img:
            message = await context.bot.send_photo(
                chat_id=chat.id,
                photo=help_img,
                caption=help_text,
                reply_markup=Buttons.help_menu(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            message = await context.bot.send_message(
                chat_id=chat.id,
                text=help_text,
                reply_markup=Buttons.help_menu(),
                parse_mode=ParseMode.MARKDOWN
            )
        db.set_user_session(user.id, chat.id, message.message_id, 'help')
    else:
        await update.message.reply_text(
            help_text,
            reply_markup=Buttons.close_only(),
            parse_mode=ParseMode.MARKDOWN
        )


async def anime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /anime command - Search for anime"""
    user = update.effective_user
    chat = update.effective_chat
    
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.increment_user_commands(user.id)
    
    # Get search query
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text(
            f"{Emojis.WARNING} Please provide an anime name.\n"
            f"Usage: `/anime <name>`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text(f"{Emojis.LOADING} Searching for anime...")
    
    try:
        # Search anime using Jikan API
        response = requests.get(
            f"{JIKAN_BASE_URL}/anime",
            params={'q': query, 'limit': 1},
            timeout=10
        )
        data = response.json()
        
        if not data.get('data'):
            await processing_msg.edit_text(Messages.ANIME_NOT_FOUND)
            return
        
        anime = data['data'][0]
        
        # Format and send result
        text = format_anime_info(anime)
        trailer_url = get_trailer_url(anime)
        
        # Get anime image
        images = anime.get('images', {})
        jpg = images.get('jpg', {})
        image_url = jpg.get('large_image_url') or jpg.get('image_url')
        
        await processing_msg.delete()
        
        if image_url:
            await context.bot.send_photo(
                chat_id=chat.id,
                photo=image_url,
                caption=text,
                reply_markup=Buttons.anime_result(anime['mal_id'], trailer_url),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text,
                reply_markup=Buttons.anime_result(anime['mal_id'], trailer_url),
                parse_mode=ParseMode.MARKDOWN
            )
            
    except Exception as e:
        logger.error(f"Error searching anime: {e}")
        await processing_msg.edit_text(Messages.ERROR)


async def character_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /character command - Search for character"""
    user = update.effective_user
    chat = update.effective_chat
    
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.increment_user_commands(user.id)
    
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text(
            f"{Emojis.WARNING} Please provide a character name.\n"
            f"Usage: `/character <name>`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    processing_msg = await update.message.reply_text(f"{Emojis.LOADING} Searching for character...")
    
    try:
        response = requests.get(
            f"{JIKAN_BASE_URL}/characters",
            params={'q': query, 'limit': 1},
            timeout=10
        )
        data = response.json()
        
        if not data.get('data'):
            await processing_msg.edit_text(Messages.CHARACTER_NOT_FOUND)
            return
        
        character = data['data'][0]
        
        text = format_character_info(character)
        
        # Get character image
        images = character.get('images', {})
        jpg = images.get('jpg', {})
        image_url = jpg.get('image_url')
        
        await processing_msg.delete()
        
        if image_url:
            await context.bot.send_photo(
                chat_id=chat.id,
                photo=image_url,
                caption=text,
                reply_markup=Buttons.character_result(character['mal_id']),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text,
                reply_markup=Buttons.character_result(character['mal_id']),
                parse_mode=ParseMode.MARKDOWN
            )
            
    except Exception as e:
        logger.error(f"Error searching character: {e}")
        await processing_msg.edit_text(Messages.ERROR)


async def airing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /airing command - Show currently airing anime"""
    user = update.effective_user
    chat = update.effective_chat
    
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.increment_user_commands(user.id)
    
    processing_msg = await update.message.reply_text(f"{Emojis.LOADING} Fetching airing schedule...")
    
    try:
        response = requests.get(
            f"{JIKAN_BASE_URL}/seasons/now",
            params={'limit': 10},
            timeout=10
        )
        data = response.json()
        
        if not data.get('data'):
            await processing_msg.edit_text("❌ No airing anime found.")
            return
        
        text = f"{Format.TOP_LEFT}{Format.HORIZONTAL * 33}{Format.TOP_RIGHT}\n"
        text += f"{Format.VERTICAL} {Emojis.ANIME} **Currently Airing**{Format.VERTICAL}\n"
        text += f"{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}\n"
        
        for i, anime in enumerate(data['data'][:10], 1):
            title = anime.get('title', 'Unknown')[:25]
            score = anime.get('score', 'N/A')
            text += f"{Format.VERTICAL} `{i}.` {title}{Format.VERTICAL}\n"
            text += f"{Format.VERTICAL}    {Emojis.STAR} {score}{Format.VERTICAL}\n"
        
        text += f"{Format.BOTTOM_LEFT}{Format.HORIZONTAL * 33}{Format.BOTTOM_RIGHT}"
        
        await processing_msg.edit_text(
            text,
            reply_markup=Buttons.back_to_help(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error fetching airing: {e}")
        await processing_msg.edit_text(Messages.ERROR)


async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /top command - Show top anime"""
    user = update.effective_user
    chat = update.effective_chat
    
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.increment_user_commands(user.id)
    
    processing_msg = await update.message.reply_text(f"{Emojis.LOADING} Fetching top anime...")
    
    try:
        response = requests.get(
            f"{JIKAN_BASE_URL}/top/anime",
            params={'limit': 10},
            timeout=10
        )
        data = response.json()
        
        if not data.get('data'):
            await processing_msg.edit_text("❌ No top anime found.")
            return
        
        text = f"{Format.TOP_LEFT}{Format.HORIZONTAL * 33}{Format.TOP_RIGHT}\n"
        text += f"{Format.VERTICAL} {Emojis.FIRE} **Top Anime**{Format.VERTICAL}\n"
        text += f"{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}\n"
        
        for i, anime in enumerate(data['data'][:10], 1):
            title = anime.get('title', 'Unknown')[:22]
            score = anime.get('score', 'N/A')
            text += f"{Format.VERTICAL} `{i}.` {title}{Format.VERTICAL}\n"
            text += f"{Format.VERTICAL}    {Emojis.STAR} {score}{Format.VERTICAL}\n"
        
        text += f"{Format.BOTTOM_LEFT}{Format.HORIZONTAL * 33}{Format.BOTTOM_RIGHT}"
        
        await processing_msg.edit_text(
            text,
            reply_markup=Buttons.back_to_help(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error fetching top anime: {e}")
        await processing_msg.edit_text(Messages.ERROR)


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /profile command - Show user profile"""
    user = update.effective_user
    chat = update.effective_chat
    
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.increment_user_commands(user.id)
    
    # Get user data
    user_data = db.get_user(user.id)
    
    if chat.type != 'private':
        # Get group member data
        member_data = db.get_group_member(chat.id, user.id)
    else:
        member_data = None
    
    text = f"""
{Format.TOP_LEFT}{Format.HORIZONTAL * 33}{Format.TOP_RIGHT}
{Format.VERTICAL} {Emojis.USER} **User Profile**{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} **Name:** {user.first_name}{Format.VERTICAL}
{Format.VERTICAL} **ID:** `{user.id}`{Format.VERTICAL}
{Format.VERTICAL} **Username:** @{user.username or 'N/A'}{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} **Stats:**{Format.VERTICAL}
{Format.VERTICAL} 📊 Commands: {user_data.get('command_count', 0) if user_data else 0}{Format.VERTICAL}
"""
    
    if member_data:
        text += f"{Format.VERTICAL} ⚠️ Warnings: {member_data.get('warn_count', 0)}{Format.VERTICAL}\n"
        text += f"{Format.VERTICAL} 💬 Messages: {member_data.get('messages_count', 0)}{Format.VERTICAL}\n"
    
    text += f"{Format.BOTTOM_LEFT}{Format.HORIZONTAL * 33}{Format.BOTTOM_RIGHT}"
    
    await update.message.reply_text(
        text,
        reply_markup=Buttons.profile_menu(),
        parse_mode=ParseMode.MARKDOWN
    )


# ============== ADMIN COMMANDS ==============

async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mute command - Mute a user"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_restrict(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to restrict members.")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(Messages.REPLY_REQUIRED)
        return
    
    target = update.message.reply_to_message.from_user
    
    # Can't mute admins
    if is_admin(context.bot, chat.id, target.id):
        await update.message.reply_text("❌ Cannot mute an admin.")
        return
    
    try:
        # Mute user
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(chat.id, target.id, permissions)
        
        # Log action
        db.add_log(chat.id, user.id, 'mute', target.id)
        
        await update.message.reply_text(
            f"{Emojis.CHECK} **Muted** {target.mention_html()}",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error muting user: {e}")
        await update.message.reply_text(Messages.ERROR)


async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unmute command - Unmute a user"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_restrict(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to restrict members.")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(Messages.REPLY_REQUIRED)
        return
    
    target = update.message.reply_to_message.from_user
    
    try:
        # Unmute user (restore default permissions)
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        await context.bot.restrict_chat_member(chat.id, target.id, permissions)
        
        # Log action
        db.add_log(chat.id, user.id, 'unmute', target.id)
        
        await update.message.reply_text(
            f"{Emojis.CHECK} **Unmuted** {target.mention_html()}",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error unmuting user: {e}")
        await update.message.reply_text(Messages.ERROR)


async def kick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /kick command - Kick a user"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_restrict(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to kick members.")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(Messages.REPLY_REQUIRED)
        return
    
    target = update.message.reply_to_message.from_user
    
    if is_admin(context.bot, chat.id, target.id):
        await update.message.reply_text("❌ Cannot kick an admin.")
        return
    
    try:
        await context.bot.ban_chat_member(chat.id, target.id)
        await context.bot.unban_chat_member(chat.id, target.id)  # Unban immediately to allow rejoin
        
        # Log action
        db.add_log(chat.id, user.id, 'kick', target.id)
        
        await update.message.reply_text(
            f"{Emojis.CHECK} **Kicked** {target.mention_html()}",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error kicking user: {e}")
        await update.message.reply_text(Messages.ERROR)


async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ban command - Ban a user"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_restrict(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to ban members.")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(Messages.REPLY_REQUIRED)
        return
    
    target = update.message.reply_to_message.from_user
    
    if is_admin(context.bot, chat.id, target.id):
        await update.message.reply_text("❌ Cannot ban an admin.")
        return
    
    try:
        await context.bot.ban_chat_member(chat.id, target.id)
        
        # Log action
        db.add_log(chat.id, user.id, 'ban', target.id)
        
        await update.message.reply_text(
            f"{Emojis.CHECK} **Banned** {target.mention_html()}",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error banning user: {e}")
        await update.message.reply_text(Messages.ERROR)


async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unban command - Unban a user"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_restrict(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to unban members.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Please provide a user ID to unban.")
        return
    
    try:
        target_id = int(context.args[0])
        await context.bot.unban_chat_member(chat.id, target_id)
        
        # Log action
        db.add_log(chat.id, user.id, 'unban', target_id)
        
        await update.message.reply_text(f"{Emojis.CHECK} **Unbanned** user `{target_id}`", parse_mode=ParseMode.MARKDOWN)
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")
    except Exception as e:
        logger.error(f"Error unbanning user: {e}")
        await update.message.reply_text(Messages.ERROR)


async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /warn command - Warn a user"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(Messages.REPLY_REQUIRED)
        return
    
    target = update.message.reply_to_message.from_user
    
    if is_admin(context.bot, chat.id, target.id):
        await update.message.reply_text("❌ Cannot warn an admin.")
        return
    
    reason = ' '.join(context.args) or "No reason provided"
    
    try:
        # Increment warn count
        warn_count = db.increment_warn(chat.id, target.id)
        
        # Log action
        db.add_log(chat.id, user.id, 'warn', target.id, reason)
        
        # Check if should ban (3 warnings)
        if warn_count >= 3:
            await context.bot.ban_chat_member(chat.id, target.id)
            await update.message.reply_text(
                f"{Emojis.WARNING} {target.mention_html()} **banned** for reaching 3 warnings!",
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                f"{Emojis.WARNING} **Warned** {target.mention_html()}\n"
                f"Warnings: {warn_count}/3\n"
                f"Reason: {reason}",
                parse_mode=ParseMode.HTML
            )
    except Exception as e:
        logger.error(f"Error warning user: {e}")
        await update.message.reply_text(Messages.ERROR)


async def purge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /purge command - Delete multiple messages"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_delete(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to delete messages.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Usage: `/purge <number>`", parse_mode=ParseMode.MARKDOWN)
        return
    
    try:
        count = int(context.args[0])
        if count < 1 or count > 100:
            await update.message.reply_text("❌ Please specify a number between 1 and 100.")
            return
    except ValueError:
        await update.message.reply_text("❌ Invalid number.")
        return
    
    try:
        # Delete command message first
        await update.message.delete()
        
        # Get messages to delete
        message_id = update.message.message_id
        deleted = 0
        
        for i in range(min(count, 100)):
            try:
                await context.bot.delete_message(chat.id, message_id - i)
                deleted += 1
            except:
                pass
        
        # Log action
        db.add_log(chat.id, user.id, 'purge', None, f"Deleted {deleted} messages")
        
        # Send confirmation and delete it after 3 seconds
        confirm_msg = await context.bot.send_message(
            chat.id,
            f"{Emojis.CHECK} Deleted {deleted} messages."
        )
        
        # Schedule deletion
        context.job_queue.run_once(
            lambda ctx: ctx.bot.delete_message(chat.id, confirm_msg.message_id),
            3
        )
        
    except Exception as e:
        logger.error(f"Error purging messages: {e}")
        await update.message.reply_text(Messages.ERROR)


async def pin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pin command - Pin a message"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_pin(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to pin messages.")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(Messages.REPLY_REQUIRED)
        return
    
    try:
        await context.bot.pin_chat_message(
            chat.id, 
            update.message.reply_to_message.message_id,
            disable_notification=False
        )
        
        # Log action
        db.add_log(chat.id, user.id, 'pin', update.message.reply_to_message.from_user.id)
        
        await update.message.reply_text(f"{Emojis.CHECK} Message pinned!")
    except Exception as e:
        logger.error(f"Error pinning message: {e}")
        await update.message.reply_text(Messages.ERROR)


async def unpin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unpin command - Unpin a message"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_pin(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to unpin messages.")
        return
    
    try:
        await context.bot.unpin_chat_message(chat.id)
        
        # Log action
        db.add_log(chat.id, user.id, 'unpin')
        
        await update.message.reply_text(f"{Emojis.CHECK} Message unpinned!")
    except Exception as e:
        logger.error(f"Error unpinning message: {e}")
        await update.message.reply_text(Messages.ERROR)


async def lock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /lock command - Lock the chat"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_restrict(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to lock the chat.")
        return
    
    try:
        # Lock chat by restricting default permissions
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.set_chat_permissions(chat.id, permissions)
        
        # Log action
        db.add_log(chat.id, user.id, 'lock')
        
        await update.message.reply_text(f"{Emojis.CHECK} Chat locked! 🔒")
    except Exception as e:
        logger.error(f"Error locking chat: {e}")
        await update.message.reply_text(Messages.ERROR)


async def unlock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unlock command - Unlock the chat"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_admin(context.bot, chat.id, user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not can_restrict(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to unlock the chat.")
        return
    
    try:
        # Unlock chat by restoring default permissions
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        await context.bot.set_chat_permissions(chat.id, permissions)
        
        # Log action
        db.add_log(chat.id, user.id, 'unlock')
        
        await update.message.reply_text(f"{Emojis.CHECK} Chat unlocked! 🔓")
    except Exception as e:
        logger.error(f"Error unlocking chat: {e}")
        await update.message.reply_text(Messages.ERROR)


# ============== OWNER COMMANDS ==============

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command - Group settings"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_owner(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group owner can use this command.")
        return
    
    # Get group settings
    group = db.get_group(chat.id)
    if not group:
        db.add_group(chat.id, chat.title, user.id)
        group = db.get_group(chat.id)
    
    welcome = group.get('welcome_enabled', True)
    goodbye = group.get('goodbye_enabled', False)
    captcha = group.get('captcha_enabled', False)
    antiraid = group.get('antiraid_enabled', False)
    
    text = f"""
{Format.TOP_LEFT}{Format.HORIZONTAL * 33}{Format.TOP_RIGHT}
{Format.VERTICAL} ⚙️ **Group Settings**{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} **Group:** {chat.title[:20]}{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} Toggle features below:{Format.VERTICAL}
{Format.BOTTOM_LEFT}{Format.HORIZONTAL * 33}{Format.BOTTOM_RIGHT}
"""
    
    await update.message.reply_text(
        text,
        reply_markup=Buttons.settings_menu(welcome, goodbye, captcha, antiraid),
        parse_mode=ParseMode.MARKDOWN
    )


async def welcome_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /welcome command - Toggle welcome messages"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_owner(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group owner can use this command.")
        return
    
    group = db.get_group(chat.id)
    if not group:
        db.add_group(chat.id, chat.title, user.id)
        group = db.get_group(chat.id)
    
    current = group.get('welcome_enabled', True)
    db.update_group_setting(chat.id, 'welcome_enabled', not current)
    
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"{Emojis.CHECK} Welcome messages {status}!")


async def goodbye_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /goodbye command - Toggle goodbye messages"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_owner(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group owner can use this command.")
        return
    
    group = db.get_group(chat.id)
    if not group:
        db.add_group(chat.id, chat.title, user.id)
        group = db.get_group(chat.id)
    
    current = group.get('goodbye_enabled', False)
    db.update_group_setting(chat.id, 'goodbye_enabled', not current)
    
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"{Emojis.CHECK} Goodbye messages {status}!")


async def captcha_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /captcha command - Toggle captcha"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_owner(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group owner can use this command.")
        return
    
    group = db.get_group(chat.id)
    if not group:
        db.add_group(chat.id, chat.title, user.id)
        group = db.get_group(chat.id)
    
    current = group.get('captcha_enabled', False)
    db.update_group_setting(chat.id, 'captcha_enabled', not current)
    
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"{Emojis.CHECK} Captcha {status}!")


async def filter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /filter command - Add a filter"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_owner(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group owner can use this command.")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: `/filter <keyword> <response>`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    keyword = context.args[0].lower()
    response = ' '.join(context.args[1:])
    
    if db.add_filter(chat.id, keyword, response, user.id):
        await update.message.reply_text(f"{Emojis.CHECK} Filter added: `{keyword}`", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(Messages.ERROR)


async def stopfilter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stopfilter command - Remove a filter"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_owner(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group owner can use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Usage: `/stopfilter <keyword>`", parse_mode=ParseMode.MARKDOWN)
        return
    
    keyword = context.args[0].lower()
    
    if db.remove_filter(chat.id, keyword):
        await update.message.reply_text(f"{Emojis.CHECK} Filter removed: `{keyword}`", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(Messages.ERROR)


async def promote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /promote command - Promote a user to admin"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_owner(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group owner can use this command.")
        return
    
    if not can_promote(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to promote members.")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(Messages.REPLY_REQUIRED)
        return
    
    target = update.message.reply_to_message.from_user
    
    try:
        await context.bot.promote_chat_member(
            chat.id,
            target.id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False,
            can_manage_chat=True,
            can_manage_video_chats=True
        )
        
        # Log action
        db.add_log(chat.id, user.id, 'promote', target.id)
        
        await update.message.reply_text(
            f"{Emojis.CHECK} **Promoted** {target.mention_html()} to admin!",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error promoting user: {e}")
        await update.message.reply_text(Messages.ERROR)


async def demote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /demote command - Demote an admin"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == 'private':
        await update.message.reply_text(Messages.GROUP_ONLY)
        return
    
    if not is_owner(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ Only group owner can use this command.")
        return
    
    if not can_promote(context.bot, chat.id, user.id):
        await update.message.reply_text("❌ You don't have permission to demote members.")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(Messages.REPLY_REQUIRED)
        return
    
    target = update.message.reply_to_message.from_user
    
    try:
        # Demote by removing all permissions
        await context.bot.promote_chat_member(
            chat.id,
            target.id,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=False,
            can_manage_video_chats=False
        )
        
        # Log action
        db.add_log(chat.id, user.id, 'demote', target.id)
        
        await update.message.reply_text(
            f"{Emojis.CHECK} **Demoted** {target.mention_html()}",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error demoting user: {e}")
        await update.message.reply_text(Messages.ERROR)


# ============== DEVELOPER COMMANDS ==============

async def setstartvideo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setstartvideo command - Set start video"""
    user = update.effective_user
    
    if not is_dev(user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not update.message.reply_to_message or not update.message.reply_to_message.video:
        await update.message.reply_text("❌ Please reply to a video message.")
        return
    
    video = update.message.reply_to_message.video
    file_id = video.file_id
    
    if db.set_config('start_video', file_id):
        await update.message.reply_text(f"{Emojis.CHECK} Start video set successfully!")
    else:
        await update.message.reply_text(Messages.ERROR)


async def sethelpimg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sethelpimg command - Set help image"""
    user = update.effective_user
    
    if not is_dev(user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("❌ Please reply to a photo message.")
        return
    
    photo = update.message.reply_to_message.photo[-1]  # Get largest photo
    file_id = photo.file_id
    
    if db.set_config('help_image', file_id):
        await update.message.reply_text(f"{Emojis.CHECK} Help image set successfully!")
    else:
        await update.message.reply_text(Messages.ERROR)


async def devstats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /devstats command - Show full bot statistics"""
    user = update.effective_user
    
    if not is_dev(user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    stats = db.get_stats()
    
    text = f"""
{Format.TOP_LEFT}{Format.HORIZONTAL * 33}{Format.TOP_RIGHT}
{Format.VERTICAL} ⚡ **Developer Statistics**{Format.VERTICAL}
{Format.LEFT_T}{Format.HORIZONTAL * 33}{Format.RIGHT_T}
{Format.VERTICAL} 👤 Total Users: `{stats['total_users']}`{Format.VERTICAL}
{Format.VERTICAL} 👥 Total Groups: `{stats['total_groups']}`{Format.VERTICAL}
{Format.VERTICAL} 📊 Total Commands: `{stats['total_commands']}`{Format.VERTICAL}
{Format.VERTICAL} 👥 Total Members: `{stats['total_members']}`{Format.VERTICAL}
{Format.VERTICAL} 🔒 Total Captchas: `{stats['total_captchas']}`{Format.VERTICAL}
{Format.BOTTOM_LEFT}{Format.HORIZONTAL * 33}{Format.BOTTOM_RIGHT}
"""
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command - Broadcast message to all groups"""
    user = update.effective_user
    
    if not is_dev(user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    message = update.message.reply_to_message
    if not message:
        await update.message.reply_text("❌ Please reply to a message to broadcast.")
        return
    
    groups = db.get_all_groups()
    
    processing_msg = await update.message.reply_text(
        f"{Emojis.LOADING} Broadcasting to {len(groups)} groups..."
    )
    
    success = 0
    failed = 0
    
    for group_id in groups:
        try:
            if message.text:
                await context.bot.send_message(group_id, message.text, parse_mode=ParseMode.MARKDOWN)
            elif message.photo:
                await context.bot.send_photo(
                    group_id, 
                    message.photo[-1].file_id,
                    caption=message.caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            elif message.video:
                await context.bot.send_video(
                    group_id,
                    message.video.file_id,
                    caption=message.caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            success += 1
        except Exception as e:
            logger.error(f"Failed to broadcast to {group_id}: {e}")
            failed += 1
    
    await processing_msg.edit_text(
        f"{Emojis.CHECK} Broadcast complete!\n"
        f"Success: {success}\n"
        f"Failed: {failed}"
    )


async def backup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backup command - Export database"""
    user = update.effective_user
    
    if not is_dev(user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    await update.message.reply_text(
        f"{Emojis.LOADING} Creating backup...\n\n"
        f"Note: Full database backup requires pg_dump. "
        f"Contact your database provider for backup options."
    )


async def restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /restart command - Restart the bot"""
    user = update.effective_user
    
    if not is_dev(user.id):
        await update.message.reply_text(Messages.NO_PERMISSION)
        return
    
    await update.message.reply_text(f"{Emojis.LOADING} Restarting bot...")
    
    # Exit the process - Render will restart it
    import sys
    sys.exit(0)


# ============== CALLBACK HANDLERS ==============

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    chat = update.effective_chat
    data = query.data
    
    # Navigation callbacks
    if data == CallbackData.HELP:
        await help_command(update, context)
    
    elif data == CallbackData.BACK_START:
        # Return to start menu
        await start_command(update, context)
    
    elif data == CallbackData.BACK_HELP:
        # Return to help menu
        await help_command(update, context)
    
    elif data == CallbackData.CLOSE:
        # Delete the message
        try:
            await query.message.delete()
        except:
            pass
    
    elif data == CallbackData.ANIME_SEARCH:
        text = f"{Format.box('Use /anime <name> to search for anime', ' Anime Search ')}"
        await query.edit_message_text(
            text,
            reply_markup=Buttons.back_to_help(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == CallbackData.CHARACTER_SEARCH:
        text = f"{Format.box('Use /character <name> to search for characters', ' Character Search ')}"
        await query.edit_message_text(
            text,
            reply_markup=Buttons.back_to_help(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == CallbackData.AIRING:
        await airing_command(update, context)
    
    elif data == CallbackData.TOP_ANIME:
        await top_command(update, context)
    
    elif data == CallbackData.PROFILE:
        await profile_command(update, context)
    
    elif data == CallbackData.SETTINGS:
        # Show settings
        if chat.type == 'private':
            await query.edit_message_text(
                f"{Format.box('Settings are only available in groups', ' Settings ')}",
                reply_markup=Buttons.back_to_help(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            group = db.get_group(chat.id)
            if group:
                welcome = group.get('welcome_enabled', True)
                goodbye = group.get('goodbye_enabled', False)
                captcha = group.get('captcha_enabled', False)
                antiraid = group.get('antiraid_enabled', False)
                
                await query.edit_message_text(
                    f"{Format.box('Group Settings', ' Settings ')}",
                    reply_markup=Buttons.settings_menu(welcome, goodbye, captcha, antiraid),
                    parse_mode=ParseMode.MARKDOWN
                )
    
    elif data == CallbackData.MUSIC:
        await query.edit_message_text(
            f"{Format.box('Mimi Tunes - Coming Soon!', ' Music ')}",
            reply_markup=Buttons.music_menu(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == CallbackData.DEV:
        if is_dev(user.id):
            await query.edit_message_text(
                f"{Format.box('Developer Zone', ' Dev ')}",
                reply_markup=Buttons.dev_menu(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await query.answer("❌ Access denied!", show_alert=True)
    
    # Settings toggles
    elif data == CallbackData.WELCOME_TOGGLE:
        if is_owner(context.bot, chat.id, user.id):
            group = db.get_group(chat.id)
            current = group.get('welcome_enabled', True) if group else True
            db.update_group_setting(chat.id, 'welcome_enabled', not current)
            await query.answer(f"Welcome {'disabled' if current else 'enabled'}!")
        else:
            await query.answer("❌ Only owner can change settings!", show_alert=True)
    
    elif data == CallbackData.GOODBYE_TOGGLE:
        if is_owner(context.bot, chat.id, user.id):
            group = db.get_group(chat.id)
            current = group.get('goodbye_enabled', False) if group else False
            db.update_group_setting(chat.id, 'goodbye_enabled', not current)
            await query.answer(f"Goodbye {'disabled' if current else 'enabled'}!")
        else:
            await query.answer("❌ Only owner can change settings!", show_alert=True)
    
    elif data == CallbackData.CAPTCHA_TOGGLE:
        if is_owner(context.bot, chat.id, user.id):
            group = db.get_group(chat.id)
            current = group.get('captcha_enabled', False) if group else False
            db.update_group_setting(chat.id, 'captcha_enabled', not current)
            await query.answer(f"Captcha {'disabled' if current else 'enabled'}!")
        else:
            await query.answer("❌ Only owner can change settings!", show_alert=True)
    
    elif data == CallbackData.ANTIRAID_TOGGLE:
        if is_owner(context.bot, chat.id, user.id):
            group = db.get_group(chat.id)
            current = group.get('antiraid_enabled', False) if group else False
            db.update_group_setting(chat.id, 'antiraid_enabled', not current)
            await query.answer(f"Anti-raid {'disabled' if current else 'enabled'}!")
        else:
            await query.answer("❌ Only owner can change settings!", show_alert=True)
