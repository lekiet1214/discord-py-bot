[![Pylint](https://github.com/lekiet1214/discord-py-bot/actions/workflows/pylint.yml/badge.svg)](https://github.com/lekiet1214/discord-py-bot/actions/workflows/pylint.yml)
# discord-py-bot
## Dependecies
- [py-cord](https://pycord.dev/)
- [dotenv](https://pypi.org/project/python-dotenv/)
## How to run
1. Clone the repository using `git clone https://github.com/lekiet1214/discord-py-bot.git`
2. Go to the directory using `cd discord-py-bot`
3. Install the dependencies using `pip install -r requirements.txt`
4. Create a `.env` file and add the following:
```env
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
OWNER_ID=YOUR_DISCORD_USER_ID
```
For information on how to get the `DISCORD_TOKEN`, refer to the [py-cord documentation](https://guide.pycord.dev/getting-started/creating-your-first-bot)
5. Run the bot using `python bot.py`
## Features
The one and only feature of this bot is to record voice data of a voice channel then save it as a `.mp3` file.
## Commands
This bot use slashh commands, to see the list of commands, type `/` in the chat and select the bot.
## License
This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.