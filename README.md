# a Vanderbilt Gaming Association bot

possibly? needs more features to be complete

## Developer Setup

the bot requires Python 3.8+.

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
python3 bot.py
```
or 
```commandline
python bot.py
```

## Architecture

```
├── bot.py
├── cogs
│   ├── rocketleague.py
├── fetchers.by
```