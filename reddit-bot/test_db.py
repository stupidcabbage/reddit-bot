import asyncio
from db import execute, fetch_one, close_db, _async_close_db, fetch_all
from services.subreddits import get_all_subreddits

async def test_function_with_db(sql):
    try:
        result = await fetch_all(sql)
        print(result)
    finally:
        await _async_close_db()

async def test_execute(sql):
    try: 
        await execute(sql)
    finally:
        await _async_close_db()

# asyncio.run(test_execute("INSERT INTO flairs VALUES(2, 'hello world');"))

result = asyncio.run(get_all_subreddits())
print(result)
