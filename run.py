from modules import bot, botName, HOST
from modules import app as application


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
    application.run(host='0.0.0.0', debug=True, port=8080)