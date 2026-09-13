import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', '0'))

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Store admins in memory (you can replace with database later)
admins = set()

# Load admins from file if exists
def load_admins():
    global admins
    if os.path.exists('admins.json'):
        with open('admins.json', 'r') as f:
            admins = set(json.load(f))

# Save admins to file
def save_admins():
    with open('admins.json', 'w') as f:
        json.dump(list(admins), f)

@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')
    print(f'🤖 Bot is ready!')
    load_admins()

# ====== OWNER COMMANDS ======

@bot.command(name='addadmin')
async def add_admin(ctx, user: discord.User):
    """Add a user as admin (Owner only)"""
    if ctx.author.id != OWNER_ID:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="Only the server owner can add admins!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    if user.id in admins:
        embed = discord.Embed(
            title="⚠️ Already Admin",
            description=f"{user.mention} is already an admin!",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        return
    
    admins.add(user.id)
    save_admins()
    embed = discord.Embed(
        title="✅ Admin Added",
        description=f"{user.mention} has been added as admin!",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='removeadmin')
async def remove_admin(ctx, user: discord.User):
    """Remove a user from admin (Owner only)"""
    if ctx.author.id != OWNER_ID:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="Only the server owner can remove admins!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    if user.id not in admins:
        embed = discord.Embed(
            title="⚠️ Not an Admin",
            description=f"{user.mention} is not an admin!",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        return
    
    admins.discard(user.id)
    save_admins()
    embed = discord.Embed(
        title="✅ Admin Removed",
        description=f"{user.mention} has been removed from admins!",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='admins')
async def list_admins(ctx):
    """List all admins"""
    if not admins:
        embed = discord.Embed(
            title="📋 Admin List",
            description="No admins added yet!",
            color=discord.Color.blue()
        )
    else:
        admin_list = '\n'.join([f"<@{admin_id}>" for admin_id in admins])
        embed = discord.Embed(
            title="📋 Admin List",
            description=admin_list,
            color=discord.Color.blue()
        )
    
    await ctx.send(embed=embed)

# ====== MODERATION COMMANDS ======

@bot.command(name='kick')
async def kick(ctx, user: discord.User, *, reason="No reason provided"):
    """Kick a user from the server (Admin only)"""
    if ctx.author.id != OWNER_ID and ctx.author.id not in admins:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You need admin permission to use this command!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    try:
        await ctx.guild.kick(user, reason=reason)
        embed = discord.Embed(
            title="👢 User Kicked",
            description=f"{user.mention} has been kicked!\n**Reason**: {reason}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(
            title="❌ Error",
            description="I don't have permission to kick this user!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name='ban')
async def ban(ctx, user: discord.User, *, reason="No reason provided"):
    """Ban a user from the server (Admin only)"""
    if ctx.author.id != OWNER_ID and ctx.author.id not in admins:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You need admin permission to use this command!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    try:
        await ctx.guild.ban(user, reason=reason)
        embed = discord.Embed(
            title="🚫 User Banned",
            description=f"{user.mention} has been banned!\n**Reason**: {reason}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(
            title="❌ Error",
            description="I don't have permission to ban this user!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name='mute')
async def mute(ctx, user: discord.User, *, reason="No reason provided"):
    """Mute a user (Admin only)"""
    if ctx.author.id != OWNER_ID and ctx.author.id not in admins:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You need admin permission to use this command!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted")
    
    member = await ctx.guild.fetch_member(user.id)
    await member.add_roles(mute_role, reason=reason)
    embed = discord.Embed(
        title="🔇 User Muted",
        description=f"{user.mention} has been muted!\n**Reason**: {reason}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name='unmute')
async def unmute(ctx, user: discord.User):
    """Unmute a user (Admin only)"""
    if ctx.author.id != OWNER_ID and ctx.author.id not in admins:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You need admin permission to use this command!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if mute_role:
        member = await ctx.guild.fetch_member(user.id)
        await member.remove_roles(mute_role)
        embed = discord.Embed(
            title="🔊 User Unmuted",
            description=f"{user.mention} has been unmuted!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

@bot.command(name='clear')
async def clear(ctx, amount: int):
    """Delete messages (Admin only)"""
    if ctx.author.id != OWNER_ID and ctx.author.id not in admins:
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You need admin permission to use this command!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(
        title="🗑️ Messages Cleared",
        description=f"Deleted {amount} messages!",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Show all available commands"""
    embed = discord.Embed(
        title="📖 Command List",
        description="Here are all available commands:",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="👑 Owner Commands", value=
        "`!addadmin @user` - Add admin\n"
        "`!removeadmin @user` - Remove admin\n"
        "`!admins` - List all admins",
        inline=False
    )
    
    embed.add_field(name="⚔️ Moderation Commands (Admin+)", value=
        "`!kick @user [reason]` - Kick user\n"
        "`!ban @user [reason]` - Ban user\n"
        "`!mute @user [reason]` - Mute user\n"
        "`!unmute @user` - Unmute user\n"
        "`!clear [number]` - Clear messages",
        inline=False
    )
    
    embed.set_footer(text="🤖 KAVYA Moderation Bot v1.0")
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
