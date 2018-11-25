import os
import sys
import array
import pyAesCrypt
import random
import string
from fileinput import filename

# encryption/decryption buffer size - 64K
with open('files.txt') as f:
    content = f.read().splitlines()
    array1=content[0].split()
    array2=content[1].split()


bufferSize = 64 * 1024
f = open("pass.txt", "r")
passkeyread = f.read()
f.close()

pyAesCrypt.decryptFile(array1[1], array1[0], passkeyread, bufferSize)
pyAesCrypt.decryptFile(array2[1], array2[0], passkeyread, bufferSize)

f=open("original.txt")
original = f.read()
f.close()

output = open(original, 'wb')
fileobj  = open(array1[0], 'rb')
fileobjbytes = fileobj.read()
output.write(fileobjbytes)
fileobj.close()
fileobj  = open(array2[0], 'rb')
fileobjbytes = fileobj.read()
output.write(fileobjbytes)
fileobj.close()
output.close()


if os.path.exists(array1[0]):
  os.remove(array1[0])

if os.path.exists(array1[1]):
  os.remove(array1[1])

if os.path.exists(array2[0]):
  os.remove(array2[0])

if os.path.exists(array2[1]):
  os.remove(array2[1])  

if os.path.exists("original.txt"):
  os.remove("original.txt")

if os.path.exists("pass.txt"):
  os.remove("pass.txt")

if os.path.exists("files.txt"):
  os.remove("files.txt")

print("Joining complete ")
