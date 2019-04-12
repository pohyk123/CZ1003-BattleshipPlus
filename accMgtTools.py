# CZ1003 Battleship+ [Group Project]
# Contains various account management tools to handle login, account creation & unlocking

import sys

def login(loginInfo):
    usr, pwd, tries = loginInfo['usr'], loginInfo['pwd'], loginInfo['tries']
    filecheck()
    with open("./database/locked.txt","r+") as locked:
        locked_acc = locked.readlines()
        for user in locked_acc:
            if user.strip() == usr.strip():
                return 0  # acc is locked

    with open("./database/data.txt", "r+") as f, open("./database/locked.txt", "a+") as locked:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            if lines[i].strip()==usr.strip():
                if lines[i+1].strip() == pwd.strip():
                    return 1  # login success
                elif tries >=2 :
                    locked.write(usr + "\n")
                    return 0  # max login exceeded
                else:
                    return 2  # Wrong pwd

        return -1  # username not found


def unlockAcc(unlockInfo):
    usr, date = unlockInfo['usr'], unlockInfo['date']
    is_found = False
    delete = False
    with open("./database/data.txt", "r+") as f, open("./database/locked.txt", "r+") as locked:
        lines = f.readlines()
        locked_acc = locked.readlines()
        for user in locked_acc:
            if user.strip() == usr.strip():
                is_found = True
        if is_found:
            for i in range(0, len(lines), 3):
                if lines[i].strip() == usr.strip():
                    if lines[i + 2].strip() == date.strip():
                        delete = True
        else:
            return -1  # username not found

        print(locked_acc)

        if delete:
            locked.seek(0)
            locked.truncate(0) # erase existing contents of locked file
            for i in range(len(locked_acc)):
                if i != locked_acc.index(usr+'\n'):
                    locked.write(locked_acc[i])
            return 1  # delete success
        else:
            return 0  # wrong date


def register(regInfo):
    usr, pwd, date = regInfo['usr'],regInfo['pwd'],regInfo['date']
    filecheck()

    # Check valid pw
    if strongpw(pwd,usr) == -1:
        return 0

    # Check valid DoB
    if(DoB(date) == -1):
        return -1

    # Check if user exists
    with open("./database/data.txt", "r+") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            if lines[i] == (usr+"\n"):
                return 2  # username already exists

    with open("./database/data.txt", "a+") as f:
        f.write(usr + "\n")
        f.write(pwd + "\n")
        f.write(date + "\n")
        return 1 #register successful

def filecheck():
    try:
        fh = open('./database/data.txt','r')
        fh2 = open('./database/locked.txt','r')
    except FileNotFoundError:
        fh = open("./database/data.txt", "w+")
        fh2= open("./database/locked.txt","w+")


def strongpw (pwd,user):
    upCase = False  # indicate if pw has at least one upper case character, etc
    lowCase = False
    digit = False
    spcharlist = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "_", "=", \
                  ",","/","?",".",";",":","'","|","]","[","{","}","~","`"]
    usern= False
    special = False

    LENGTH=8
    for char in pwd:  # iterate on each character of the pw
        if char.isupper():
            upCase = True
        if char.islower():
            lowCase = True
        if char.isdigit():
            digit = True
        if user not in pwd:
            usern = True
        for i in spcharlist:
            if i in pwd:
                special = True

    length =len(pwd)
    strong = upCase and lowCase and usern and digit and special and length > LENGTH
    if strong:
        return 1
    else:
        return -1 #weak password

def DoB(birth):
    x= birth.count('/')
    if x!=2:
        return -1 # invalid dob format

    day, month, year = birth.split('/')
    if(not (day.isdigit() and month.isdigit() and year.isdigit())):
        return -1 # invalid dob format

    if(int(day) > 31 or int(day) < 1 or int(month) > 12 or int(month) < 1):
        return -1 # invalid dob format

    return 1 # valid dob

def regis():
    while True:
        username = input("Please input a new username: ")
        pw = input("Please input your password: ")
        pwsuper = strongpw(pw,username)
        birthsuper = DoB()
        x = register(username, pwsuper, birthsuper)

        if x == 1:
            print("Register successful!")
            break
        else:
            print("Username already exist!\n")

if __name__ == "main":
    regis()
