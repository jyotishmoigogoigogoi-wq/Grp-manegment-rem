# ˹ʀᴇᴍ˼ Bot — Complete Telegram Bot

Your ultimate anime & group management companion!

## Bot Identity

| Property | Value |
|----------|-------|
| Name | ˹ʀᴇᴍ˼ |
| Username | @RemNanoBot |
| Developer | YorichiiPrime (ID: 7728424218) |
| Platform | Render.com (Python) |
| Database | Neon PostgreSQL |

## Links

| Type | URL |
|------|-----|
| Channel | https://t.me/+g9uDSVO-mTI0Nzc9 |
| Group | https://t.me/kingchaos7 |
| Developer | https://t.me/YorichiiPrime |

## File Structure

```
rem_bot/
├── config.py          # Constants, links, formatting templates
├── database.py        # Neon DB connection & all queries
├── buttons.py         # All inline keyboard layouts
├── commands.py        # All command handlers (user/admin/owner/dev)
├── keep_alive.py      # Flask server to prevent Render sleep
├── main.py            # Entry point, bot initialization
├── requirements.txt   # Dependencies
└── README.md          # This file
```

## Features

### 1. Start Command (DM Only)
- Background image/video (set via dev command)
- Aesthetic box format with branding
- Stats: groups, users, commands
- 6 buttons: Help, Mimi Tunes, Channel, Support, My Lord, Add to Group

### 2. Replaceable Messages
- Every button click edits same message (no flood)
- Session tracking per user
- Back button returns to previous menu

### 3. Role-Based Menus

| Role | Access |
|------|--------|
| User | Anime search, profile, airing, top |
| Admin | + Mute, kick, ban, warn, purge, pin, lock |
| Owner | + Settings, welcome/goodbye toggle, captcha toggle, filters, promote/demote |
| Dev (you only) | + Set images/video, broadcast, stats, backup, restart |

### 4. Anime Features (Jikan API)
- `/anime <name>` — Full details with trailer button
- `/character <name>` — Character info
- `/airing` — Currently airing this season
- `/top` — Top anime
- Aesthetic formatting with box borders

### 5. Group Management
- Welcome/goodbye with custom images (you set)
- Captcha in DM (button/math/image modes)
- Anti-raid protection
- Full admin command set with reply-based targeting

### 6. Developer Zone
- `/setstartvideo` — Reply to video → sets start video
- `/sethelpimg` — Reply to image → sets help background
- `/devstats` — Full bot statistics
- `/broadcast` — Message all groups
- `/backup` — Export database
- `/restart` — Restart bot

## Aesthetic Format

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ˹ʀᴇᴍ˼  🤖                      ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  Content here                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Database Tables

- `users` — Global user data
- `groups` — Per-group settings
- `group_members` — Per-group user stats
- `user_sessions` — For replaceable messages
- `bot_config` — Dev settings (your video/image IDs)
- `captcha_sessions` — Active captchas
- `filters` — Group word filters
- `logs` — Admin action logs

## Render Setup

### Environment Variables

```bash
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=your_neon_postgresql_url_here
```

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
python main.py
```

### Instance Type
- **Free Tier**: Works on Render's free tier
- **Keep Alive**: Built-in Flask server prevents sleeping

## Commands Reference

### User Commands
| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help menu |
| `/anime <name>` | Search for anime |
| `/character <name>` | Search for character |
| `/airing` | Currently airing anime |
| `/top` | Top anime |
| `/profile` | Your profile |

### Admin Commands
| Command | Description |
|---------|-------------|
| `/mute` | Mute user (reply) |
| `/unmute` | Unmute user |
| `/kick` | Kick user |
| `/ban` | Ban user |
| `/unban <id>` | Unban user |
| `/warn` | Warn user |
| `/purge <n>` | Delete n messages |
| `/pin` | Pin message |
| `/unpin` | Unpin message |
| `/lock` | Lock chat |
| `/unlock` | Unlock chat |

### Owner Commands
| Command | Description |
|---------|-------------|
| `/settings` | Group settings |
| `/welcome` | Toggle welcome |
| `/goodbye` | Toggle goodbye |
| `/captcha` | Toggle captcha |
| `/filter <kw> <resp>` | Add filter |
| `/stopfilter <kw>` | Remove filter |
| `/promote` | Promote to admin |
| `/demote` | Demote admin |

### Developer Commands
| Command | Description |
|---------|-------------|
| `/setstartvideo` | Set start video (reply) |
| `/sethelpimg` | Set help image (reply) |
| `/devstats` | Bot statistics |
| `/broadcast` | Broadcast to all groups |
| `/backup` | Backup database |
| `/restart` | Restart bot |

## Deployment Steps

1. **Create Telegram Bot**
   - Message @BotFather
   - Create new bot
   - Get BOT_TOKEN

2. **Setup Neon Database**
   - Create account at neon.tech
   - Create new project
   - Get DATABASE_URL

3. **Deploy to Render**
   - Create new Web Service
   - Connect your GitHub repo
   - Set environment variables
   - Deploy!

4. **Configure Bot**
   - Send `/setstartvideo` (reply to video)
   - Send `/sethelpimg` (reply to image)
   - Done!

## License

This bot is proprietary software developed by YorichiiPrime.

## Support

For support, join: https://t.me/kingchaos7
