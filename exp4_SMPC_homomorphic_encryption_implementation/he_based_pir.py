from phe import paillier
import random

class Alice:
    
    def __init__(self, gen_keys=True, domainSize=100):

        self.domainSize = domainSize    # N维向量的维度
        self.priv   = None
        self.pub    = None
        self.index  = []

        if gen_keys:
            self.generate_keys()

    def generate_keys(self):
        # Alice生成公私钥

        self.pub, self.priv = paillier.generate_paillier_keypair()

    def lookup(self, pos):
        """查询索引为pos的数据"""

        s = []
        for i in range(0, pos):
            s.append(self.pub.encrypt(0))
        s.append(self.pub.encrypt(1))
        for i in range(pos+1, self.domainSize):
            s.append(self.pub.encrypt(0))
        
        return s

    def Alice2Bob(self, pos):
        """发送给Bob"""
        
        return self.lookup(pos)
        
    def decrypt_result(self, bob_):

        return self.priv.decrypt(bob_)

class Bob:

    def __init__(self, domainSize=100, s=[]):

        self.domainSize = domainSize
        self.set = None
        if len(s) != self.domainSize:
            self.set = [random.randint(0, 1000) for i in range(self.domainSize)]   # Bob生成随机n维度向量
        else:
            self.set = [_ for _ in s]

    def __str__(self):
        s = "Bob的N维向量:\n" + "{ "
        for _ in self.set[:-1]:
            s += str(_) + ", "
        s += str(self.set[-1])
        s += "}"

        return s

    def homomorphic_calc(self, alice_enc):
        """计算Alice发来的加密向量"""
        
        if len(alice_enc) == self.domainSize:
            addup = alice_enc[0] * self.set[0]
            for i in range(1, self.domainSize):
                addup += alice_enc[i] * self.set[i]
            
            return addup

        return None

if __name__ == "__main__":
    bob = Bob()
    alice = Alice()
    print(bob)
    print("查询结果:", \
            alice.decrypt_result(bob.homomorphic_calc(alice.Alice2Bob(32)))) # 查询index=32处元素

