from elgamal.elgamal import find_prime, gcd

class PublicKey:
    """RSA公钥"""
    
    def __init__(self, p=None, q=None):
        self.p = p
        self.q = q
        self.phi = None
        self.e = None

        self.generate()

    def generate():

class PrivateKey:
    """RSA私钥"""

    def __init__(self, p=None, q=None):
        self.p = p
        self.q = q
        self.phi = None
        self.d = None

        self.generate()

    def generate()


