import telegram

BOT_TOKEN = ''


async def sound_alarm(property_dict, chat_id):
    message_text = property_dict['price'] + '\n' + property_dict['address'] + '\n' + property_dict['type'] + '\n' \
                   + property_dict['link']
    bot = telegram.Bot(token=BOT_TOKEN)
    async with bot:
        await bot.sendMessage(chat_id=chat_id, text=message_text)
