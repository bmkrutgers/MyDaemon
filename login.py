import os
import sys
import getpass
import clioptions
print("Welcome to Cloud9 proceed to Login")

mydb = mysql.connector.connect(
  host="cloudnine.c87lmy1ftwtu.us-east-2.rds.amazonaws.com",
  user="modi1234",
  passwd="Was160497",
  database="CloudNine"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT username FROM user")

myresult = mycursor.fetchall()

with open("userlogin.txt") as f:
    content = f.read().splitlines()
    array=content[0].split()


CorrectUsername = array[0]
CorrectPassword = array[1]

def userlogin():
    boolvar = 'true'
    while (boolvar == 'true'):
        user = input("Please enter your username:  ")
        for y in myresult:
		    x = ''.join(y)
		    if(x==user):
                while True:
                        pwd = getpass.getpass(prompt='enter your password:  ')
                        mycursor.execute("SELECT passwd FROM user")
  			            myresult = mycursor.fetchall()
            		    for y in myresult:
				            x = ''.join(y)
  				            if(x==pwd):
                                print("Welcome!!!")
                                boolvar = 'false'
                                clioptions.options()
                                break
                            else:
                                print("The password you entered is incorrect.")
            else:
                print("incorrect username")
    return
