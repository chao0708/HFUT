whitespaces = [0x00A0, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006,
               0x2007, 0x2008, 0x2009, 0x200A, 0x202F, 0x205F, 0x200B, 0x2060]


def python_en(msg_lst, hash_value):
    new_msg_lst = []
    bit = 0
    # 对应多行注释、输入和输出 单行注释
    judge_1, judge_2, judge_3 = 0, 0, 0

    for i in msg_lst:
        if bit == len(hash_value):
            new_msg_lst.append(i)

        else:
            i_lst = list(i)

            if '"""' in i:
                judge_1 = (judge_1 + 1) % 2

            if "input(" in i or "print(" in i:
                judge_2 = 1

            if "#" in i:
                judge_3 = 1

            if judge_1 == 1:
                for j in range(len(i_lst)):
                    if i_lst[j] == " " and bit != len(hash_value):
                        i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                        bit += 1

            else:
                if judge_2 == 1:
                    idx = i.index("t(")
                    judge = 0
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == "\"":
                            judge = (judge + 1) % 2
                        elif i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_2 = 0

                if judge_3 == 1:
                    idx = i.index("#")
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == " " and bit != len(hash_value):
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_3 = 0

            # 将列表中的元素拼接成代码
            line = ''.join(i_lst)
            new_msg_lst.append(line)

    return new_msg_lst, bit


def c_en(msg_lst, hash_value):
    new_msg_lst = []
    bit = 0
    judge_1, judge_2, judge_3 = 0, 0, 0  # 对应多行注释、单行注释、输入和输出

    for i in msg_lst:
        if bit == len(hash_value):
            new_msg_lst.append(i)

        else:
            i_lst = list(i)

            if "/*" in i or "*/" in i:
                judge_1 = (judge_1 + 1) % 2

            if "printf(" in i:
                judge_2 = 1

            if "//" in i:
                judge_3 = 1

            if judge_1 == 1:
                judge = 0
                for j in range(len(i_lst)):
                    if i_lst[j] != " ":
                        judge = 1
                    if i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                        i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                        bit += 1

            else:
                if judge_2 == 1:
                    idx = i.index("f(")
                    judge = 0
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == "\"":
                            judge = (judge + 1) % 2
                        elif i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_2 = 0

                if judge_3 == 1:
                    idx = i.index("//")
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == " " and bit != len(hash_value):
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_3 = 0

            line = ''.join(i_lst)
            new_msg_lst.append(line)

    return new_msg_lst, bit


def cpp_en(msg_lst, hash_value):
    new_msg_lst = []
    bit = 0
    judge_1, judge_2, judge_3 = 0, 0, 0  # 对应多行注释、单行注释、输入和输出

    for i in msg_lst:
        if bit == len(hash_value):
            new_msg_lst.append(i)

        else:
            i_lst = list(i)

            if "/*" in i or "*/" in i:
                judge_1 = (judge_1 + 1) % 2

            if "cout" in i:
                judge_2 = 1

            if "//" in i:
                judge_3 = 1

            if judge_1 == 1:
                judge = 0
                for j in range(len(i_lst)):
                    if i_lst[j] != " ":
                        judge = 1
                    if i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                        i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                        bit += 1

            else:
                if judge_2 == 1:
                    idx = i.index("cout")
                    judge = 0
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == "\"":
                            judge = (judge + 1) % 2
                        elif i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_2 = 0

                if judge_3 == 1:
                    idx = i.index("//")
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == " " and bit != len(hash_value):
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_3 = 0

            line = ''.join(i_lst)
            new_msg_lst.append(line)

    return new_msg_lst, bit


def java_en(msg_lst, hash_value):
    new_msg_lst = []
    bit = 0
    judge_1, judge_2, judge_3 = 0, 0, 0  # 对应多行注释、单行注释、输入和输出

    for i in msg_lst:
        if bit == len(hash_value):
            new_msg_lst.append(i)

        else:
            i_lst = list(i)

            if "/*" in i or "*/" in i:
                judge_1 = (judge_1 + 1) % 2

            if "print(" in i or "println(" in i:
                judge_2 = 1

            if "//" in i:
                judge_3 = 1

            if judge_1 == 1:
                judge = 0
                for j in range(len(i_lst)):
                    if i_lst[j] != " ":
                        judge = 1
                    if i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                        i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                        bit += 1

            else:
                if judge_2 == 1:
                    idx = i.index("print")
                    judge = 0
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == "\"":
                            judge = (judge + 1) % 2
                        elif i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_2 = 0

                if judge_3 == 1:
                    idx = i.index("//")
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == " " and bit != len(hash_value):
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_3 = 0

            line = ''.join(i_lst)
            new_msg_lst.append(line)

    return new_msg_lst, bit


