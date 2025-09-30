# Импортируем библиотека
import asyncio
from websockets.asyncio.server import serve
from websockets.asyncio.client import connect

# Адрес оригинального вебссокета маха
ONEME_WS_URL = "wss://ws-api.oneme.ru/websocket"

# Юзер-агент для большей надежности
HEADER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"

async def repeater(websocket):
    # Устанавливаем в фоне подключение с оригинальным вебсокетом
    oneme_ws = await connect(
        uri=ONEME_WS_URL,
        origin="https://web.max.ru",
        user_agent_header=HEADER_USER_AGENT
    )
    
    async def forward_to_oneme():
        """Функция перенаправки пакетов в оригинальный вебсокет макса"""
        async for message in websocket:
            print(">>> {}".format(message))
            await oneme_ws.send(message)

    async def forward_to_client():
        """Функция перенаправки пакетов клиенту"""
        async for message in oneme_ws:
            print("<<< {}".format(message))
            await websocket.send(message)

    await asyncio.gather(forward_to_oneme(), forward_to_client())

async def main():
    """Функция запуска сервера"""
    async with serve(repeater, "localhost", 8080) as server:
        await server.serve_forever()

asyncio.run(main())