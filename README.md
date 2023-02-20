# Just-BOT

[![contributors]][contributors-url]
[![issues]][issues-url]
![stars]
[![forks]][forks-url]
[![license]][license-url]

Good evening, welcome on the main page of Just-BOT


Just-BOT is a Discord bot with a lot of feature


## Summary

- [Configuration](#configuration)
- [Installation](#installation)
- [Run](#run)
- [Bugs and Feature](#bugsfeatures)
- [TODO LIST](#todo-list)


## Configuration

Before launching the bot for the first time, you must edit the file [config.json]

- **TOKEN**  --> The bot token available on [the developer portal][dev portal], and if you don't know how to find the token of your bot, [here is a tuto that explains it][find token]

- **database** --> The path to a file to store your SQLITE database, **if the file does not exist, it is automatically created by python**, by default it's `data/bot.db`

- **debug** --> If you want to launch your bot by activating the `debug_guild` here is an example,otherwise you can leave the default config:
    ```json
    {
        "debug": [true, ["List of guild ids"]]
    }
    ```

**🚨 Warning 🚨** : Before launching the bot, you must reinvite it by activating the `applications.commands`, like that.
![invite img]


## Installation

 - You can install the necessary packages by following these steps :

**Linux/Mac** 
```bash
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
C:\> python -m pip -r requirements.txt
```
**Note** : You can get more information about venv by following this [link][venv info]


## RUN

- You can launch the program by running the file `main.py`

**Linux/Mac** 
```bash
$ source /path/to/new/virtual/environment/bin/activate
$ python main.py
```

**Windows**
```
    
C:\> \path\to\new\virtual\environment\Scripts\activate.bat
    
C:\> python main.py
```


## Bugs/Features

If you encounter a bug, you can create an issue, with details of the bug encountered.

For more features, you can create an issue, with details about your features


## TODO LIST:

* ### Presentation:
    - discord : create discord server for bot and me
    - hosted version : Provide a hosted version of the bot

* ### Command:
    - todo : Allows the owner to create a callback for features or bug fixes
    - serverstats : Get information about the server
    - funfact : give obvious or unbelievable information

* ### Update:
    - bot_info : add bot uptime
    - ui: Show information about user in image
    - list channel : Allows you to obtain the list of slowmodes for a specific channel
    - automatic update of the user name#discriminator in the DB if the user name changes
    - automatic addition of a user in slowmode, if the slowmode of the role is activated


<!-- Markdown link -->
[invite img]:doc/img/invite_option.png
[config.json]:https://github.com/gamingdy/Just-BOT/blob/main/config.json
[dev portal]:https://discord.com/developers/applications
[find token]:https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token
[venv info]:https://docs.python.org/3/library/venv.html

[contributors]: https://img.shields.io/github/contributors/gamingdy/Just-BOT?color=E91E63&style=for-the-badge
[contributors-url]:https://github.com/gamingdy/Just-BOT/graphs/contributors

[stars]: https://img.shields.io/github/stars/gamingdy/Just-BOT?color=E91E63&style=for-the-badge

[issues]:https://img.shields.io/github/issues/gamingdy/Just-BOT?color=E91E63&style=for-the-badge
[issues-url]:https://github.com/gamingdy/Just-BOT/issues

[forks]:https://img.shields.io/github/forks/gamingdy/Just-BOT?color=E91E63&style=for-the-badge
[forks-url]:https://github.com/gamingdy/Just-BOT/network/members

[license]:https://img.shields.io/github/license/gamingdy/Just-BOT?color=E91E63&style=for-the-badge
[license-url]:LICENCE

