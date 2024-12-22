from settings import CACHE_TYPE
from .base import Cache
from .filesystem import FileSystemCache
from .s3 import S3Cache


def get_cache() -> Cache:
    if CACHE_TYPE == "s3":
        return S3Cache()
    return FileSystemCache()


default_cache = get_cache()
make_key = Cache.make_key
dump_result = default_cache.dump_result
load_result = default_cache.load_result
screenshot_location = default_cache.screenshot_location

__all__ = [
    "Cache",
    "FileSystemCache",
    "S3Cache",
    "make_key",
    "dump_result",
    "load_result",
    "screenshot_location",
]
