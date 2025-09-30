# Импортируем библиотека
import asyncio
from websockets.asyncio.server import serve
from websockets.asyncio.client import connect

# Адрес оригинального вебссокета маха
ONEME_WS_URL = "wss://ws-api.oneme.ru/websocket"

async def repeater(websocket):
    # Устанавливаем в фоне подключение с оригинальным вебсокетом
    oneme_ws = await connect(ONEME_WS_URL, origin="https://web.max.ru")
    
    async def forward_to_oneme():
        """Функция перенаправки пакетов в оригинальный вебсокет макса"""
        async for message in websocket:
            await oneme_ws.send(message)

    async def forward_to_client():
        """Функция перенаправки пакетов клиенту"""
        async for message in oneme_ws:
            await websocket.send(message)

    await asyncio.gather(forward_to_oneme(), forward_to_client())

async def main():
    """Функция запуска сервера"""
    async with serve(repeater, "localhost", 8080) as server:
        await server.serve_forever()

asyncio.run(main())