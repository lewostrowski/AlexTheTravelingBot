# AlexTheTravelingBot

This app was created for learning purposes and was never used (and should not be used) for data scrapping. Using it may breach the law and rules of scrapped sites.


## Prerequisites


This bot was prepared to work on a server-like computer with Arch Linux and LXQT interface (graphical mode for puppet browser is needed to avoid bot detection).


The bot is working on a rigged Google Chrome driver created by [ultrafunkamsterdam](https://github.com/ultrafunkamsterdam/undetected-chromedriver) called Undetected Chromedriver.


Due to Arch Linux's nature, the original Google Chrome must be installed via the AUR repository, not Flatpack.


## Initializing bot


Clone repository, then type in the main folder:


`$ python start.py --install`


You will be asked to provide a full token from Telegram's BotFather. The script will automatically retrieve the ID and auth token. After that, the first run will be initialized. Each next run will be randomly scheduled in 2-3 hours.


## How it works?


With each run, the bot will turn on the screen, open Undetected Chromedriver with a graphical interface, and enter saved links. Scrapping results will be kept in a database. 


After the second run, the bot will check for bargains and send a message via Telegram if he founds one. The message will be sent once in 24h for if a deal is found.


Users can communicate with the bot via Telegram using the following commands:


`links` will list all saved links with index number

`delete [link's index]` delete links by index number

`status` lists the current price and other information for all saved routes


A user must send only a link to the bot to save a link. Works with `esky.pl` links.
