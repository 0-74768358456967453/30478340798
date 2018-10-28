import discord
import aiohttp
import asyncio
import asyncpg
import time
import config
import random
from datetime import datetime
from datetime import timezone
from discord import Game
from config import token, link, prefix, ownerid
from discord.ext.commands import Bot
from discord.ext import commands

client = Bot(prefix)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="for commands! | ..help", type = 3))
    servers = list(client.servers)
    print("----------------------")
    print("Logged in!")
    print("Username: %s"%client.user.name)
    print("ID: %s"%client.user.id)
    print("Connected on " + str(len(client.servers)) + " servers:")
    for x in range(len(servers)):
        print((''+servers[x-1].name).encode("utf8"))
    print("----------------------")

@client.event
async def is_nsfw(channel: discord.Channel):
    try:
        _gid = channel.server.id
    except AttributeError:
        return False
    data = await client.http.request(
        discord.http.Route(
            'GET', '/guilds/{guild_id}/channels', guild_id=_gid))
    channeldata = [d for d in data if d['id'] == channel.id][0]
    return channeldata['nsfw']

@client.command(pass_context=True)
async def help(ctx):
    embed=discord.Embed(title="", colour=0xFFFF)
    embed.add_field(name="Bot commands", value='''..help - Shows this message.
..creator - Displays the credit information.
..ping - Check the status of the bot.
..choose - Let the bot choose for you.
..coinflip - The bot will flip a coin for you.
..say - Bot will repeat whatever you type. (DISABLED, FOR NOW)
..youtube - Search for something on youtube.
..google - Search for something on google.
..nudity - Search for some juicy stuff. (WIP)
..botinvite - Get an invite for the bot.
..serverinvite - Get an invite for your server.
..bans - Display an embedded list of all banned users.
..serverinfo - Displays an embedded information of the server.
..msgpurge - Delete multiple messages at once.
..warn - Warn a user. (WIP)
..ban - Ban a user. (WIP)
..kick - Kick a user.
..mute - Mute a user.
..unmute - Unmute a user.
..report - Report a user.

Type ..help command for more info on a command. (WIP)
If something isn't working give the bots role the Aministrator permission.
If you need further assistance contact Drezy#1469 on discord.''', inline=False)
    embed.set_footer(text="Updated - 10/27/18 6:25PM [PST]")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def changelog(ctx):
    embed=discord.Embed(title="CHANGE LOG", colour=0xFFFF)
    embed.add_field(name="UPDATE v2.2", value='''- Disabled "say" command. (Trolling capabilties, will be fixed soon.)
    - Added changelog command and converted to an embedded message.
    - Added a porn command for those of you who like the juicy stuff.
    - Added a creator command to give credits.
    - Updated the report command so your command is deleted. (more discreat)
    - Added a google command for searching google.
    - Added help command with new commands and information.
    - Updated the bot invite command to an embedded message.
    - Added a broadcasting command so that I may make announcements if need be.
    - Updated the porn command for NSFW channels.
    **If you notice any mistakes contact Drezy#1469 on discord.**''', inline=False)
    embed.set_footer(text="Updated - 10/27/18 6:25PM [PST]")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def broadcast(ctx, *, msg):
    await client.delete_message(ctx.message)
    if ctx.message.author.id == "104001063148879872":
        for server in client.servers:
            for channel in server.channels:
                try:
                    await client.send_message(channel, msg)
                except Exception:
                    continue
                else:
                    break
                    await client.whisper("**Message has been broadcasted!**")
    else:
        await client.say("**Sorry, only the bot owner may use this command.**")

@client.command(pass_context=True)
async def nudity(ctx):
    channel_nsfw = await client.is_nsfw(ctx.message.channel)
    if channel_nsfw:
        embed=discord.Embed(title="Here you go (Searching Coming Soon)", colour=0xFFFF)
        embed.set_image(url="https://cdn.discordapp.com/attachments/431172765899292685/498558994105892865/owo_lol.png")
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="You're searching for porn? Not in this christian channel!", colour=0xFFFF)
        embed.set_image(url="https://cdn.discordapp.com/attachments/503790262208954378/505188771734618113/tenor.gif")
        await client.say(embed=embed)

