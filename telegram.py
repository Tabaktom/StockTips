
def share_telegram(message):
    import telepot
    from secrets import telegram_chat_token
    token = telegram_chat_token
    botname = 'BOT_NAME'

    TelegramBot = telepot.Bot(token)
    #bot_id = TelegramBot.getMe()['id']
    #print(bot_id)
    bot_id='BOT_ID'
    updates = TelegramBot.getUpdates()
    send_id='CHAT_ID'
    #send_id = updates[1]['message']['chat']['id']

    #print(TelegramBot.getChat('StockTips'))
    TelegramBot.sendMessage(send_id, message)
