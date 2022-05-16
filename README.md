# Gag-Bot
## What you do with my code is on you, I am not responsible for any use or misuse of my code.
A Discord Bot, that gags.

Made it as a gag.
# Modules/Dependencies
[Discord py](https://github.com/Rapptz/discord.py)

[python-dotenv](https://pypi.org/project/python-dotenv/)

[python 3](https://www.python.org/downloads/)

[Discord Bot Token](https://discord.com/developers/docs/getting-started#configuring-a-bot)
## Ez-Install & Usage
Place PublicGagBotClient-X.X.X.py somewhere, preferable in its own folder.

Place BotManager-X.X.X.py in the same folder as PublicGagBotClient-X.X.X.py.

Ensure you have all the modules/dependencies installed.

Run BotManager-X.X.X.py

>BotManager will:
>1. look to see if you have a .env file and if not it will create one and ask you to input your discord bot token
>2. will check to see if there is a PID file and if the PID inside is running if it is it will ask you if you would like to kill the PID
>3. if you kill the PID then it will search for the newest (based on X.X.X) bot script and will ask you if you would like to run it
>4. you can say No, ICT, or IB in response to being asked to run the script
>5. No : Doesn't run script
>6. ICT : Runs the script in your current terminal
>7. IB : Runs the script in the background

## Installation
Place PublicGagBotClient-X.X.X.py somewhere, preferably in its own folder.

Make a file called .env in the folder with PublicGagBotClient-X.X.X.py.

Fill .env file (XXXXX is bot token): 
```
# .env
DISCORD_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
## Usage
The minimum commands needed is:

While being in a terminal in the location of where the file is
```
python3 <FileName>
```
While being in a terminal
```
python3 <FilePath>
```

I normally run mine with commands
```
nohup python3 <FileName> &
```
nohup : Outputs anything that gets sent to the console to a file called "nohop.out"

python3 : Designated which version of python to use

& : Sets script to run in background (YOU WILL NEED TO KILL THE PROCESS TO STOP THE SCRIPT)

### Note
A file named .pid will be made and the PID of the script should be in there so you can use that PID to kill the script.

The log file made by the bot will be made in whatever folder you are in when you run the script.

# Bot Commands
Help: Lists Commands and usage
```
>Help
```
