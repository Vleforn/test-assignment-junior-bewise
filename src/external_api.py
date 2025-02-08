import aiohttp
import os
from config import settings

async def create_aiohttp_session() -> None:
    global aiohttp_session
    aiohttp_session = aiohttp.ClientSession()

async def get_token() -> str:
    token = os.getenv("TOKEN")
    if token is None:
        async with aiohttp_session.get(settings.token_url, params={"command": "request"}) as response:
            r = await response.json()
            token = r["token"]
            os.environ["TOKEN"] = token
    return token
 

async def request_questions(num: int) -> dict[str, str | list[str]]:
    params = {"amount": num, "token": await get_token()}
    async with aiohttp_session.get(settings.api_url, params=params) as response:
        r = await response.json()
        questions = r["results"]
    return questions
