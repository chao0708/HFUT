import time
import new_SM3
from gmssl import sm3

data = "Hello world"
begin = time.time()
print(sm3.sm3_hash(sm3.bytes_to_list(data.encode())))
print("原SM3运行时间：", (time.time() - begin) * 1000, "ms")

begin = time.time()
print(new_SM3.sm3_hash(data))
print("新SM3运行时间：", (time.time() - begin) * 1000, "ms")
