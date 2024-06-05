whitespaces = [0x00A0, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006,
               0x2007, 0x2008, 0x2009, 0x200A, 0x202F, 0x205F, 0x200B, 0x2060]


def decode(msg_lst, length):

    # 记录提取的消息和嵌入比特数
    bit = 0
    decode_message = ""
    new_msg_lst = []

    for i in msg_lst:

        # 达到嵌入上限则不进行判断
        if bit == length:
            new_msg_lst.append(i)
        else:
            i_lst = list(i)

            # 遍历替换其中全部的特殊字符
            for j in range(len(i_lst)):
                if ord(i_lst[j]) in whitespaces and bit != length:
                    decode_message += hex(whitespaces.index(ord(i_lst[j])))[2:].lower()
                    i_lst[j] = chr(0x0020)
                    bit += 1

            # 将所有的字符拼接成一行代码并存入列表
            line = ''.join(i_lst)
            new_msg_lst.append(line)

    return new_msg_lst, decode_message

