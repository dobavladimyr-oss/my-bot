import os
import json
import urllib.request
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Отслеживаем и каналы (channel), и группы/супергруппы (group)
@app.on_message(filters.channel | filters.group)
async def handle_new_message(client, message):
    # Забираем текст из обычного сообщения ИЛИ подпись из медиа (картинки)
    text_content = message.text or message.caption
    
    # Если в сообщении нет вообще никакого текста, пропускаем
    if not text_content:
        return

    payload = {
        "text": text_content,
        "chat_id": message.chat.id,
        "message_id": message.id
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"[LOG] Перехвачено! Чат: {message.chat.id}, Статус Make: {response.getcode()}")
    except Exception as e:
        print(f"[ERROR] Ошибка отправки в Make: {e}")

if __name__ == "__main__":
    print("Юзербот запускается...")
    app.run()
