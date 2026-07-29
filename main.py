import asyncio
from telethon import TelegramClient, events
import aiohttp

API_ID = 32065095
API_HASH = 'c23ce03ff001e29dc44a36976699b862'
WEBHOOK_URL = 'https://hook.eu1.make.com/r9b84om9ih1vlavqriglefifrayha47f'

client = TelegramClient('dubai_parser_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    if event.is_channel or event.is_group:
        text = event.message.message
        if text:
            payload = {
                'text': text,
                'chat_id': event.chat_id,
                'message_id': event.id
            }
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(WEBHOOK_URL, json=payload) as resp:
                        print(f"Пост отправлен в Make! Статус: {resp.status}")
                except Exception as e:
                    print(f"Ошибка: {e}")

print("Юзербот запущен!")
client.start()
client.run_until_disconnected()
