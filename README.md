Application checks popular NL websites with rental offers and sends notifications to Telegram.
To run the app:
1. Download `geckodriver` and put it into the root directory. This is a Firefox webdriver;
2. Create `.env` file in the root directory with the following environment variables:
```
TG_BOT_TOKEN=<value>
TG_CHAT_ID=<value>
TG_TEST_CHAT_ID=<value>
```
where all the variables refer to the corresponding Telegram values.
3. Change the cron schedule in `dockerfile` if necessary.
4. Build an image and run the container using `docker`.
