from bot import InternetSpeedTwitterBot

PROMISED_UP = 10
PROMISED_DOWN = 160

bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
if bot.up < PROMISED_UP or bot.down < PROMISED_DOWN:
    bot.tweet_at_provider()



