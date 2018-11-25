import os
import sys

print("Welcome to Cloud9")

print("1. Login")
print("2. Register")

loop = 'true'
while (loop == 'true'):
    userinput = input(" Enter your choice: ")

    if (userinput == '1'):
        os.system('python login.py')
        loop = 'false'

    elif (userinput == '2'):
        os.system('python register.py')
        loop = 'false'

    else:
        print("invalid input ")
