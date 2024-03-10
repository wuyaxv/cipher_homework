#!/usr/bin/env python3

"""百万富翁问题实现"""

"""
N = 100
加密算法：RSA
"""

import logging
import rsa_int
import random
from elgamal.elgamal import find_prime      # 在实验一中我们用到的查找大素数的函数

N = 100

class Millionaire:
    
    def __init__(self, f):
        self.fortune = f             # 富翁的财富

    def getFortune(self):
        return self.fortune
        
def Alice_2_Bob(Alice, pub):
    """Alice发送给Bob的内容"""

    rand_num = random.randint(1, 1000)  # Alice生成一个随机数
    return rsa_int.encryption(pub, rand_num) - Alice.getFortune(), rand_num

def Bob_2_Alice(Bob, priv, from_Alice):
    """Bob从Alice处接收加密数据"""

    Yn = [rsa_int.decryption(priv, from_Alice+u) for u in range(1, N+1) ]
    Zn = []

    while(True):
        prime = find_prime(64, 16)      # confidence=16使用solovay-strassen素数判定来查找64位的素数，64位是我随便设的，过大的话太慢了
        Zn.clear()
        Zn.append(Yn[0] % prime)
        for i in range(1, 99):
            Zn.append(Yn[i] % prime)
            for j in range(0, i):
                if abs(Zn[i] - Zn[j]) < 2:
                    continue
        break
    for i in range(Bob.fortune, N-1):
        Zn[i] += 1

    return Yn, Zn, prime

def if_Alice_richer(Alice, from_bob, prime, rand_num):
    if from_bob[Alice.getFortune()-1] == (rand_num % prime):
        return False
    else:
        return True

if __name__ == "__main__":

    logging.basicConfig(format='[*] %(message)s', level=logging.INFO)
    logger = logging.getLogger("foo")

    # 生成RSA公私钥
    pub, priv = rsa_int.generate_keys()

    Alice   = Millionaire(random.randint(1, 100))
    Bob     = Millionaire(random.randint(1, 100))

    print(f"Alice的财富值:  {Alice.getFortune()}")
    print(f"Bob的财富值:    {Bob.getFortune()}")

    from_Alice, rand_num = Alice_2_Bob(Alice, pub)
    print(f"随机整数: {rand_num}")
    print(f"公钥:\nn: {pub['n']},\ne: {pub['e']}")
    print(f"私钥:\nn: {pub['n']},\nd: {priv['d']}")
    print(f"Alice发送C-i给Bob: \n{from_Alice}")

    Yn, Zn, prime = Bob_2_Alice(Bob, priv, from_Alice)
    print(f"Yn: \n{Yn}")
    print(f"Zn: \n{Zn}")
    print("Alice是否比Bob富有:", if_Alice_richer(Alice, Zn, prime, rand_num))
    

