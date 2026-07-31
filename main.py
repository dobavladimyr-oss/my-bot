import os
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# --- 1. Фейк-сервер для Render ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

Thread(target=run_dummy_server, daemon=True).start()
# ----------------------------------

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.channel | filters.group)
async def handle_new_message(client, message):
    try:
        # Забираем текст сообщения или подпись к медиа
        text_content = message.text or message.caption
        
        if not text_content:
            return

        # Фильтруем системные сообщения
        if text_content.strip().startswith("SKIP") or "Tribute" in text_content:
            print("[LOG] Пропущено системное сообщение со SKIP")
            return

        payload = {
            "text": text_content,
            "chat_id": message.chat.id,
            "message_id": message.id
        }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"[LOG] Успешно перехвачено! Чат: {message.chat.id}, Статус Make: {response.getcode()}")
            
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке сообщения: {e}")

# Функция прогрева диалогов при запуске
async def main():
    async with app:
        print("Прогреваем базу чатов и диалогов...")
        async for dialog in app.get_dialogs():
            pass  # Загружаем все чаты в кэш Pyrogram
        print("Юзербот успешно запущен и готов к работе!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
