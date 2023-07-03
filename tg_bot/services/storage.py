from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis


def init_storage(is_redis: bool, host_name: str) -> BaseStorage:
    if is_redis:
        return RedisStorage(redis=Redis(host=host_name))

    return MemoryStorage()
