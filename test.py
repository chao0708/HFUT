import Decode
import Encode
import new_SM3

with open('25.cpp.html', 'r', encoding='utf-8') as file:
    msg = file.read()

msg_lst = msg.split('\n')
hash_value = new_SM3.sm3_hash(msg)

new_msg_lst, bit = Encode.html_en(msg_lst, hash_value)

new_line = '\n'.join(new_msg_lst)

with open('2.html', 'w', encoding='utf-8') as file:
    file.write(new_line)

msg_lst = new_line.split('\n')
new_msg_lst, decode_message = Decode.decode(msg_lst, 64)
print(len(decode_message) * 4)

new_line = '\n'.join(new_msg_lst)
with open('3.html', 'w', encoding='utf-8') as file:
    file.write(new_line)

hash = new_SM3.sm3_hash(new_line)
if decode_message == hash[:len(decode_message):]:
    print(True)
else:
    print(False)