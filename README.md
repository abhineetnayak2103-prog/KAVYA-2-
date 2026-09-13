# 🤖 KAVYA - Discord Moderation Bot

A powerful Discord moderation bot with owner admin management features.

## ✨ Features

### 👑 Owner Commands
- `!addadmin @user` - Add a user as admin
- `!removeadmin @user` - Remove admin
- `!admins` - List all admins

### ⚔️ Moderation Commands (Admin+)
- `!kick @user [reason]` - Kick user from server
- `!ban @user [reason]` - Ban user from server
- `!mute @user [reason]` - Mute user (removes chat access)
- `!unmute @user` - Unmute user
- `!clear [number]` - Delete messages from channel

### 📖 Other
- `!help` - Show all commands

## 🚀 Setup

### 1. Create Discord Bot
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Click "New Application"
- Go to "Bot" section and click "Add Bot"
- Copy your bot token

### 2. Give Bot Permissions
- Go to OAuth2 > URL Generator
- Select scopes: `bot`
- Select permissions:
  - Send Messages
  - Manage Messages
  - Kick Members
  - Ban Members
  - Manage Roles
- Copy the generated URL and open it to invite bot to your server

### 3. Clone and Setup
```bash
git clone https://github.com/abhineetnayak2103-prog/KAVYA-2-.git
cd KAVYA-2-
pip install -r requirements.txt
```

### 4. Create `.env` file
```
DISCORD_TOKEN=your_bot_token_here
OWNER_ID=your_discord_user_id_here
```

Get your Discord ID:
- Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
- Right-click your username and click "Copy User ID"

### 5. Run Bot Locally
```bash
python main.py
```

## 🌐 Deploy on Railway

### Option 1: Easy Deploy
1. Go to [railway.app](https://railway.app)
2. Create new project
3. Connect your GitHub repo
4. Add environment variables in Railway dashboard:
   - `DISCORD_TOKEN` - Your bot token
   - `OWNER_ID` - Your Discord ID
5. Deploy!

### Option 2: Manual Deploy
```bash
railway link
railway up
```

## 📝 Usage Examples

```
# Add admin
!addadmin @john

# Kick user
!kick @spammer breaking rules

# Mute user
!mute @annoying_user spam

# Clear 50 messages
!clear 50

# List admins
!admins
```

## 🔒 Security
- Only owner can add/remove admins
- Only owner/admins can use moderation commands
- Admin list is saved to `admins.json`

## 📦 Requirements
- Python 3.11+
- discord.py 2.3.2+
- python-dotenv

## 🤝 Contributing
Feel free to fork and submit pull requests!

## 📄 License
MIT License

---

**Made with ❤️ by KAVYA Bot**
