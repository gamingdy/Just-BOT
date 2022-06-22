# Just-BOT

[invite img]:img/invite_option.png

Good evening, welcome on the README of Just-BOT

Just-BOT is a Discord bot allowing to realize only one thing ( for the moment ), which is the possibility to put in slowmode one or several users/roles.   


## Summary

- [Configuration](https://github.com/gamingdy/Just-BOT#configuration)
- [Installation](https://github.com/gamingdy/Just-BOT#installation)
- [Bugs and Feature](https://github.com/gamingdy/Just-BOT#bugsfeatures)

## Configuration

Before launching the bot for the first time, you must edit the file [config.json](https://github.com/gamingdy/Just-BOT/blob/main/config.json)

- `TOKEN`  --> The bot token available on [the developer portal](https://discord.com/developers/applications), and if you don't know how to find the token of your bot, [here is a tuto that explains it](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token)

- `database` --> The path to a file to store your database, **if the file does not exist, it is automatically created by python**, by default it's `data/bot.db`

- `debug` --> If you want to launch your bot by activating the `debug_guild` here is an example,otherwise you can leave the default config:
    ```json
    {
        "debug": [True, [List of guild ids]]
    }
    ```

**🚨 Warning 🚨** : Before launching the bot, you must reinvite it by activating the `applications.commands`, like that.
![invite img]

## Installation

 - you can install the necessary packages by doing :

**Linux/Mac** 
```
$ python3 -m venv /path/to/new/virtual/environment

$ source /path/to/new/virtual/environment/bin/activate

$ pip -r requirements.txt
```

**Windows**
```
	
C:\> python3 -m venv \path\to\new\virtual\environment
	
C:\> \path\to\new\virtual\environment\Scripts\activate.bat
	
C:\> pip -r requirements.txt
```

**If `pip -r requirements.txt` don't work , you can try**:
```
$ python -m pip -r requirements.txt
```

## Bugs/Features

If you encounter a bug, you can create an issue, with details of the bug encountered.

For more features, you can create a pull request, with details about your features