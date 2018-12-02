import os
import sys
import smtplib
import pyAesCrypt
import random
import string

userdetails =[]

def key_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def registration():
    print("welome to registration")
    loop = 'true'
    while(loop == 'true'):
        username = input("enter username: ")
        if not username:
            print("username cannot be empty")
        else:
            if username in open('userlist.txt').read():## here database read commands comes in#
                 print("username already exists choose new one ")

            else:
                userdetails.append(username)
                loop = 'false'
    loop = 'true'
    while(loop == 'true'):
        emailid =input("enter email address: ")
        if not emailid:
            print("email id cannot be emptty")
        else:
            if emailid in open('userlist.txt').read():## here database read commands comes in#
                 print("emailid  already exists choose new one ")
         
            else:
                server=smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("cloudr9.rutgers@gmail.com", "Hunter321")
                msg = key_generator() # The /n separates the message from the headers
                server.sendmail("cloud9@rutgers.com", emailid, msg)
                server.close()
                loopinside = 'true'
                while(loopinside == 'true'):
                    verifycode = input("Verification Mail sent to your mail address enter the code: ")
                    if (verifycode == msg):
                        print("email successfully verified")
                        loopinside = 'false'
                loop = 'false'
                userdetails.append(emailid)
    loop = 'true'
    while(loop == 'true'):
        password = input("enter a password: ")
        if not password:
            print("password must be non empty")
        else:
            repassword = input("retype password:")
            if(password == repassword):
                userdetails.append(password)
                loop == 'false'
                break
            else:
                print("passwords do not match")

    print(userdetails)# here databse write command goes##
    return