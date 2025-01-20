import asyncio
import time
import aiohttp

API_LINK = "https://frontend-api-v2.pump.fun/coins/for-you?offset=0&limit=50&includeNsfw=false"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"

headers = {
    "User-Agent": UA,
}

async def get_featured_token() -> list[dict]:
    start_time = time.monotonic()  # Начало отсчета времени
    async with aiohttp.ClientSession(headers=headers) as s:
        async with s.get(API_LINK) as response:
            print(await response.text())
            resp = await response.json()
    elapsed_time = time.monotonic() - start_time  # Вычисляем затраченное время
    print(f"Время выполнения запроса: {elapsed_time:.2f} секунд")
    return resp
        
        

if __name__ == "__main__":
    asyncio.run(get_featured_token())
