import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import aiohttp
from aiohttp import web

API_ID = 32065095
API_HASH = 'c23ce03ff001e29dc44a36976699b862'
WEBHOOK_URL = 'https://hook.eu1.make.com/r9b84om9ih1vlavqriglefifrayha47f'
SESSION_STRING = '1ApWapzMBu2AgVzbsy43IaEpdwXq8vPFrI8kHyCyVUHyOX08plS_n6PmqhomM-bN18wNDy1A6Req19-uTHxw-iuEmUUUeBGGeDVb99f3T8vi6Zo38jJ2pSF7PXV3HyLQihfGzW87a7mCe8pKBXBjG85dEPaosNv1UaUBsjYzS41O_MqG5pgAWPFkSYNlFPdUqykFkYUH8ZItAYOiMEqnZZM8ijaUv_mcqu-l1pKVCjA88S9ycd0PYhqDRkhwMAuco79Fb_l7NNGbDvzgdjaywZe6M4tmkXmSfEkoww2f-Dt9F3Ba7wBE9EC36F4EZ0ojdRLpVJB9KXnhn0nq3IdHpU6h01NPX8FY='

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

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

# Простой веб-сервер, чтобы Render был доволен открытым портом
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await start_web_server()
    print("Юзербот успешно запущен!")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
