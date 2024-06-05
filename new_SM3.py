import binascii
from numba import njit, uint32, int64
import numpy as np


@njit(uint32(int64), nogil=True, cache=True)
def i8_u4(x):
    return x


p32 = i8_u4(1 << 32)
mod32 = uint32(p32 - 1)

IV = np.asarray([0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e],
                np.uint32)
TJ = np.asarray([2043430169, 2055708042], np.uint32)


@njit(uint32[::1](uint32[::1], uint32[::1]), nogil=True, cache=True)
def CF(V, B_):
    W = np.empty((68,), np.uint32)
    for i in range(0, len(B_), 16):
        W[:4] = B_[i:i + 4]
        A, B, C, D, E, F, G, H = V
        tj = TJ[0]
        for j in range(16):
            if j < 12:
                W[j + 4] = B_[i + j + 4]
            else:
                temp0 = W[j - 12] ^ W[j - 5] ^ i8_u4(W[j + 1] << 15 | W[j + 1] >> 17)
                W[j + 4] = i8_u4(temp0 ^ (temp0 << 15 | temp0 >> 17) ^ (temp0 << 23 | temp0 >> 9)) ^ i8_u4(
                    W[j - 9] << 7 | W[j - 9] >> 25) ^ W[j - 2]
            temp0 = ((A << 12) | (A >> 20)) & mod32
            temp1 = (temp0 + E + tj) & mod32
            tj = ((tj << 1) | (tj >> 31)) & mod32
            temp1 = (temp1 << 7 | temp1 >> 25) & mod32
            temp0 = temp1 ^ temp0
            temp0 = ((A ^ B ^ C) + D + temp0 + (W[j] ^ W[j + 4])) & mod32
            temp1 = ((E ^ F ^ G) + H + temp1 + W[j]) & mod32
            A, B, C, D = temp0, A, i8_u4((B << 9) | (B >> 23)), C
            E, F, G, H = i8_u4(temp1 ^ (temp1 << 9 | temp1 >> 23) ^ (temp1 << 17 | temp1 >> 15)), E, i8_u4(
                F << 19 | F >> 13), G

        tj = np.uint32(0x9d8a7a87)
        for j in range(16, 64):
            temp0 = W[j - 12] ^ W[j - 5] ^ i8_u4(W[j + 1] << 15 | W[j + 1] >> 17)
            W[j + 4] = i8_u4(temp0 ^ (temp0 << 15 | temp0 >> 17) ^ (temp0 << 23 | temp0 >> 9)) ^ i8_u4(
                W[j - 9] << 7 | W[j - 9] >> 25) ^ W[j - 2]
            temp0 = ((A << 12) | (A >> 20)) & mod32
            temp1 = (temp0 + E + tj) & mod32
            tj = ((tj << 1) | (tj >> 31)) & mod32
            temp1 = (temp1 << 7 | temp1 >> 25) & mod32
            temp0 = temp1 ^ temp0
            temp0 = (((A & B) | (B & C) | (C & A)) + D + temp0 + (W[j] ^ W[j + 4])) & mod32
            temp1 = (((E & F) | ((~E) & G)) + H + temp1 + W[j]) & mod32
            A, B, C, D = temp0, A, i8_u4((B << 9) | (B >> 23)), C
            E, F, G, H = i8_u4(temp1 ^ (temp1 << 9 | temp1 >> 23) ^ (temp1 << 17 | temp1 >> 15)), E, i8_u4(
                F << 19 | F >> 13), G
        V[:] = V[0] ^ A, V[1] ^ B, V[2] ^ C, V[3] ^ D, V[4] ^ E, V[5] ^ F, V[6] ^ G, V[7] ^ H
    return V


def sm3_hash(msg):
    if isinstance(msg, str):
        msg = bytes(msg, encoding='utf-8')
    pad_num = 64 - ((len(msg) + 1) & 0x3f)
    msg += b'\x80' + (len(msg) << 3).to_bytes(pad_num if pad_num >= 8 else pad_num + 64, 'big')
    V = binascii.b2a_hex(CF(np.copy(IV), np.frombuffer(msg, np.uint32).byteswap()).byteswap().tobytes()).decode()
    return V
