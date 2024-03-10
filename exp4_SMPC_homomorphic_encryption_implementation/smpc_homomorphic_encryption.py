#!/usr/bin/env python3 

from phe import paillier
import random

class Millionaire:
    """百万富翁"""

    def __init__(self, pub=None, priv=None, treasure=None, gen_keys=False):

        self.public_key = pub           # 可能生成的公钥
        self.private_key = priv         # 可能生成的私钥
        self.treasure = treasure
        
        if gen_keys:
            self.generate_keys()

    def generate_keys(self):

        pub, priv = paillier.generate_paillier_keypair()
        self.public_key = pub
        self.private_key = priv

    def getKeys(self):
        return self.public_key, self.private_key

    def setTreasure(self, treasure):

        self.treasure = treasure

    def getTreasure(self):
        return self.treasure

class Alice(Millionaire):
    
    def __init__(self, treasure=None, gen_keys=False):

        Millionaire.__init__(self, treasure=treasure, gen_keys=True)
        if not isinstance(treasure, int) and treasure != 0:
            self.setTreasure(random.randint(1, 100))      #随机给Alice一个财富

    def decrypt_bobs_message(self, t1, t2):
        message1 = self.private_key.decrypt(t1)
        message2 = self.private_key.decrypt(t2)

        return message1, message2

class Bob(Millionaire):

    def __init__(self, treasure=None, gen_keys=False):
        
        self.x = None
        self.y = None
        Millionaire.__init__(self, treasure=treasure, gen_keys=False)
        if not isinstance(treasure, int) and treasure != 0:
            self.setTreasure(random.randint(1, 100))        #随机给Bob一个财富

        self.generate_rand_int()

    def generate_rand_int(self):

        self.x = random.randint(1, 1000000)
        self.y = random.randint(1, 1000000)

    def homomorphic_calc(self, public_key, c1, c2):

        t1 = c1*self.x + public_key.encrypt(self.y)
        t2 = c2*self.x + public_key.encrypt(self.y)

        return t1, t2
        
if __name__ == "__main__":

    Alice   = Alice(gen_keys=True) # Alice生成keys
    Bob     = Bob()

    print(f"Alice的财富: {Alice.getTreasure()}\nBob的财富: {Bob.getTreasure()}")

    pub, priv = Alice.getKeys()
    
    # 将Alice和Bob的财富加密
    c1 = pub.encrypt(Alice.getTreasure())
    c2 = pub.encrypt(Bob.getTreasure())

    r = Alice.decrypt_bobs_message(*Bob.homomorphic_calc(pub, c1, c2))

    if r[0] > r[1]:
        print("Alice更富有")
    elif r[0] < r[1]:
        print("Bob更富有")
    else:
        print("Alice和Bob一样富有")
