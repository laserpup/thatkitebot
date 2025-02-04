from discord import Message
from aioredis import Redis


async def add_message_to_cache(redis: Redis, message):
    key = f"{message.guild.id}:{message.channel.id}:{message.author.id}:{message.id}"
    msgdict = dict(
        content=message.content,
        clean_content=message.clean_content,
        created_at=message.created_at.timestamp()
    )
    await redis.hmset(key, msgdict)
    return message


async def get_contents(redis: Redis, gid, cid, uid):
    key = f"{gid}:{cid}:{uid}:*"
    a = []
    async for mkey in redis.scan_iter(key):
        a.append(await redis.hget(mkey, "clean_content"))
    return a
