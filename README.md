Application checks popular NL websites with rental offers and sends notifications to Telegram.
To run the app:
1. Download [geckodriver](https://github.com/mozilla/geckodriver/releases) and put it into the root directory. This is a Firefox webdriver;
2. Create `.env` file in the root directory with the following environment variables:
```
TG_BOT_TOKEN=<...>
TG_CHAT_ID=<...>
TG_TEST_CHAT_ID=<...>
REBO_LOGIN=<...>
REBO_PWD=<...>
```
where three former variables refer to the corresponding Telegram values,
and two latter ones refer to login and password for the corporation https://rebowonenhuur.nl.
_The thing is that now it's impossible to check the available options not being logged in._

3. Build the docker image and run the containers following the instructions from `docker_cmds.txt`.
Mind that I'm creating two containers that process different corporations.
_I empirically found out that some corps are updated extremelly rarely, so that I put them into the separate container and scheduled scrapping once per 5 minutes._

Have fun!
