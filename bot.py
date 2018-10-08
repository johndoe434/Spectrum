import discord, asyncio, time, datetime, random, json, aiohttp, logging, os
from discord.ext import commands
from time import ctime
from os import listdir
from os.path import isfile, join

lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
no_py = [s.replace('.py', '') for s in lst]
startup_extensions = ["cogs." + no_py for no_py in no_py]

with open("databases/thesacredtexts.json") as f:
    config = json.load(f)

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("$"),
                              owner_id=276707898091110400,
                              case_insensitive=True)
    
bot.remove_command("help")
bot.launch_time = datetime.datetime.utcnow()

url = "https://discordbots.org/api/bots/320590882187247617/stats"
headers = {"Authorization" : config["tokens"]["dbltoken"]}

def is_owner(ctx):
        if ctx.message.author.id == bot.owner_id:
            return True
        return False

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def update_activity():
    await bot.change_presence(
        activity=discord.Activity(
            name=f"@Spectrum help | {len(bot.guilds)} guilds!",
            type=1,
            url="https://www.twitch.tv/SpectrixYT"))

    payload = {"server_count"  : len(bot.guilds)}

    async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(
                url,
                data=payload,
                headers=headers)

@bot.event
async def on_ready():
    print("=========\nConnected\n=========\n")
    await update_activity()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command()
async def uptime(ctx):
    delta_uptime = datetime.datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

@bot.event
async def on_guild_join(guild):
    await update_activity()
    try:
        embed = discord.Embed(color=discord.Color(value=0x36393e))
        embed.set_author(name="Here's some stuff to get you started:")
        embed.add_field(name="Prefix", value="`$`, or **just mention me!**")
        embed.add_field(name="Command help", value="[Documentation](https://spectrix.me/spectrum/)")
        embed.add_field(name="Support Server", value="[Join, it's quite fun here](https://discord.gg/SuN49rm)")
        embed.add_field(name="Upvote", value="[Click here](https://discordbots.org/bot/320590882187247617/vote)")
        embed.set_thumbnail(url=config["styling"]["gifLogo"])
        embed.set_footer(text=f"Thanks to you, Spectrum is now on {len(bot.guilds)} servers! <3", icon_url=config["styling"]["normalLogo"])
        await guild.system_channel.send(content="**Hello World! Thanks for inviting me! :wave: **", embed=embed)
    except Exception:
        pass

@bot.event
async def on_guild_remove(guild):
    await update_activity()

if __name__ == '__main__':

    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(config["tokens"]["token"])