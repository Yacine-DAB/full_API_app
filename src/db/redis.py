import redis.asyncio as aioredis

from src.config import Config

JTI_EXPIRE = 3600

token_blocklist = aioredis.from_url(Config.REDIS_URL)

async def add_jti_to_clacklist(jti: str) -> None:
     await token_blocklist.set(name=jti, value='', ex=JTI_EXPIRE)
     
     
async def token_in_blocklist(jti: str) -> bool:
     jti = await token_blocklist.get(jti)
     
     return jti is not None

