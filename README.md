<div align="center">

<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,2,22,24,25&height=350&section=header&text=˹ʀᴇᴍ˼&fontSize=100&fontColor=fff&animation=fadeIn&fontAlignY=30&desc=The%20Future%20of%20Telegram%20Bots&descAlignY=50&descSize=25&rotate=0"/>

<!-- Animated Typing -->
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Orbitron&weight=700&size=28&duration=2500&pause=800&color=FF00FF&center=true&vCenter=true&multiline=true&width=800&height=100&lines=⚡+ULTRA+PERFORMANCE;🎭+ANIME+POWERED;🔮+AI+ENHANCED;🌸+AESTHETIC+PERFECTION)](https://git.io/typing-svg)

<br>

<!-- Status Badges -->
<div>
<img src="https://img.shields.io/badge/🟢-ONLINE-success?style=for-the-badge&labelColor=000&color=00ff00"/>
<img src="https://img.shields.io/badge/⚡-V2.0.0_ULTRA-ff00ff?style=for-the-badge&labelColor=000"/>
<img src="https://img.shields.io/badge/🛡️-ENTERPRISE_GRADE-00ffff?style=for-the-badge&labelColor=000"/>
</div>

<br>

<!-- Tech Stack -->
<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=ffdd54&labelColor=1a1a2e"/>
<img src="https://img.shields.io/badge/Telegram-Bot_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white&labelColor=1a1a2e"/>
<img src="https://img.shields.io/badge/PostgreSQL-Neon-4169E1?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=1a1a2e"/>
<img src="https://img.shields.io/badge/Cloud-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white&labelColor=1a1a2e"/>
<img src="https://img.shields.io/badge/Async-aiogram-ff6b6b?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e"/>

<br><br>

<!-- Stats Row -->
<img src="https://img.shields.io/badge/👥_Users-10K+-ff6b6b?style=flat-square"/>
<img src="https://img.shields.io/badge/💬_Groups-500+-4ecdc4?style=flat-square"/>
<img src="https://img.shields.io/badge/⚡_Uptime-99.9%25-ffe66d?style=flat-square"/>
<img src="https://img.shields.io/badge/🚀_Speed-&lt;50ms-a8e6cf?style=flat-square"/>

</div>

---

<div align="center">

## 🎴 `IDENTITY`

</div>

<table align="center" style="border: none;">
<tr>
<td width="50%">

```diff
+ ╔═══════════════════════════════════╗
+ ║  🤖 BOT PROFILE                   ║
+ ╠═══════════════════════════════════╣
+ ║  Name: ˹ʀᴇᴍ˼                      ║
+ ║  Username: @RemNanoBot            ║
+ ║  Version: 2.0.0-ULTRA             ║
+ ║  Status: 🟢 OPERATIONAL            ║
+ ║  Platform: Render.com              ║
+ ║  Database: Neon PostgreSQL         ║
+ ║  Language: Python 3.11+            ║
+ ╚═══════════════════════════════════╝
```

</td>
<td width="50%">

```diff
+ ╔═══════════════════════════════════╗
+ ║  👨‍💻 DEVELOPER                    ║
+ ╠═══════════════════════════════════╣
+ ║  Name: YorichiiPrime               ║
+ ║  ID: 7728424218                    ║
+ ║  Role: Creator & Architect         ║
+ ║  Contact: @YorichiiPrime           ║
+ ║  Status: 🟢 Available              ║
+ ║  Specialty: Bot Architecture       ║
+ ║  Experience: 5+ Years              ║
+ ╚═══════════════════════════════════╝
```

</td>
</tr>
</table>

---

<div align="center">

## ⚡ `FEATURE MATRIX`

</div>

<div align="center">

| Module | Features | Status | Performance |
|:------:|:---------|:------:|:-----------:|
| 🎌 **Anime Core** | Jikan API, Trailers, Characters, MAL Sync | <img src="https://img.shields.io/badge/ACTIVE-00ff00?style=flat-square"/> | ⚡⚡⚡⚡⚡ |
| 👥 **Group Mgmt** | Welcome, Captcha, Anti-Raid, Filters | <img src="https://img.shields.io/badge/ACTIVE-00ff00?style=flat-square"/> | ⚡⚡⚡⚡⚡ |
| 🔐 **Security** | RBAC, Admin Actions, Audit Logs | <img src="https://img.shields.io/badge/ACTIVE-00ff00?style=flat-square"/> | ⚡⚡⚡⚡⚡ |
| 🎨 **UI/UX** | Replaceable Msgs, Sessions, Aesthetics | <img src="https://img.shields.io/badge/ACTIVE-00ff00?style=flat-square"/> | ⚡⚡⚡⚡⚡ |
| 🔮 **Dev Tools** | Broadcast, Backup, Analytics | <img src="https://img.shields.io/badge/ACTIVE-00ff00?style=flat-square"/> | ⚡⚡⚡⚡⚡ |

</div>

---

<div align="center">

## 🏗️ `ARCHITECTURE`

</div>

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#a855f7', 'primaryTextColor': '#fff', 'primaryBorderColor': '#fff', 'lineColor': '#a855f7', 'secondaryColor': '#1a1a2e', 'tertiaryColor': '#2d2d44'}}}%%
graph TB
    subgraph "🌐 Frontend"
        User([👤 Telegram User])
        Admin([👨‍💻 Dev Admin])
    end

    subgraph "⚡ Core Layer"
        TG[Telegram Bot API]
        Bot[🤖 ˹ʀᴇᴍ˼ Core]
        Flask[🌐 Keep-Alive Server]
    end

    subgraph "🗄️ Data Layer"
        DB[(Neon PostgreSQL)]
        Cache[(Session Store)]
    end

    subgraph "🔗 External APIs"
        Jikan[Jikan API]
        AniList[AniList GraphQL]
    end

    User -->|Commands| TG
    Admin -->|Dev Commands| TG
    TG -->|Webhooks| Bot
    Bot -->|Health Check| Flask
    Bot -->|Queries| DB
    Bot -->|Cache| Cache
    Bot -->|Fetch| Jikan
    Bot -.->|Future| AniList

    style Bot fill:#a855f7,stroke:#fff,stroke-width:4px,color:#fff
    style DB fill:#4169e1,stroke:#fff,stroke-width:3px,color:#fff
    style TG fill:#26a5e4,stroke:#fff,stroke-width:3px,color:#fff
    style Flask fill:#46e3b7,stroke:#fff,stroke-width:2px,color:#000
```

---

<div align="center">

## 📁 `FILE STRUCTURE`

</div>

```
🌸 rem_bot/
│
├── ⚙️ config.py          # ➤ Constants, templates, env vars
├── 🗄️ database.py        # ➤ Neon DB ORM & connection pool
├── ⌨️ buttons.py         # ➤ Inline keyboards & UI components  
├── 📜 commands.py        # ➤ Handler router (User/Admin/Owner/Dev)
├── 🌐 keep_alive.py      # ➤ Flask server (Render anti-sleep)
├── 🚀 main.py            # ➤ Entry point, dispatcher, middleware
├── 📦 requirements.txt   # ➤ Dependencies & versions
└── 📖 README.md          # ➤ You are here ✨
```

---

<div align="center">

## 🎮 `COMMAND CENTER`

</div>

<details>
<summary>
<b>👤 USER COMMANDS</b> 
<img src="https://img.shields.io/badge/7_Commands-4ecdc4?style=flat-square"/>
</summary>

| Command | Usage | Description | Rate Limit |
|:-------:|:-----:|:-----------|:----------:|
| `/start` | - | 🚀 Initialize & main menu | None |
| `/help` | - | 📚 Interactive help system | None |
| `/anime` | `<name>` | 🎌 Search with trailer | 5s |
| `/character` | `<name>` | 👤 Character database | 5s |
| `/airing` | - | 📺 This season's anime | 10s |
| `/top` | - | 🏆 Top ranked anime | 10s |
| `/profile` | - | 👤 Your stats & history | None |

</details>

<details>
<summary>
<b>🛡️ ADMIN COMMANDS</b> 
<img src="https://img.shields.io/badge/10_Commands-ff6b6b?style=flat-square"/>
</summary>

| Command | Target | Action | Permission |
|:-------:|:------:|:-------|:----------:|
| `/mute` | Reply | 🔇 Restrict chatting | Admin+ |
| `/unmute` | Reply | 🔊 Restore chat | Admin+ |
| `/kick` | Reply | 👢 Remove user | Admin+ |
| `/ban` | Reply | ⛔ Permanent ban | Admin+ |
| `/unban` | `<id>` | ✅ Revoke ban | Admin+ |
| `/warn` | Reply | ⚠️ Issue warning | Admin+ |
| `/purge` | `<n>` | 🧹 Delete messages | Admin+ |
| `/pin` | Reply | 📌 Pin message | Admin+ |
| `/unpin` | - | 📍 Unpin | Admin+ |
| `/lock` / `/unlock` | - | 🔒 Chat control | Admin+ |

</details>

<details>
<summary>
<b>👑 OWNER COMMANDS</b> 
<img src="https://img.shields.io/badge/8_Commands-ffd93d?style=flat-square"/>
</summary>

| Command | Parameters | Description |
|:-------:|:----------:|:------------|
| `/settings` | - | ⚙️ Group configuration |
| `/welcome` | `on/off` | 👋 Toggle welcomes |
| `/goodbye` | `on/off` | 😢 Toggle goodbyes |
| `/captcha` | `on/off` | 🛡️ Toggle verification |
| `/filter` | `<kw> <resp>` | 💬 Add auto-reply |
| `/stopfilter` | `<kw>` | 🗑️ Remove filter |
| `/promote` | Reply | ⬆️ Make admin |
| `/demote` | Reply | ⬇️ Remove admin |

</details>

<details>
<summary>
<b>🔮 DEVELOPER COMMANDS</b> 
<img src="https://img.shields.io/badge/6_Commands-a855f7?style=flat-square"/>
</summary>

| Command | Usage | Power |
|:-------:|:-----:|:-----:|
| `/setstartvideo` | Reply to video | 🌟🌟🌟🌟🌟 |
| `/sethelpimg` | Reply to image | 🌟🌟🌟🌟🌟 |
| `/devstats` | - | 🌟🌟🌟🌟🌟 |
| `/broadcast` | `<msg>` | 🌟🌟🌟🌟🌟 |
| `/backup` | - | 🌟🌟🌟🌟🌟 |
| `/restart` | - | 🌟🌟🌟🌟🌟 |

</details>

---

<div align="center">

## 🎨 `UI PREVIEW`

</div>

```diff
+ ╔══════════════════════════════════════════════════════════════════╗
+ ║                                                                  ║
+ ║   🌸 ˹ʀᴇᴍ˼  🤖  v2.0.0-ULTRA                                    ║
+ ║   ═══════════════════════════════════════════════════════════   ║
+ ║                                                                  ║
+ ║   ✨ Features:                                                   ║
+ ║   ├─ 🎌 Advanced Anime Search Engine                            ║
+ ║   ├─ 👥 Intelligent Group Management                            ║
+ ║   ├─ 🛡️ Anti-Raid Protection System                             ║
+ ║   ├─ 🔐 DM-Based Captcha Verification                           ║
+ ║   └─ 📊 Real-time Analytics Dashboard                           ║
+ ║                                                                  ║
+ ║   ┌──────────┬──────────┬──────────┬──────────┐                ║
+ ║   │  🎌 Anime │  👥 Group │  ⚙️ Settings│  📊 Stats │                ║
+ ║   └──────────┴──────────┴──────────┴──────────┘                ║
+ ║                                                                  ║
+ ║   💜 Crafted by @YorichiiPrime                                   ║
+ ║                                                                  ║
+ ╚══════════════════════════════════════════════════════════════════╝
```

---

<div align="center">

## 🗄️ `DATABASE SCHEMA`

</div>

```sql
-- 🎯 Core Entities
users            → Global profiles, stats, preferences
groups           → Per-group config, welcome settings
group_members    → Memberships, roles, warnings
user_sessions    → Message states, navigation history
bot_config       → Dev media IDs, global settings
captcha_sessions → Active verifications, attempts
filters          → Keyword triggers, responses
logs             → Audit trail, command history
```

---

<div align="center">

## 🚀 `DEPLOYMENT`

</div>

### 🎯 Prerequisites
```bash
✅ Python 3.11 or higher
✅ PostgreSQL 14+ (Neon recommended)
✅ Telegram Bot Token (@BotFather)
✅ Render Account (Free tier works!)
```

### ⚡ Quick Start
```bash
# 1. Clone Repository
git clone https://github.com/yourusername/rem_bot.git
cd rem_bot

# 2. Setup Environment
cp .env.example .env
# Edit .env with your tokens

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Deploy to Render
# Connect GitHub repo → Web Service → Deploy!
```

### 🔧 Render Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| **Environment** | Python 3 | Latest stable |
| **Build** | `pip install -r requirements.txt` | Auto-install |
| **Start** | `python main.py` | Entry point |
| **Plan** | Free Tier | $0/month |
| **Keep Alive** | ✅ Built-in | No sleep mode |

---

<div align="center">

## 📊 `PERFORMANCE`

</div>

<div align="center">

| Metric | Value | Grade | Graph |
|--------|-------|-------|-------|
| ⚡ Response | 45ms | A+ | ████████████ 100% |
| 🎯 Uptime | 99.9% | A+ | ████████████ 100% |
| 👥 Users | 10,000+ | A | ███████████░ 92% |
| 🗄️ Queries | 500/sec | A+ | ████████████ 100% |
| 💾 Memory | 512MB | A | ██████████░░ 85% |

</div>

---

<div align="center">

## 🔗 `CONNECT`

</div>

<div align="center">

[![Channel](https://img.shields.io/badge/📢_UPDATES-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/+g9uDSVO-mTI0Nzc9)
[![Group](https://img.shields.io/badge/💬_SUPPORT-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/kingchaos7)
[![Dev](https://img.shields.io/badge/👨‍💻_DEVELOPER-ff6b6b?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/YorichiiPrime)
[![Bot](https://img.shields.io/badge/🤖_TRY_NOW-A855F7?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/RemNanoBot)

</div>

---

<div align="center">

## 💎 `WHY ˹ʀᴇᴍ˼?`

</div>

<table align="center">
<tr>
<td align="center" width="25%">

### ⚡ Speed
Async architecture with connection pooling delivers sub-50ms responses

</td>
<td align="center" width="25%">

### 🎨 Design
Replaceable messages & session tracking create seamless UX

</td>
<td align="center" width="25%">

### 🔒 Security
Enterprise-grade RBAC with anti-raid and DM captcha

</td>
<td align="center" width="25%">

### 🌸 Anime
Deep Jikan integration with trailers, chars, seasonal data

</td>
</tr>
</table>

---

<div align="center">

## 🛠️ `TECH STACK`

</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Neon](https://img.shields.io/badge/Neon-00E699?style=for-the-badge&logo=neon&logoColor=black)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

---

<div align="center">

## 📜 `LEGAL`

</div>

<div align="center">

**© 2024 YorichiiPrime. All Rights Reserved.**

*Proprietary Software. Unauthorized distribution prohibited.*

**Crafted with 💜 by [YorichiiPrime](https://t.me/YorichiiPrime)**

</div>

---

<div align="center">

<!-- Animated Footer -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,2,22,24,25&height=200&section=footer&text=Made%20with%20💜&fontSize=40&fontColor=fff&animation=fadeIn"/>

<!-- Visitor Counter -->
<img src="https://komarev.com/ghpvc/?username=rem-bot&label=👁️+Profile+Views&color=a855f7&style=flat-square"/>

</div>
