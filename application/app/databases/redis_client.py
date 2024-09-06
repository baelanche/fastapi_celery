from redis import Redis

class RedisClient(Redis):

    def cache_exists_or_not(self, key, if_exists, if_not_exists):
        cached_value = super().get(key)

        if cached_value:
            return if_exists(cached_value)
        else:
            return if_not_exists()