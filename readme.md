# MemeBot
[![BCH compliance](https://bettercodehub.com/edge/badge/OhmNoobs/MemeBot?branch=master)](https://bettercodehub.com/)

https://hub.docker.com/r/dockerwoop/memebot/

## Setup
Regardless if run in a container or not.

### Required Environment Variable
| Variable | Expected Value |
|---|---|
| `BOT_TOKEN` | your telegram bot token as generated by the [@bot_father](https://t.me/BotFather) |

## Running the tests
In the projects root directory, call:  
`python -m unittest discover --pattern "Test*.py" --start "bot"`

## Developing
Database description: https://editor.ponyorm.com/user/woop/memebot