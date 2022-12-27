# Speedrunning leaderboard Discord bot

---

## Warning: This project is a W.I.P. Please report any issues on the Issues tab.

### License

**Speedrunning-leaderboard-Discord-Bot-Python © 2022 by Iwakura Megumi is licensed under CC BY-NC 4.0. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/**
### Setup

```bash
$ git clone https://github.com/gvmii/Speedrunning-leaderboard-Discord-Bot-Python.git
$ cd Speedrunning-leaderboard-Discord-Bot-Python
$ ./venv/Scripts/activate
```
Create a .env file and add the following:
`TOKEN='YOUR_TOKEN_HERE'` replacing `YOUR_TOKEN_HERE` with your Discord Bot Token

After that, run the following:

```bash 
$ python ./bot.py
```

### TODO/WIP
Please first contribute to the project by fixing things tagged in the code with "TODO:" or with "FIXME:"

- Make speedrun categories scalable
- Move to another data file method (Database, or .csv)
- Add a medals system, where you can give them to members for certain achievements
- Get data from speedrun.com
- Separate commands/utilities by cogs
- Write unittests
### Style guidelines

- All code should be formatted with [Black](https://black.readthedocs.io/en/stable/index.html)
- Line length should be **79**.
- Follow PEP8 whenever possible.
- Indentation should be **4 spaces**.

Everyone's free to contribute to this project, but I'd appreciate if an issue or a pull request got opened before I commited again (To prevent merge issues)

### Credits

- Discord library used: [Nextcord](https://github.com/nextcord/nextcord)

[Join my Discord Server, the Gumistation!](https://discord.gg/XKfKm2F)
