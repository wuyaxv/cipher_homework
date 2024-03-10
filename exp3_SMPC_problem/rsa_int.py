"""验证RSA乘法同态"""

__author__  = "吴亚戌"
__email__   = "wuyaxu@foxmail.com"

import logging
from cryptography.hazmat.primitives.asymmetric import rsa

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger("rsa_homomorphic_enc")

EXPONENT = 65537            # RSA中的e

def generate_keys() -> tuple:
    """生成公私钥(pub, priv)
    """

    # 生成公私钥实例RSAPublicKey与RSAPrivateKey
    priv = rsa.generate_private_key(EXPONENT, 512)
    pub  = priv.public_key()
    
    pub_num     = {"n": pub.public_numbers().n, "e": pub.public_numbers().e} #公钥 (n, e)
    priv_num    = {"p": priv.private_numbers().p, "q": priv.private_numbers().q, "d": priv.private_numbers().d} # 私钥(n, d)

    return (pub_num, priv_num)

def encryption(pub, message):
    """RSA加密:
    c = m ^ e mod n
    """

    return pow(message, pub["e"], pub["n"])

def decryption(priv, message):
    """RSA解密:
    m = c ^ d mod n
    """

    return pow(message, priv["d"], priv["p"]*priv["q"])


if __name__ == '__main__':
    pub, priv = generate_keys()
    logger.info(f"公钥:\nn: {pub['n']},\ne: {pub['e']}")
    logger.info(f"私钥:\nn: {pub['n']},\nd: {priv['d']}")

    m1, m2 = 37, 22                         # 随便选两个值
    logger.info(f"明文:\nm1: {m1},\nm2: {m2}")

    c1 = encryption(pub, m1)                # 先进行加密f(m1), f(m2)
    c2 = encryption(pub, m2)
    logger.info(f"密文:\nc1: {c1},\nc2: {c2}")

    homo = c1 * c2                          # 验证 f(m1) * f(m2) = f(m1 * m2)
    logger.info(f"同态加密密文:\nc1 * c2: {homo}")
    
    homo_d = decryption(priv, homo)
    logger.info(f"同态解密明文验证:\n{homo_d} = {m1 * m2}")

    

