import base64
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# 加密，别动

def encrypt(link):
    timestamp = int(time.time() * 1e3)
    rest = link
    text = 'tsmall#{}#{}'.format(timestamp, rest)
    word = 'F3FBA721F9E9233D'
    key = word.encode('utf-8')
    iv = b'f74ae0290a9e4b64'
    aes = AES.new(key, AES.MODE_CBC, iv)
    text_pad = pad(text.encode('utf-8'), AES.block_size, style='pkcs7')
    encrypt_aes = aes.encrypt(text_pad)
    encrypted_text = base64.encodebytes(encrypt_aes).decode('utf-8')
    _final_link = 'https://wxmall.topsports.com.cn%s?tssign=%s' % (link, encrypted_text)
    final_link = _final_link.replace('\n','')
    return final_link


def encrypt_sign(link):
    timestamp = int(time.time() * 1e3)
    rest = link
    text = 'tsmall#{}#{}'.format(timestamp, rest)
    word = 'F3FBA721F9E9233D'
    key = word.encode('utf-8')
    iv = b'f74ae0290a9e4b64'
    aes = AES.new(key, AES.MODE_CBC, iv)
    text_pad = pad(text.encode('utf-8'), AES.block_size, style='pkcs7')
    encrypt_aes = aes.encrypt(text_pad)
    encrypted_text = base64.encodebytes(encrypt_aes).decode('utf-8')
    return encrypted_text
