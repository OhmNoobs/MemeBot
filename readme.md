# MemeBot
[![BCH compliance](https://bettercodehub.com/edge/badge/OhmNoobs/MemeBot?branch=master)](https://bettercodehub.com/)
![Tests](https://github.com/OhmNoobs/MemeBot/workflows/Tests/badge.svg)

https://hub.docker.com/r/dockerwoop/memebot/

## Setup
Regardless if run in a container or not.

### Environment Variables
| Variable | Expected Value |
|---|---|
| `BOT_TOKEN` | your telegram bot token as generated by the [@bot_father](https://t.me/BotFather) |
| `ADMINS` | comma separated list of admins telegram ids |

### Bot Settings
Talk to the [@bot_father](https://t.me/BotFather) and enable the following features for your bot:
- `/setinlinefeedback`: `Enabled`
- `/setjoingroups`: `Enable`
- `/setinline`: Any phrase send while looking for inline results

## Developing
Database description: https://editor.ponyorm.com/user/woop/memebot

### Running The Tests
In the projects root directory, call:  
`python -m unittest discover --pattern "Test*.py" --start "bot"`