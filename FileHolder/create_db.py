import redis

r = redis.Redis()

testFile = open('database', 'r')
fileLines = testFile.readlines()
for line in fileLines:
  userData = line.split(' ')
  login = userData[0]
  password = userData[2]
  r.hset('sawickij:webapp:users', login, password)
