from phe import paillier
import random

class Client:
    
    def __init__(self, s=list(), gen_keys=True, domainSize=100):

        self.domainSize = domainSize
        self.priv   = None
        self.pub    = None
        self.index  = []

        self.setSets(s)

        if gen_keys:
            self.generate_keys()

    def generate_keys(self):

        self.pub, self.priv = paillier.generate_paillier_keypair()

    def getEncryptedSets(self):

        i = [0 for i in range(self.domainSize)]
        enc_sets = []
        for _ in self.index:
            i[_] = 1
        for _ in i:
            enc_sets.append(self.pub.encrypt(_))
        return enc_sets

    def client2server(self):
        return (self.getEncryptedSets(), 
                self.pub
                )

    def decrypt_from_server(self, bob_multiplied):

        r = []
        for i in bob_multiplied:
            r.append(self.priv.decrypt(i))

        return r

    def setSets(self, s):

        self.index.clear()
        if isinstance(s, list) and len(s) != 0 and (i < self.domainSize and i >= 0 for i in s):
            self.index.extend(s)
        else:
            print("集合不满足要求")

class Server:

    def __init__(self, data=[], domainSize=100):

        self.data = []
        self.domainSize = domainSize
        self.index = [0 for i in range(self.domainSize)]
        
        self.setData(data)


    def homomorphic_calc(self, alice_enc):
        
        r = []
        for i in range(self.domainSize):
            r.append(alice_enc[i] * self.index[i])
            
        return r

    def setData(self, s):
        if isinstance(s, list) and len(s) != 0 and (i < self.domainSize and i >= 0 for i in s):
            self.data.clear()
            self.data.extend(s)
            for i in range(len(self.index)):
                self.index[i] = 0
            for i in self.data:
                self.index[i] = 1
        else:
            print("集合不满足要求")

if __name__ == "__main__":
    client_set = [0, 7, 9, 25, 31, 44, 39, 67, 10, 84, 93, 26, 14, 3, 21]
    server_set = [9, 7, 25, 4, 24, 18, 39, 44, 32, 13, 55, 69, 96, 71, 38, 46, 64, 21]

    print("client集合", client_set)
    print("server集合", server_set)

    s = Server(server_set)
    c = Client(s=client_set, gen_keys=True)

    result = s.homomorphic_calc(c.getEncryptedSets())
    domain_result = c.decrypt_from_server(result)
    for i in range(len(domain_result)):
        if domain_result[i]:
            print(i, end=" ")
    print()