@client.command(pass_context=True)
async def creator(ctx):
    embed=discord.Embed(title="", colour=0xFFFF)
    embed.add_field(name="Credits", value="This bot was created by Drezy#1469 with the help of users from the [BotDevelopment] discord, mainly including Wrong#4794", inline=False)
    await client.say(embed=embed)

@client.command()
async def ping():
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = time.time() - pingtime
    await client.edit_message(pingms, ":ping_pong:  time is `%.01f seconds`" % ping)

@client.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    await client.say(random.choice(choices))

@client.command(pass_context=True)
async def botinvite(ctx):
    embed=discord.Embed(title="Bot Invite", url='https://discordapp.com/api/oauth2/authorize?client_id=500090490180468736&permissions=2146561239&scope=bot', description="Click the above text to invite Mr. Clean to another discord server!", color=0XFFFF)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def serverinvite(ctx):
        inviteLink = await client.create_invite(destination = ctx.message.channel, xkcd = True, max_uses = 0)
        await client.whisper(inviteLink)
        await client.say("Check Your DM's :wink:")

@client.command(pass_context=True)
async def youtube(ctx):
    await client.send_typing(ctx.message.channel)
    args = ctx.message.content.split(" ")
    combargs = (" ".join(args[1:]))
    formatted = combargs.replace(" ", "+")
    em = discord.Embed(title=  (" ".join(args[1:])), url='https://www.youtube.com/results?search_query=%s' %(formatted), colour=0x439e1f)
    em.set_author(name= 'Search results for: ' + (combargs) ,icon_url='https://cdn.discordapp.com/attachments/486611168891502624/489191307441471488/580b57fcd9996e24bc43c545.png')
    em.set_footer(text='Search generated by: %s' %(ctx.message.author) , icon_url=ctx.message.author.avatar_url )
    await client.send_message(ctx.message.channel, embed=em )

@client.command(pass_context=True)
async def google(ctx):
    await client.send_typing(ctx.message.channel)
    args = ctx.message.content.split(" ")
    combargs = (" ".join(args[1:]))
    formatted = combargs.replace(" ", "+")
    em = discord.Embed(title=  (" ".join(args[1:])), url='https://www.google.com/search?ei=_WjSW7mKL8qR0wKitomYDw&q=%s' %(formatted), colour=0x439e1f)
    em.set_author(name= 'Search results for: ' + (combargs) ,icon_url='https://cdn.discordapp.com/attachments/503790262208954378/505183201552236574/5a951939c4ffc33e8c148af2.png')
    em.set_footer(text='Search generated by: %s' %(ctx.message.author) , icon_url=ctx.message.author.avatar_url )
    await client.send_message(ctx.message.channel, embed=em )

@client.command(pass_context = True)
async def saydis(ctx, *args):
    mesg = ' '.join(args)
    await client.delete_message(ctx.message)
    return await client.say(mesg)

@client.command(pass_context=True)
async def coinflip(ctx):
    pick = ['heads','tails']
    flip = random.choice(pick)
    await client.say ("Your coin landed on " + flip + '!')

@client.command(pass_context = True)
async def bans(ctx):
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of banned idiots", description = x, color=0xFFFFF)
    return await client.say(embed = embed)

@client.command(pass_context = True)
async def serverinfo(ctx):
    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];

    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', colour = 0xFFFF);
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text & Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);

#Clears The Chat

@client.command(pass_context = True)
async def msgpurge (ctx, amount=100):
  if ctx.message.author.server_permissions.manage_messages:
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
      messages.append(message)
    await client.delete_messages(messages)
    await client.whisper('''**Message(s) deleted.**''')
  else:
    await client.say("**You do not have permission to delete messages!**")

