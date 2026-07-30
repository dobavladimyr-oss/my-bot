import os
import asyncio
from aiohttp import web
from pyrogram import Client, filters
import aiohttp

# 1. Данные из окружения
API_ID = int(os.environ.get("API_ID", "0").strip())
API_HASH = os.environ.get("API_HASH", "").strip().strip("'\"")
SESSION_STRING = os.environ.get("SESSION_STRING", "").strip().strip("'\"")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "").strip().strip("'\"")

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

# 2. Фильтр: безопасно ловим любые посты
@app.on_message(filters.channel | filters.group)
async def handle_channel_post(client, message):
    try:
        # Извлекаем текст или подпись к медиафайлу
        text = message.text or message.caption or ""
        
        if not text.strip():
            return

        payload = {
            "text": text,
            "chat_id": message.chat.id,
            "message_id": message.id
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=payload, timeout=10) as resp:
                print(f"[LOG] Успешно отправлено на Make! Статус: {resp.status}")

    except Exception as e:
        # Логируем ошибку, но НЕ даем приложению упасть!
        print(f"[ERROR] Ошибка при обработке сообщения: {e}")


# 3. Веб-сервер для поддержки Render
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
    print("[LOG] Юзербот запущен и отслеживает каналы!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
