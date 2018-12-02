import os
import sys
import getpass
import clioptions
print("Welcome to Cloud9 proceed to Login")

with open("userlogin.txt") as f:
    content = f.read().splitlines()
    array=content[0].split()


CorrectUsername = array[0]
CorrectPassword = array[1]

def userlogin():

    boolvar = 'true'
    while (boolvar == 'true'):
        user = input("Please enter your username:  ")
        if user == CorrectUsername:
            while True:
                pwd = getpass.getpass(prompt='enter your password:  ')

                if pwd == CorrectPassword:
                    print("Welcome!!!")
                    boolvar = 'false'
                    clioptions.options()
                    break
                else:
                    print
                    "The password you entered is incorrect."
            else:
                print("incorrect username")
    return