@client.command(pass_context = True)
async def warn(ctx, user="", reason="", mod="", n="", channel=""):
  if ctx.message.author.server_permissions.manage_messages:
    if user == "":
        await client.say(":x: No user Mentioned")
    if reason == "":
        await client.say(":x: No reason entered!")
    if mod == "":
        await client.say(":x: No Mod is Selected!")
    if n == "":
        await client.say(":x: No Warn Number was selected")
    if channel == "":
        await client.say(":x: No Channel entered!")
    channel = client.get_channel(channel)
    em = discord.Embed(color=0x42fc07)
    em.add_field(name='Warning', value=("You Have Been Warned -->"))
    em.add_field(name='User', value=(user))
    em.add_field(name='Reason', value=(reason))
    em.add_field(name='Moderator', value=(mod))
    em.set_footer(text="Warnings had : {}".format(n))
    await client.send_message(channel, embed=em)
  else:
    await client.say("**You do not have permission to warn!**")

@client.command(pass_context=True, hidden = True)
async def report(ctx, user: discord.Member, *, reason):

    author = ctx.message.author
    server = ctx.message.server

    joined_at = user.joined_at
    user_joined = joined_at.strftime("%D - %I:%M %p [UTC]")
    joined_on = "{}".format(user_joined)

    args = ''.join(reason)
    adminlist = []
    check = lambda r: r.name in ['Administrator' or 'Moderator' or 'Owner']

    members = server.members
    for i in members:

        role = bool(discord.utils.find(check, i.roles))

        if role is True:
            adminlist.append(i)
        else:
            pass

    colour = discord.Colour.magenta()

    description = "User Reported"
    data = discord.Embed(description=description, colour=colour)
    data.add_field(name="Reason Reported:", value=reason)
    data.add_field(name="Report By:", value=author)
    data.add_field(name="User Join Date:", value=joined_on)
    data.set_footer(text="User ID: {}".format(user.id))

    name = str(user)
    name = " ~ ".join((name, user.nick)) if user.nick else name

    if user.avatar_url:
        data.set_author(name=name, url=user.avatar_url)
        data.set_thumbnail(url=user.avatar_url)
    else:
        data.set_author(name=name)

    for i in adminlist:
        await client.delete_message(ctx.message)
        await client.whisper("**Thank you, User reported!**")
        await client.send_message(i, embed=data)

@client.command(pass_context = True)
async def ban(ctx, *, member : discord.Member = None, days = " "):
  if ctx.message.author.server_permissions.ban_members:
    try:
        if member == None:
            await client.say(ctx.message.author.mention + ", please specify a user to ban!")
            return

        if member.id == ctx.message.author.id:
            await client.say(ctx.message.author.mention + ", you cannot ban yourself!")
            return
        else:
            await client.ban(member, days)

    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")

    embed = discord.Embed(description = "**%s** has been banned!"%member.name, color = 0xF00000)
    embed.set_footer(text="Reason:" + reason + ".")
    await client.say(embed = embed)
  else:
    await client.say("**You do not have permission to kick!**")

#Kick a Member From The Server

@client.command(pass_context = True)
async def kick(ctx, *, member : discord.Member = None):
  if ctx.message.author.server_permissions.kick_members:
    try:
        if member == None:
            await client.say(ctx.message.author.mention + ", please specify a member to kick!")
            return

        if member.id == ctx.message.author.id:
            await client.say(ctx.message.author.mention + ", you cannot kick yourself!")
            return
        else:
            await client.kick(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")

    embed = discord.Embed(description = "**%s** has been kicked."%member.name, color = 0xF00000)
    embed.set_footer(text="Cleaned up an oopsy!")
    await client.say(embed = embed)
  else:
    await client.say("**You do not have permission to kick!**")


#Mutes a Member From The server

@client.command(pass_context = True)
async def mute(ctx, *, member : discord.Member):
  if ctx.message.author.server_permissions.mute_members:

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await client.say("**%s** is now Muted! You must wait For an unmute.."%member.mention)
  else:
    await client.say("**You do not have permission to mute!**")

#Unmutes a member

@client.command(pass_context = True)
async def unmute(ctx, *, member : discord.Member):
  if ctx.message.author.server_permissions.mute_members:

    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)

    await client.say("**%s** Time is up...You are now unmuted!"%member.mention)
  else:
    await client.say("**You do not have permission to unmute!**")

client.run(token)
