import time

from gmssl import sm3
import new_SM3


def calculate_sm3(message):
    hasher = sm3.SM3Hash()
    hasher.update(message.encode('utf-8'))
    digest = hasher.finish()
    return digest


message = "Hello, world!"
begin = time.time()
sm3_digest = calculate_sm3(message)
end = time.time()
print("SM3 Digest:", (end - begin) * 1000)
