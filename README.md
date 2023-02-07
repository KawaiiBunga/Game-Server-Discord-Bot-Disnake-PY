# Game-Server-Discord-Bot (Made in Disnake Py)
Discord bot that pulls various info from your server and displays it through slash commands using BattleMetrics API. Also sets the status of the bot as playercount/maxplayers

This bot has been optimized for SRCDS servers. Some aspects of it work with MC servers, but some things are broke :( This is being worked on

### **License -**
Covered under Unlicense (https://unlicense.org)

### **Requirements -** 
- Python 3.11+
- A discord bot application
- A game server that is on BattleMetrics (https://www.battlemetrics.com/)

### **Dependencies -**
- ```pip install Disnake```
- ```pip install AIOHTTP```
- ```pip install Json```
- ```pip install datetime```

### **Config Walkthrough -**
1. Configure the config.json file to have your game server/bot parameters

![image](https://user-images.githubusercontent.com/107073565/216780462-b323101c-51d2-4922-9b07-d535e7a4f921.png)

```"serverName": "KarmaDev"``` - Set as the name you want to show up in sent slash commands, your servers name

```"website": "https://krma.site"``` - Set as your website

```"iconURL": "xxxxxxxxxxxx.png"``` - Set as the logo you want for slash command author

```"token": "xxxxxx"``` - Discord Bot Token (https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token)

```"clientID": "xxxxxx"``` - Discord Bot's Client ID

```"Game": "gmod"``` - Set this as this part of your server's BattleMetrics URL
![image](https://user-images.githubusercontent.com/107073565/216780645-26b57906-073c-402e-b2e0-cb7045a4f193.png)

```"BM_ServerID": "xxxxxxxx"``` - Set this as your servers BattleMetrics ID
![image](https://user-images.githubusercontent.com/107073565/216780694-0e730e79-0e20-4e24-8cd2-11e6eaa573cf.png)

```"statusText": "on KarmaMC - "``` - Set this as what you want before your playercount/maxplayer in the Bot's status
![image](https://user-images.githubusercontent.com/107073565/216780801-fef91ba5-7cd5-449c-93c1-e102c10ecee7.png)


### **Running the Bot -**

1. Install the dependencies by opening a terminal/cmd prompt in the folder your bot is located in and run the individual commands listed in dependancies above

2. Run the bot in a terminal/command prompt with Python (or PM2 with nodejs installed for linux)
- In a terminal or Command Prompt, run 
```python bot.py``` (for PM2, use ```pm2 start "py bot.py" --name "Whatever you wanna name this"```)
- If everything is configured correctly, your bots output should look like this:
![image](https://user-images.githubusercontent.com/107073565/216780817-6aa48e55-d96b-4e39-8e26-4b025e8af1e5.png)


### **Inviting the bot to your server -**

1. Go to your bots dev app page and click "OAuth2" on the left side

2. Under "OAuth2", click "URL Generator"

3. Select scopes as shown in the below image

4. Select bot permissions as shown in the below image

5. Copy the link under the "Bot Permissions" box, paste it in your browser, login with Discord, and invite the bot to your server!
![gitreadme](https://user-images.githubusercontent.com/107073565/213134525-ff29f242-25c8-4e29-ac7c-f348674a7053.png)



### **Slash commands -**

Section being added soon
