"""使用到的第三方库：https://github.com/RyanRiddle/elgamal"""
#!/usr/bin/env python3

__author__  = "吴亚戌"
__email__   = "wuyaxu@foxmail.com"

from elgamal import elgamal
import random
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger("elgamal_homomorphic_enc")

keys = elgamal.generate_keys()

def encrypt_integer(key: elgamal.PublicKey, num: int, y=0):
    """按整型进行加密"""
    if y != 0:
        y = random.randint(0, key.p)
    c = elgamal.modexp(key.g, y, key.p)
    d = (num * elgamal.modexp(key.h, y, key.p)) % key.p
    
    return (c, d, y)

def decrypt_integer(key: elgamal.PrivateKey, cipher_pair: tuple):
    c, d = cipher_pair
    s = elgamal.modexp(c, key.x, key.p)
    plain_integer = (d * elgamal.modexp(s, key.p-2, key.p)) % key.p

    return plain_integer

# 明文
i1 = 439
i2 = 892

# 公私钥生成
key = elgamal.generate_keys()
priv, pub = key["privateKey"], key["publicKey"]

logger.info(f"整型明文:\nm1 = {i1}\nm2 = {i2}")
logger.info(f"生成公钥:\n(p, g, h) = ({pub.p}, {pub.g}, {pub.h})")
logger.info(f"生成私钥:\n(p, g, x) = ({priv.p}, {priv.g}, {priv.x})")

c1, d1, y1 = encrypt_integer(pub, i1)
c2, d2, y2 = encrypt_integer(pub, i2)

logger.info(f"m1加密 = ({c1}, {d1})")
logger.info(f"m2加密 = ({c2}, {d2})")

m1 = decrypt_integer(priv, (c1, d1))
m2 = decrypt_integer(priv, (c2, d2))
logger.info(f"c1解密 = {m1}")
logger.info(f"c2解密 = {m2}")

logger.info(f"验证同态加密:\n")
"""E(m1, r1)E(m2, r2) = E(m1m2, r1+r2)
有模的运算可以直接进行，故c3, d3 = (c1 * c2, d1 * d2)
"""
c3, d3 = (c1*c2, d1*d2)     
logger.info(f"同态加密密文: (c1*c2, d1*d2) = ({c3}, {d3})")
m3 = decrypt_integer(priv, (c3, d3))
logger.info(f"验证: {m3} = {m1 * m2})")





