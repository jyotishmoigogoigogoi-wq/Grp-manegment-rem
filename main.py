"""
˹ʀᴇᴍ˼ Bot - Main Entry Point
Telegram Bot for Anime & Group Management
Developed by YorichiiPrime
"""

import logging
import asyncio
import random
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ChatMemberHandler,
    filters
)

from config import BOT_TOKEN, BOT_NAME, DEVELOPER_NAME, Emojis
from database import db
from keep_alive import keep_alive
from commands import (
    # User commands
    start_command,
    help_command,
    anime_command,
    character_command,
    airing_command,
    top_command,
    profile_command,
    # Admin commands
    mute_command,
    unmute_command,
    kick_command,
    ban_command,
    unban_command,
    warn_command,
    purge_command,
    pin_command,
    unpin_command,
    lock_command,
    unlock_command,
    # Owner commands
    settings_command,
    welcome_command,
    goodbye_command,
    captcha_command,
    filter_command,
    stopfilter_command,
    promote_command,
    demote_command,
    # Developer commands
    setstartvideo_command,
    sethelpimg_command,
    devstats_command,
    broadcast_command,
    backup_command,
    restart_command,
    # Callback handler
    button_callback
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ============== EVENT HANDLERS ==============

async def handle_new_member(update: Update, context):
    """Handle new chat members - Welcome & Captcha"""
    chat = update.effective_chat
    
    # Skip if not a group
    if chat.type == 'private':
        return
    
    # Get group settings
    group = db.get_group(chat.id)
    if not group:
        # Auto-add group to database
        db.add_group(chat.id, chat.title, update.effective_chat.id)
        group = db.get_group(chat.id)
    
    for member in update.chat_member.new_chat_members:
        # Skip bots
        if member.is_bot:
            continue
        
        # Add user to database
        db.add_user(member.id, member.username, member.first_name, member.last_name)
        db.add_group_member(chat.id, member.id)
        
        # Check welcome enabled
        if group and group.get('welcome_enabled', True):
            welcome_text = group.get('welcome_text', 'Welcome {mention} to {group_name}!')
            welcome_text = welcome_text.replace('{mention}', member.mention_html())
            welcome_text = welcome_text.replace('{group_name}', chat.title)
            welcome_text = welcome_text.replace('{username}', member.username or 'N/A')
            welcome_text = welcome_text.replace('{first_name}', member.first_name)
            
            welcome_media = group.get('welcome_media')
            
            try:
                if welcome_media:
                    await context.bot.send_photo(
                        chat.id,
                        photo=welcome_media,
                        caption=welcome_text,
                        parse_mode='HTML'
                    )
                else:
                    await context.bot.send_message(
                        chat.id,
                        welcome_text,
                        parse_mode='HTML'
                    )
            except Exception as e:
                logger.error(f"Error sending welcome: {e}")
        
        # Check captcha enabled
        if group and group.get('captcha_enabled', False):
            captcha_mode = group.get('captcha_mode', 'button')
            
            try:
                if captcha_mode == 'button':
                    # Simple button captcha
                    from buttons import Buttons
                    captcha_id = db.create_captcha(member.id, chat.id, 'button', 'verified')
                    
                    msg = await context.bot.send_message(
                        chat.id,
                        f"{member.mention_html()}, please verify you're human!",
                        reply_markup=Buttons.captcha_button(captcha_id),
                        parse_mode='HTML'
                    )
                    
                    # Update captcha with message id
                    # (In production, you'd want to update the captcha session)
                    
                elif captcha_mode == 'math':
                    # Math captcha
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 10)
                    answer = num1 + num2
                    
                    captcha_id = db.create_captcha(member.id, chat.id, 'math', str(answer))
                    
                    # Generate options
                    options = [answer]
                    while len(options) < 4:
                        fake = random.randint(2, 20)
                        if fake not in options:
                            options.append(fake)
                    random.shuffle(options)
                    
                    from buttons import Buttons
                    await context.bot.send_message(
                        chat.id,
                        f"{member.mention_html()}, solve this: {num1} + {num2} = ?",
                        reply_markup=Buttons.captcha_math(options, captcha_id),
                        parse_mode='HTML'
                    )
                    
            except Exception as e:
                logger.error(f"Error sending captcha: {e}")


