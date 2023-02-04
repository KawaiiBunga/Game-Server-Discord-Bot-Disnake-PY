import disnake
from disnake.ext import tasks, commands
import aiohttp
import datetime
import json

# Import data from config file
with open('config.json') as f:
    data = json.load(f)
    token = data["token"]
    game = data["Game"]
    serverName = data["serverName"]
    Status = data["StatusText"]
    iconURL = data["iconURL"]
    website = data["website"]
    BM_ServerID = data["BM_ServerID"]

#Battlemetrics API Call
url = "https://api.battlemetrics.com/servers/" + str(BM_ServerID)
uptime_url = "https://api.battlemetrics.com/servers/" + str(BM_ServerID) + "/relationships/outages"

# Global cmd registration, sent .sync_commands_debug to false once in production
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = False

bot = commands.Bot(
    command_prefix = disnake.ext.commands.when_mentioned,
    command_sync_flags = command_sync_flags,
)

#Updating status from BM API
@tasks.loop(seconds=20)
async def presence():
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    #Get data from API response
                    resp_dict = json.loads(await resp.text())
                    status = resp_dict["data"]["attributes"]["status"] 
                    Player_Count = resp_dict["data"]["attributes"]["players"] 
                    Max_Players = resp_dict["data"]["attributes"]["maxPlayers"]
                    #If server is online, set status
                    if status == "online":
                        statusText = disnake.Game(name = f'{Status} {Player_Count}/{Max_Players}')
                        await bot.change_presence(activity=statusText)
                    #If BM API error, set status as 'BM ERROR' and send API error response in console
                    else:
                        statusText = disnake.Game(name = f'BM ERROR')
                        await bot.change_presence(activity=statusText)
                        print(f"Battlemetrics Error with status code: {resp.status}, please check your config")

# On ready event
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f'The bot is ready! Logged in as {bot.user}')
    presence.start()
    
# Slash commands

#Status command
@bot.slash_command(
    name = "status",
    description = f"Shows {serverName}'s status")
async def status(inter):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                #Get data from API response
                resp_dict = json.loads(await resp.text())
                status = resp_dict["data"]["attributes"]["status"] 
                PlayerCount = resp_dict["data"]["attributes"]["players"] 
                MaxPlayers = resp_dict["data"]["attributes"]["maxPlayers"]
                name = resp_dict["data"]["attributes"]["name"]
                ip = resp_dict["data"]["attributes"]["ip"]
                port = resp_dict["data"]["attributes"]["port"]
                #If server is online, send Embed
                if status == "online":
                    embed = disnake.Embed(
                        title = f'Server is {status}',
                        colour = 0x009FF,
                        timestamp=datetime.datetime.now(),
                    )
                    embed.set_author(
                        name = serverName + ' Bot',
                        url = website,
                        icon_url = iconURL,
                    )
                    embed.set_footer(
                    text = "Sent by " + serverName + " Bot",
                    icon_url = iconURL,
                    )

                    embed.add_field(name = "**Connect -**", value = f'{ip}:{port}', inline = False)
                    embed.add_field(name = "**Server -**", value = name, inline=False)
                    embed.add_field(name = "**Player Count -**", value = f'{PlayerCount}/{MaxPlayers}', inline=False)

                    await inter.send(embed=embed)

                else:
                    #If server is offline, send error code from BM
                    print(f"Battlemetrics Error with status code: {resp.status}")
                    await inter.send('BM ERROR')
         
#Locate command
@bot.slash_command(
    name = "locate",
    description = f"Shows {serverName}'s location")
async def status(inter):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                #Get data from API response
                resp_dict = json.loads(await resp.text())
                status = resp_dict["data"]["attributes"]["status"] 
                country = resp_dict["data"]["attributes"]["country"] 
                coord = resp_dict["data"]["attributes"]["location"] 
                #If server is online, send Embed
                if status == "online":
                    embed = disnake.Embed(
                        title = f"{serverName}'s Location:",
                        colour = 0x009FF,
                        timestamp=datetime.datetime.now(),
                    )
                    embed.set_author(
                        name = serverName + ' Bot',
                        url = website,
                        icon_url = iconURL,
                    )
                    embed.set_footer(
                    text = "Sent by " + serverName + " Bot",
                    icon_url = iconURL,
                    )

                    embed.add_field(name = "**Country -**", value = f'{country}', inline = False)
                    embed.add_field(name = "**Coordinates -**", value = f'{coord}', inline = False)
                    
                    await inter.send(embed=embed)

                else:
                    #Send error if occurs
                    print(f"Battlemetrics Error with status code: {resp.status}")
                    await inter.send('BM ERROR')

#Rank command
@bot.slash_command(
    name = "rank",
    description = f"Shows {serverName}'s Battlemetrics Rank")
async def status(inter):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                #Get data from API response
                resp_dict = json.loads(await resp.text())
                status = resp_dict["data"]["attributes"]["status"] 
                id = resp_dict["data"]["attributes"]["id"]  
                rank = resp_dict["data"]["attributes"]["rank"]   
                #If server is online, send Embed
                if status == "online":
                    embed = disnake.Embed(
                        title = f"{serverName}'s BattleMetrics Rank:",
                        colour = 0x009FF,
                        timestamp=datetime.datetime.now(),
                    )
                    embed.set_author(
                        name = serverName + ' Bot',
                        url = website,
                        icon_url = iconURL,
                    )
                    embed.set_footer(
                    text = "Sent by " + serverName + " Bot",
                    icon_url = iconURL,
                    )

                    embed.add_field(name = "**Server Rank -**", value = f'Server {id} is ranked {rank} on BattleMetrics', inline = False)
                    embed.add_field(name = "**BattleMetrics Link -**", value = f'https://www.battlemetrics.com/servers/{game}/{id}', inline = False)
                    
                    await inter.send(embed=embed)

                else:
                    #Send error if occurs
                    print(f"Battlemetrics Error with status code: {resp.status}")
                    await inter.send('BM ERROR')

#Uptime command
@bot.slash_command(
    name = "uptime",
    description = f"Shows {serverName}'s uptime")
async def status(inter):
    async with aiohttp.ClientSession() as session:
        async with session.get(uptime_url) as resp:
            if resp.status == 200:
                #Get data from API response
                resp_dict = json.loads(await resp.text())
                last_crash_start = resp_dict["data"][int('0')]["attributes"]["start"]
 
                #If server is online, send Embed
                if status == "online":
                    embed = disnake.Embed(
                        title = f"{serverName}'s BattleMetrics Rank:",
                        colour = 0x009FF,
                        timestamp=datetime.datetime.now(),
                    )
                    embed.set_author(
                        name = serverName + ' Bot',
                        url = website,
                        icon_url = iconURL,
                    )
                    embed.set_footer(
                    text = "Sent by " + serverName + " Bot",
                    icon_url = iconURL,
                    )

                    embed.add_field(name = "**Online Since -**", value = f'{serverName} last went offline {last_crash_start}', inline = False)
                           
                    await inter.send(embed=embed)

                else:
                    #Send error if occurs
                    print(f"Battlemetrics Error with status code: {resp.status}")
                    await inter.send('BM ERROR')

bot.run(token)
