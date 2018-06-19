# GENERATED WITH: 'angecryption.py'

# This script decrypts the file 'zipflv.zip' that is located
# in 'result/ZIPFLV' and writes the result into the file
# 'zipflv.flv' that will also be located in 'result/ZIPFLV'.
# The decryption key is 'MySuperSecureKey'
from Crypto.Cipher import AES

algo = AES.new('MySuperSecureKey', AES.MODE_CBC, '\x1d\x9e\xa6\xd1\t0\xb04\x91\x95\xf9\xf2[\\\x8f\xc6')

with open('../result/ZIPFLV/zipflv.zip', 'rb') as f:
	d = f.read()

d = algo.encrypt(d)

with open('../result/ZIPFLV/zipflv.flv', 'wb') as f:
	f.write(d)
