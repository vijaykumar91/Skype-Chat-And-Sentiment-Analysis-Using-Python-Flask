import win32crypt
import bottle
from bottle import get, request, run, route
import binascii

#
# @get('/decryptCookie')
# def decryptCookie():
decrypted_cookies = ''
hexstrs = request.query.encrypted_values

for hexstr in hexstrs.split('--'):
    encrypted_cookie = binascii.unhexlify(hexstr)

    decrypted_cookie = win32crypt.CryptUnprotectData(encrypted_cookie, None, None, None, 0)[1]
    decrypted_cookies = decrypted_cookies + ';' + decrypted_cookie

   # return decrypted_cookies[1:]


run(host='localhost', port=8080, quiet=True, debug=False)