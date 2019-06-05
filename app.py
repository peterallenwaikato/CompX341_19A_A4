import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
	retries = 5
	while True:
		try:
			return cache.incr('hits')
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)
@app.route('/isPrime/<int:prime>')
def isPrime(prime):
	if prime > 1:    
		for i in range(2,prime):
			if (prime % i) == 0:          
				break
		else:
			cache.sadd('primes',str(prime) + " ")
			
			return(str(prime) + " is a prime number\n")
				      	
	else:
		return(str(prime) + " is not a prime number\n")
	return(str(prime) + " is not a prime number\n") 
@app.route('/primesStored')
def returnPrimes():
	count = cache.smembers('primes')
	string = ""		
	for var in count:
		string +=var.decode("utf-8")
	if len(count) == 0:
		return("Cache is empty\n")
	else:
		return string
	

@app.route('/clear')
def clear():
	cache.flushdb()
	return("done\n")

