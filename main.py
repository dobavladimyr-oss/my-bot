import os
import asyncio
from aiohttp import web
from pyrogram import Client, filters
import aiohttp

# 1. Данные из переменных окружения
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

# 2. Инициализация юзербота
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# 3. Фильтр: ловим ВСЕ сообщения из каналов и групп
@app.on_message(filters.channel | filters.group)
async def handle_channel_post(client, message):
    text = message.text or message.caption
    
    if not text:
        return

    payload = {
        "text": text,
        "chat_id": message.chat.id,
        "message_id": message.id
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=payload) as resp:
                print(f"[LOG] Передано на вебхук! Статус: {resp.status}")
    except Exception as e:
        print(f"[ERROR] Ошибка отправки на Webhook: {e}")


# 4. Веб-сервер для Render
async def handle_ping(request):
    return web.Response(text="Your service is live 🚀")

async def start_web_server():
    server = web.Application()
    server.router.add_get("/", handle_ping)
    runner = web.AppRunner(server)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"[LOG] Web server running on port {port}")

async def main():
    await start_web_server()
    await app.start()
    print("[LOG] Юзербот успешно запущен и отслеживает каналы!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Правильный запуск asyncio для новых версий Python
    asyncio.run(main())
