import bcrypt
import hashlib, binascii
import random, string


def random_salt():
    return bcrypt.gensalt()


def encrypt_pass(passw , salt):
    try:
        dk = hashlib.pbkdf2_hmac('sha256', passw.encode('utf-8'), salt.encode('utf-8'), 9503)
        return binascii.hexlify(dk).decode('utf-8')
    except Exception as e:
        print(e)


def get_random(number):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(number))


def get_random_num(number):
    return ''.join(random.choice(string.digits) for x in range(number))


def get_random_str(number):
    return ''.join(random.choice(string.ascii_letters) for x in range(number))

