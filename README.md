# a Vanderbilt Gaming Association bot

currently has Rocket League capabilities only

## Developer Setup

This bot is hosted on Heroku and uses MongoDB to track user info.

### Installation

Clone the repo by 
`git clone https://github.com/casciand/vga-bot.git` or use ssh.

`cd` into the repo and do `pip install -r requirements.txt` (or pip3) to install dependencies.

### Secrets

Create a file named `.env` in the repo and add your discord token to it: `DISCORD=your_token_here`.
This is what links the application to your bot profile.

### Run

Run the bot using 

```commandline
python bot.py
```
or 
```commandline
python3 bot.py
```

## Architecture

```
├── bot.py
├── cogs
│   ├── rocketleague.py
├── fetchers.py
├── database.py
```