async def handle_left_member(update: Update, context):
    """Handle members leaving - Goodbye message"""
    chat = update.effective_chat
    
    if chat.type == 'private':
        return
    
    # Get group settings
    group = db.get_group(chat.id)
    if not group:
        return
    
    if group.get('goodbye_enabled', False):
        member = update.chat_member.old_chat_member.user
        
        goodbye_text = group.get('goodbye_text', 'Goodbye {mention}!')
        goodbye_text = goodbye_text.replace('{mention}', member.mention_html())
        goodbye_text = goodbye_text.replace('{group_name}', chat.title)
        goodbye_text = goodbye_text.replace('{username}', member.username or 'N/A')
        goodbye_text = goodbye_text.replace('{first_name}', member.first_name)
        
        try:
            await context.bot.send_message(
                chat.id,
                goodbye_text,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Error sending goodbye: {e}")
    
    # Remove from group members
    member = update.chat_member.old_chat_member.user
    db.remove_group_member(chat.id, member.id)


async def handle_message(update: Update, context):
    """Handle regular messages - Filters, etc."""
    if not update.effective_message or not update.effective_message.text:
        return
    
    chat = update.effective_chat
    user = update.effective_user
    text = update.effective_message.text
    
    # Skip private chats
    if chat.type == 'private':
        return
    
    # Update user activity
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Check filters
    group = db.get_group(chat.id)
    if group and group.get('filter_enabled', True):
        filters_list = db.get_filters(chat.id)
        for filt in filters_list:
            if filt['keyword'].lower() in text.lower():
                await update.message.reply_text(filt['response'])
                break


async def handle_captcha_callback(update: Update, context):
    """Handle captcha verification callbacks"""
    query = update.callback_query
    data = query.data
    
    if not data.startswith('captcha_'):
        return
    
    await query.answer()
    
    user = update.effective_user
    chat = update.effective_chat
    
    parts = data.split(':')
    action = parts[0]
    
    if action == 'captcha_verify':
        captcha_id = int(parts[1])
        captcha = db.get_captcha(user.id, chat.id)
        
        if captcha and captcha['session_id'] == captcha_id:
            db.verify_captcha(captcha_id)
            await query.edit_message_text(
                f"╔═══════════════════╗\n"
                f"║ ✅ Verified!        ║\n"
                f"╠═══════════════════╣\n"
                f"║ 👤 {user.mention_html()}\n"
                f"║ ✓ Human confirmed\n"
                f"╚═══════════════════╝",
                parse_mode='HTML'
            )
        else:
            await query.answer("❌ Invalid or expired captcha!", show_alert=True)
    
    elif action == 'captcha_math':
        captcha_id = int(parts[1])
        answer = parts[2]
        
        captcha = db.get_captcha(user.id, chat.id)
        
        if captcha and captcha['session_id'] == captcha_id:
            if captcha['captcha_answer'] == answer:
                db.verify_captcha(captcha_id)
                await query.edit_message_text(
                    f"╔═══════════════════╗\n"
                    f"║ ✅ Correct!         ║\n"
                    f"╠═══════════════════╣\n"
                    f"║ 👤 {user.mention_html()}\n"
                    f"║ ✓ Math verified\n"
                    f"╚═══════════════════╝",
                    parse_mode='HTML'
                )
            else:
                await query.answer("❌ Wrong answer! Try again.", show_alert=True)
        else:
            await query.answer("❌ Invalid or expired captcha!", show_alert=True)


async def error_handler(update: Update, context):
    """Handle errors"""
    logger.error(f"Update {update} caused error: {context.error}")
    
    # Notify user of error if possible
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                f"╔═══════════════════╗\n"
                f"║ ❌ Error!           ║\n"
                f"╠═══════════════════╣\n"
                f"║ Something went\n"
                f"║ wrong. Try again.\n"
                f"╚═══════════════════╝"
            )
        except:
            pass


# ============== BOT INITIALIZATION ==============

def main():
    """Main function - Initialize and run bot"""
    
    print(f"""
    ╔══════════════════════════════════════════╗
    ║                                          ║
    ║           {BOT_NAME} Bot              ║
    ║                                          ║
    ║     Anime & Group Management Bot         ║
    ║                                          ║
    ║     Developed by: {DEVELOPER_NAME}        ║
    ║                                          ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Start keep-alive server
    print("[Main] Starting keep-alive server...")
    keep_alive()
    
    # Check required environment variables
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not set!")
        return
    
    print("[Main] Initializing bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ============== COMMAND HANDLERS ==============
    
    # User commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("anime", anime_command))
    application.add_handler(CommandHandler("character", character_command))
    application.add_handler(CommandHandler("airing", airing_command))
    application.add_handler(CommandHandler("top", top_command))
    application.add_handler(CommandHandler("profile", profile_command))
    
    # Admin commands
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("kick", kick_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("warn", warn_command))
    application.add_handler(CommandHandler("purge", purge_command))
    application.add_handler(CommandHandler("pin", pin_command))
    application.add_handler(CommandHandler("unpin", unpin_command))
    application.add_handler(CommandHandler("lock", lock_command))
    application.add_handler(CommandHandler("unlock", unlock_command))
    
    # Owner commands
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("welcome", welcome_command))
    application.add_handler(CommandHandler("goodbye", goodbye_command))
    application.add_handler(CommandHandler("captcha", captcha_command))
    application.add_handler(CommandHandler("filter", filter_command))
    application.add_handler(CommandHandler("stopfilter", stopfilter_command))
    application.add_handler(CommandHandler("promote", promote_command))
    application.add_handler(CommandHandler("demote", demote_command))
    
    # Developer commands
    application.add_handler(CommandHandler("setstartvideo", setstartvideo_command))
    application.add_handler(CommandHandler("sethelpimg", sethelpimg_command))
    application.add_handler(CommandHandler("devstats", devstats_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("backup", backup_command))
    application.add_handler(CommandHandler("restart", restart_command))
    
    # Captcha callback handler (higher priority - must be FIRST)
    application.add_handler(CallbackQueryHandler(handle_captcha_callback, pattern=r'^captcha_'))
    
    # General callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Chat member handlers
    application.add_handler(ChatMemberHandler(handle_new_member, ChatMemberHandler.CHAT_MEMBER))
    
    # Message handler (for filters)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    print("[Main] Bot started successfully!")
    print("[Main] Press Ctrl+C to stop")
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
