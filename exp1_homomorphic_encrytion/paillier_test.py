#!/usr/bin/env python3

from phe import paillier

if __name__ == "__main__":
    public_key, private_key = paillier.generate_paillier_keypair()
    message1 = 34
    message2 = 45
    c1 = public_key.encrypt(message1)
    c2 = public_key.encrypt(message2)
    c3 = c1 * message2
    c4 = c1 + c2
    d_message1 = private_key.decrypt(c3)
    d_message2 = private_key.decrypt(c4)
    print(f"传送的信息M1:{message1}")
    print(f"传送的信息M2:{message2}")
    print(f"原始数据乘法同态: {d_message1}")
    print(f"原始数据加法同态: {d_message2}")

