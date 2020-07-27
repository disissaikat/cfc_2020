from cryptography.fernet import Fernet
key = b'mlgHc4CrmeiVLmR82I1dRTL7zrR-Dff-k8mS_x7x1uY='
cipher_suite = Fernet(key)

def encrypt_pwd(pwd):
    byte_pwd = bytes(pwd, 'utf-8') #convert to byte for encryption
    ciphered_pwd = cipher_suite.encrypt(byte_pwd) 
    ciphered_pwd = str(ciphered_pwd, 'utf-8')
    return ciphered_pwd

def decrypt_pwd(pwd):
    byte_pwd = bytes(pwd, 'utf-8') #convert to byte for encryption
    decryptpwd = (cipher_suite.decrypt(byte_pwd))
    decryptpwd = str(decryptpwd, 'utf-8')
    return decryptpwd