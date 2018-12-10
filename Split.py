import os
import sys
import array
import pyAesCrypt
import random
import string
from fileinput import filename
import mysql.connector

mydb = mysql.connector.connect(
  host="cloudnine.c87lmy1ftwtu.us-east-2.rds.amazonaws.com",
  user="modi1234",
  passwd="Was160497",
  database="CloudNine"
)


mycursor = mydb.cursor()

# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024

str_google = "google"
str_dropbox = "dropbox"
filename = sys.argv[1]
file1 = filename + str_google
file2 = filename + str_dropbox
names = [file1, file2]
size = 2

def key_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def split_files(filename, size):
    with open(filename, 'rb') as mfile:
        data = mfile.read()
        bytes = len(data)
        noOfChunks = bytes / size
        if ((bytes % size) != 0):
            noOfChunks += 1
        f = open(file1, 'wb')
        f.write(data[0:int(noOfChunks)])
        f.close()
        g = open(file2, 'wb')
        g.write(data[int(noOfChunks) + 1:int(bytes)])
        g.close()

    passwordkey = key_generator()
    f = open("pass.txt", "w+")
    f.write(passwordkey)
    f.close()

    split_files(filename, 2)
    
    

    aes = ".aes"
    file1aes = file1 + aes
    pyAesCrypt.encryptFile(file1, file1aes, passwordkey, bufferSize)
    file2aes = file2 + aes
    pyAesCrypt.encryptFile(file2, file2aes, passwordkey, bufferSize)

    f = open("original.txt", "w+")
    modified = filename
    f.write(modified)
    f.close()

    f = open("fileslist.txt", "w+")
    f.write(file1)
    f.write("  ")
    f.write(file1aes)
    f.write("\n")
    f.write(file2)
    f.write("  ")
    f.write(file2aes)
    f.write("\n")
    f.close()

    if os.path.exists(file1):
        os.remove(file1)

    if os.path.exists(file2):
        os.remove(file2)

    if os.path.exists(filename):
        os.remove(filename)
        
    sql = "INSERT INTO fileinfo (filename, cloud_provider, encryption_key) VALUES (%s,%s,%s)"
    val = (file1, "google", passwordkey)
    mycursor.execute(sql, val)
    mydb.commit()
    
    sql = "INSERT INTO fileinfo (filename, cloud_provider, encryption_key) VALUES (%s,%s,%s)"
    val = (file2, "dropbox", passwordkey)
    mycursor.execute(sql, val)
    mydb.commit()

    print("splitting complete ")
    return
