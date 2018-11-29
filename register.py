import os
import sys
import smtplib
import pyAesCrypt
import random
import string
import mysql.connector

mydb = mysql.connector.connect(
  host="cloudnine.c87lmy1ftwtu.us-east-2.rds.amazonaws.com",
  user="modi1234",
  passwd="Was160497",
  database="CloudNine"
)


mycursor = mydb.cursor()

userdetails = []


def key_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
  



print("welome to registration")
loop = 'true'
while (loop == 'true'):
    username = input("enter username: ")
    if not username:
        print("username cannot be empty")
    else:
        mycursor.execute("SELECT username FROM user")
        myresult = mycursor.fetchall()
        for y in myresult:
            x = ''.join(y)
            if(x==user):
          #if username in open('userlist.txt').read():  ## here database read commands comes in#
              print("username already exists choose new one ")
            else:
              #userdetails.append(username)
              loop = 'false'
loop = 'true'
while (loop == 'true'):
    emailid = input("enter email address: ")
    if not emailid:
        print("email id cannot be emptty")
    else:
        mycursor.execute("SELECT email FROM user")
        myresult = mycursor.fetchall()
        for y in myresult:
            x = ''.join(y)
            if(x==emailid):
        #if emailid in open('userlist.txt').read():  ## here database read commands comes in#
              print("emailid  already exists choose new one ")

        else:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("cloudr9.rutgers@gmail.com", "Hunter321")
            msg = key_generator()  # The /n separates the message from the headers
            server.sendmail("cloud9@rutgers.com", emailid, msg)
            server.close()
            loopinside = 'true'
            while (loopinside == 'true'):
                verifycode = input("Verification Mail sent to your mail address enter the code: ")
                if (verifycode == msg):
                    print("email successfully verified")
                    loopinside = 'false'
            loop = 'false'
            #userdetails.append(emailid)
loop = 'true'
while (loop == 'true'):
    password = input("enter a password: ")
    if not password:
        print("password must be non empty")
    else:
        repassword = input("retype password:")
        if (password == repassword):
            #userdetails.append(password)
            sql = "INSERT INTO user (username, passwd, email) VALUES (%s,%s,%s)"
            mycursor.execute(sql, username, emailid, password)
            loop == 'false'
            break
        else:
            print("passwords do not match")

print(userdetails)
