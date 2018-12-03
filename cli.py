import os
import sys
import register
import login
print("Welcome to Cloud9")

print("1. Login")
print("2. Register")

loop = 'true'
while (loop == 'true'):
    userinput = input(" Enter your choice: ")

    if (userinput == '1'):
        login.userlogin()
        loop = 'false'

    elif (userinput == '2'):
        register.registration()
        loop = 'false'

    else:
        print("invalid input ")
