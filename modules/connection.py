import redis as r


REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6397

def redis():
	return r.Redis()
