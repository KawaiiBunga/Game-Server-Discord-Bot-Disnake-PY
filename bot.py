import disnake
from disnake.ext import tasks, commands
import aiohttp
import datetime
import json
import requests

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

#Battlemetrics API URL's
url = "https://api.battlemetrics.com/servers/" + str(BM_ServerID)
uptime_url = "https://api.battlemetrics.com/servers/" + str(BM_ServerID) + "/relationships/outages"


# Global cmd registration, set .sync_commands_debug to false once in production
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = False

bot = commands.Bot(
    command_prefix = disnake.ext.commands.when_mentioned,
    command_sync_flags = command_sync_flags,
)

#Convert/format time for API output
def time_conversion(seconds):
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    months, weeks = divmod(weeks, 4)
    years, months = divmod(months, 12)

    time_units = [f"{years} year(s)" if years else None,
                  f"{months} month(s)" if months else None,
                  f"{weeks} week(s)" if weeks else None,
                  f"{days} day(s)" if days else None,
                  f"{hours} hour(s)" if hours else None,
                  f"{minutes} minute(s)" if minutes else None,
                  f"{secs} second(s)" if secs else None]
    
    return ', '.join([x for x in time_units if x])

#Convert/format date/time for API output
def dt_conversion(date_time_str):
    return datetime.datetime.fromisoformat(date_time_str).strftime("%B %d, %Y %I:%M:%S %p")

#Get location from coordinates for API Output
def get_location(lat, lon):
    mapi_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(mapi_url)
    if response.status_code == 200:
        location_data = response.json()
        city=location_data["address"]["city"] 
        state=location_data["address"]["state"] 
        country=location_data["address"]["country"]
        location = f"{city}, {state}, {country}"
        return location
        
    else:
        return None


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
                map = resp_dict["data"]["attributes"]["details"]["map"]
                password = resp_dict["data"]["attributes"]["details"]["password"]
                gamemode = resp_dict["data"]["attributes"]["details"]["gameMode"]
                game = resp_dict["data"]["relationships"]["game"]["data"]["id"]
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

                    embed.add_field(name = "**Server Name -**", value = name, inline=True)
                    embed.add_field(name = "**Connect -**", value = f'{ip}:{port}', inline = True)
                    embed.add_field(name = "**Gamemode -**", value = gamemode, inline=True)
                    embed.add_field(name = "**Map -**", value = map, inline=False)
                    embed.add_field(name = "**Player Count -**", value = f'{PlayerCount}/{MaxPlayers}', inline=True)
                    embed.add_field(name = "**Password? -**", value = password, inline=True)
                    embed.add_field(name = "**Game -**", value = game, inline=True)

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

                    lon, lat = coord

                    embed.add_field(name = "**City, State, Country -**", value = f'{get_location(lat, lon)}', inline = False)
                    
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
                name = resp_dict["data"]["attributes"]["name"]  
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

                    embed.add_field(name = "**Server Rank -**", value = f'{name} is ranked {rank} on BattleMetrics', inline = False)
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
            async with session.get(url) as rep:
                if resp.status == 200:
                #Get data from API response
                    resp_dict = json.loads(await resp.text())
                    rep_dict = json.loads(await rep.text())
                    onlinesince = resp_dict["meta"]["onlineSince"]
                    lastplayerjoin = resp_dict["meta"]["lastPlayerJoin"]
                    status = rep_dict["data"]["attributes"]["status"] 
 
                #If server is online, send Embed
                if status == "online":
                    embed = disnake.Embed(
                        title = f"{serverName}'s Uptiime:",
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

                    embed.add_field(name = "**Online Since -**", value = f'{serverName} has been online since {dt_conversion(onlinesince)}', inline = False)
                    embed.add_field(name = "**Last Player Join -**", value = f'The last player joined {serverName} at {dt_conversion(lastplayerjoin)}', inline = False)       
                    await inter.send(embed=embed)

                else:
                    #Send error if occurs
                    print(f"Battlemetrics Error with status code: {resp.status}")
                    await inter.send('BM ERROR')

#Last Outage command
@bot.slash_command(
    name = "lastcrash",
    description = f"Shows {serverName}'s last outage")
async def status(inter):
    async with aiohttp.ClientSession() as session:
        async with session.get(uptime_url) as resp:
            async with session.get(url) as rep:
                if resp.status == 200:
                #Get data from API response
                    resp_dict = json.loads(await resp.text())
                    rep_dict = json.loads(await rep.text())
                    lastcrashstart = resp_dict["data"][0]["attributes"]["start"]
                    lastcrashend = resp_dict["data"][0]["attributes"]["stop"]
                    status = rep_dict["data"]["attributes"]["status"] 
 
                    embed = disnake.Embed(
                        title = f"{serverName}'s Last Crash:",
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

                    embed.add_field(name = "**Last Crash Start -**", value = f'{serverName} last crashed/restarted: {dt_conversion(lastcrashstart)}', inline = False)
                    embed.add_field(name = "**Last Crash End -**", value = f'{serverName} came back online: {dt_conversion(lastcrashend)}', inline = False)       
                    await inter.send(embed=embed)

                else:
                    #Send error if occurs
                    print(f"Battlemetrics Error with status code: {resp.status}")
                    await inter.send('BM ERROR')                    

#playtime command
@bot.slash_command(
    name = "playtime",
    description = f"Shows {serverName}'s last outage")
async def status(inter, bm_player_id: int):
    async with aiohttp.ClientSession() as session:
        playtime_url = "https://api.battlemetrics.com/players/" + str(bm_player_id) + "/servers/" + str(BM_ServerID)
        player_url = "https://api.battlemetrics.com/players/" + str(bm_player_id)
        async with session.get(playtime_url) as resp:
            async with session.get(player_url) as player:
                async with session.get(url) as rep:
                    if resp.status == 200:
                #Get data from API response
                        resp_dict = json.loads(await resp.text())
                        player_dict = json.loads(await player.text())
                        firstjoin = resp_dict["data"]["attributes"]["firstSeen"]
                        lastjoin = resp_dict["data"]["attributes"]["lastSeen"]
                        timeplayed = resp_dict["data"]["attributes"]["timePlayed"]
                        online = resp_dict["data"]["attributes"]["online"] 
                        playername = player_dict["data"]["attributes"]["name"]
 
                        embed = disnake.Embed(
                            title = f"{playername}'s Play Stats on {serverName}:",
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

                        if online == "true":
                            embed.add_field(name = "**Online Status -**", value = 'Online', inline = False)      
                        else:
                            embed.add_field(name = "**Online Status -**", value = 'Offline', inline = False) 
                        
                        embed.add_field(name = "**First Joined -**", value = f'{dt_conversion(firstjoin)}', inline = False)
                        embed.add_field(name = "**Last Joined -**", value = f'{dt_conversion(lastjoin)}', inline = False)  
                        embed.add_field(name = "**Time Played -**", value = f'{time_conversion(timeplayed)}', inline = False) 
                        await inter.send(embed=embed)
                    else:
                        #Send error if occurs
                        print(f"Battlemetrics Error with status code: {resp.status}")
                        await inter.send('BM ERROR')

bot.run(token)
