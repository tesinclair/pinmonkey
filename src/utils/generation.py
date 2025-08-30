import random, string

def random_secure_string(length=8):
    return ''.join(random.SystemRandom().choices(
                    string.ascii_letters + 
                    string.digits +
                    string.punctuation, k=length))


