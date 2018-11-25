import os
import sys
import getpass
import mysql.connector

print("Welcome to Cloud9 proceed to Login")

mydb = mysql.connector.connect(
  host="cloudnine.c87lmy1ftwtu.us-east-2.rds.amazonaws.com",
  user="modi1234",
  passwd="Was160497",
  database="CloudNine"
)

mycursor = mydb.cursor()

with open("userlogin.txt") as f:
    content = f.read().splitlines()
    array=content[0].split()


CorrectUsername = array[0]
CorrectPassword = array[1]

mycursor.execute("SELECT username FROM user")

myresult = mycursor.fetchall()

boolvar = 'true'
while (boolvar == 'true'):
    user = input("Pleaae enter your username:  ")
    for x in myresult:
		if(x==user):
        	while True:
        		mycursor.execute("SELECT passwd FROM user")
            	pwd = p = getpass.getpass(prompt='enter your password:  ')

            	mycursor.execute("SELECT passwd FROM user")
  				myresult = mycursor.fetchall()
            	for x in myresult:
  					if(x==pwd):
                		print("Welcome!!!")
                		boolvar = 'false'
                		os.system("python options.py")
                		break
            		else:
                		print
                		"The password you entered is incorrect."
    	else:
        print("incorrect username")
