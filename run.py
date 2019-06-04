from modules import bot, botName, HOST
from modules import app
import os


def setIt():
    url = "{}/".format(HOST)
    s = bot.setWebhook(url)
    #print ()
    if s:
        print("Webhook set done")
        return ("{} WebHook Setup OK!".format(botName))
    else:
        print("Webhook set Nooo")
        return ("{} WebHook Setup Failed!".format(botName))


if __name__=='__main__': 
    setIt()   
    app.run()