def javascript_en(msg_lst, hash_value):
    new_msg_lst = []
    bit = 0
    judge_1, judge_2, judge_3 = 0, 0, 0  # 对应多行注释、单行注释、输入和输出

    for i in msg_lst:
        if bit == len(hash_value):
            new_msg_lst.append(i)

        else:
            i_lst = list(i)

            if "/*" in i or "*/" in i:
                judge_1 = (judge_1 + 1) % 2

            if "prompt(" in i or "log(" in i:
                judge_2 = 1

            if "//" in i:
                judge_3 = 1

            if judge_1 == 1:
                judge = 0
                for j in range(len(i_lst)):
                    if i_lst[j] != " ":
                        judge = 1
                    if i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                        i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                        bit += 1

            else:
                if judge_2 == 1:
                    idx = i.index("(")
                    judge = 0
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == "\"":
                            judge = (judge + 1) % 2
                        elif i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_2 = 0

                if judge_3 == 1:
                    idx = i.index("//")
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == " " and bit != len(hash_value):
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_3 = 0

            line = ''.join(i_lst)
            new_msg_lst.append(line)

    return new_msg_lst, bit


def php_en(msg_lst, hash_value):
    new_msg_lst = []
    bit = 0
    judge_1, judge_2, judge_3 = 0, 0, 0  # 对应多行注释、单行注释、输入和输出

    for i in msg_lst:
        if bit == len(hash_value):
            new_msg_lst.append(i)

        else:
            i_lst = list(i)

            if "/*" in i or "*/" in i:
                judge_1 = (judge_1 + 1) % 2

            if "readline(" in i or "echo" in i:
                judge_2 = 1

            if "//" in i:
                judge_3 = 1

            if judge_1 == 1:
                judge = 0
                for j in range(len(i_lst)):
                    if i_lst[j] != " ":
                        judge = 1
                    if i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                        i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                        bit += 1

            else:
                if judge_2 == 1:
                    idx = i.index("\"")
                    judge = 0
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == "\"":
                            judge = (judge + 1) % 2
                        elif i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_2 = 0

                if judge_3 == 1:
                    idx = i.index("//")
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == " " and bit != len(hash_value):
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_3 = 0

            line = ''.join(i_lst)
            new_msg_lst.append(line)

    return new_msg_lst, bit


def go_en(msg_lst, hash_value):
    new_msg_lst = []
    bit = 0
    judge_1, judge_2, judge_3 = 0, 0, 0  # 对应多行注释、单行注释、输入和输出

    for i in msg_lst:
        if bit == len(hash_value):
            new_msg_lst.append(i)

        else:
            i_lst = list(i)

            if "/*" in i or "*/" in i:
                judge_1 = (judge_1 + 1) % 2

            if "Print(" in i or "Println(" in i:
                judge_2 = 1

            if "//" in i:
                judge_3 = 1

            if judge_1 == 1:
                judge = 0
                for j in range(len(i_lst)):
                    if i_lst[j] != " ":
                        judge = 1
                    if i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                        i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                        bit += 1

            else:
                if judge_2 == 1:
                    idx = i.index("Print")
                    judge = 0
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == "\"":
                            judge = (judge + 1) % 2
                        elif i_lst[j] == " " and bit != len(hash_value) and judge == 1:
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_2 = 0

                if judge_3 == 1:
                    idx = i.index("//")
                    for j in range(idx, len(i_lst)):
                        if i_lst[j] == " " and bit != len(hash_value):
                            i_lst[j] = chr(whitespaces[int(hash_value[bit], 16)])
                            bit += 1
                    judge_3 = 0

            line = ''.join(i_lst)
            new_msg_lst.append(line)

    return new_msg_lst, bit
