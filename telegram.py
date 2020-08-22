
def share_telegram(message):
    print('inside')
    import telepot
    from secrets import telegram_chat_token
    token = telegram_chat_token
    botname = 'StockTips111_bot'

    TelegramBot = telepot.Bot(token)
    #bot_id = TelegramBot.getMe()['id']
    #print(bot_id)
    bot_id='1368976537'
    updates = TelegramBot.getUpdates()
    send_id='-333641597'
    #send_id = updates[1]['message']['chat']['id']

    #print(TelegramBot.getChat('StockTips'))
    TelegramBot.sendMessage(send_id, message)
