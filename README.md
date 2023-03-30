# Game-Server-Discord-Bot (Made in Disnake Py)
Discord bot that pulls various info from your server and displays it through slash commands using BattleMetrics API. Also sets the status of the bot as playercount/maxplayers

`/uptime`, `/playtime`, and `/lastcrash` do NOT work for MC servers right now, this is currently being worked on

### **Planned Updates -**
- Remove `serverName` from `config.json` and make it auto grab the bot's name
- add `/link` command for steam account integration with the bot (for auto-grabbing player stats from a BM server)

### **License -**
Covered under Unlicense (https://unlicense.org)

### **Requirements -** 
- Python 3.11+
- A discord bot application
- A game server that is on BattleMetrics (https://www.battlemetrics.com/)

### **Dependencies -**
- Run ```pip install requirements.txt``` from the CMD Prompt/Terminal in the project root

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

![image](https://user-images.githubusercontent.com/107073565/217389758-76ab54e9-5b6f-4c98-8a33-6c2d334c2b4f.png)


```/lastcrash``` - Shows the last outage the server had

![image](https://user-images.githubusercontent.com/107073565/217389818-90eb29d3-447a-40c2-9256-7c2f4e8d18e8.png)


```/locate``` - Shows the servers location

![image](https://user-images.githubusercontent.com/107073565/217389864-df745407-1ba5-40b0-be48-9a738fef7a90.png)

```/playtime``` - Shows a players play-time on the server using their BattleMetrics playerID

![image](https://user-images.githubusercontent.com/107073565/217390068-324dfd49-ce63-44c8-a9e7-71f05be90c0e.png)


```/rank``` - Shows the servers rank on BattleMetrics

![image](https://user-images.githubusercontent.com/107073565/217390134-502277d3-79bd-44eb-9abd-4d1c27e7a734.png)


```/status``` - Shows the server status and various info about the server (changes info shown based on game server type)

![image](https://user-images.githubusercontent.com/107073565/217390198-43813733-f662-49da-a01f-e9022d7c3f57.png)


```/uptime``` - Shows the servers uptime and when the last player joined

![image](https://user-images.githubusercontent.com/107073565/217390290-b69f21a2-834a-488c-b61e-19594344e060.png)








