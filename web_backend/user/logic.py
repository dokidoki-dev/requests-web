from random import Random
import hashlib


# 生成密码盐
def hash_salt(l=8):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in range(l):
        salt += chars[random.randint(0, len_chars)]
    salt = hashlib.md5(salt.encode('utf-8')).hexdigest()
    return salt
