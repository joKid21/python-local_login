import json #this is the file type that we store users and passwords in
import time #this sets wait time so user can read msg before they disappear
import getpass #this to hide password when user is authenticating
import hashlib #this encrypts the password
import random #This is for salting the password hashes
import string #For allocating letter with ascii characters

def cls():  #this defining clear screen command so it can be called from anywhere
   print('\033c')
valid_login={}  #this is where we store the dictionary of users and passwords
user_salts={} #this is where we store the dictionary of salted users and passwords
old_passpassword={} #this is where we store the old passwords of users so they dont use old passwords
try:                 #check if the valid login file exists 
    with open('validlogin.json') as f:
        valid_login = json.load(f)
except:             #if it doesn't exist it will be created
    with open('validlogin.json', 'w') as f:
        json.dump(valid_login, f)
try:                 #check if the valid login file exists 
    with open('usersalts.json') as R:
        user_salts = json.load(R)
except:             #if it doesn't exist it will be created
    with open('usersalts.json', 'w') as R:
        json.dump(user_salts, R)
try:                 #check if the valid login file exists 
    with open('oldpass.json') as R:
        old_passpassword = json.load(R)
except:             #if it doesn't exist it will be created
    with open('oldpass.json', 'w') as R:
        json.dump(old_passpassword, R)

def Login(username, password): #this is where we check the dictionary if the username and passwords are correct
    for k, v in valid_login.items():
        if username in k:
            if username == k and password == v:
                global Global_Username
                Global_Username = username
                cls()
                print(f"Logged in as: {username}!")
                time.sleep(2)
                cls()
                return True
            else: 
                (cls)
                print ("Username and password does not match")
                time.sleep(5)
                (cls)
                return False
        else:
            cls()
            print ("Username Does Not Exist")
            time.sleep(5)
            cls()

def Create_SaltedEncrypt(new_user,new_password):
    Random_integer = str(random.randint(1000, 9999))
    Random_Letter = random.choice(string.ascii_letters)
    Random_Letter_2 = random.choice(string.ascii_letters)
    Random_Character=(f"{Random_Letter_2}{Random_integer}{Random_Letter}")
    user_salts[new_user]=Random_Character
    with open('usersalts.json', 'w') as R: #and then the dictionary is written to the json file
        json.dump(user_salts, R)
    Random_Character=(f"{Random_integer}{Random_Letter}")
    new_password=(f"{new_password}{Random_Character}")
    return

def SaltedEncrypt(username, password):
        for k, v in user_salts.items():
            if username == k:
                password=(f"{password}{v}")
                return

def Pass_quirements(password):
    special_characters = ("!@#$%^&*()_-+=<>?/[]{}|")
    length = len(password)
    if any(r.isupper() for r in password) and any(r.isdigit() for r in password) and any(r in special_characters for r in password) and length >= 8:
            return True
    else:
        print("password must contain at least one uppercase, number and a special character")
        print('and longer than 8 character')
        time.sleep(5)
        cls()
        return False
    return

def CreateUser():
    Username_not_taken=False
    while not Username_not_taken: #this loop is to check if username is already taken
        cls()
        new_user=input("Please enter username: ")
        if new_user not in valid_login:
            Username_not_taken=True
            global Global_Username
            Global_Username=new_user
            Matching_password=False
            while not Matching_password:         #this loop check if both passwords entered are the same
                new_pass=getpass.getpass("Please enter password: ")
                if Pass_quirements(new_pass):
                    confirm_pass=getpass.getpass("Please re-entern password: ")
                    if new_pass==confirm_pass:
                        Create_SaltedEncrypt(new_user,new_pass) #encrypt the password and save it
                        change_pass_bytes = new_pass.encode('utf-8')
                        encrypted_change_pass=hashlib.sha256(change_pass_bytes).hexdigest() #encrypt password and save
                        valid_login[new_user]=encrypted_change_pass     #if they are they are writen to the dictionary
                        with open('validlogin.json', 'w') as f:#and then the dictionary is written to the json file  
                            json.dump(valid_login, f)
                        old_passpassword[new_user]=encrypted_change_pass
                        with open('oldpass.json', 'w') as f:    #and then the dictionary is written to the json file
                            json.dump(old_passpassword, f)
                            Matching_password=True
                            return True
                    else:
                        cls()
                        print ("The password are not the same, please try again")
                        time.sleep(2)
                        cls()
                        print ("Username: ",new_user)
        else:
            cls()
            print ("Username is already in use")
            time.sleep(5)


def LoginUser(): #defining login so it can be called back when changing passwords etc
        loged_in=False
        while not loged_in:
            cls()
            username=input('Please enter your username: ')
            cls()
            for k, v in user_salts.items():
                if username in k:
                    print("Loging in as",username)
                    password= getpass.getpass('Please enter your password: ')
                    SaltedEncrypt(username, password)
                    change_pass_bytes=password.encode('utf-8')
                    encrypted_change_pass=hashlib.sha256(change_pass_bytes).hexdigest() #encrypt password and save
                    if (Login(username, encrypted_change_pass)):
                        loged_in=True
                        return True
                else: 
                    cls()
                    print('Username Does not exist')
                    time.sleep(2)
                    cls()

def ChangingPassword():
    Current_password=getpass.getpass('please enter your current password: ')
    SaltedEncrypt(Global_Username, Current_password)
    Encrypted_Current_pass_bytes=Current_password.encode('utf-8')
    Encryped_pass_Check=hashlib.sha256(Encrypted_Current_pass_bytes).hexdigest()
    if Login(Global_Username, Encryped_pass_Check):
        change_password=getpass.getpass('please enter your new password: ')
        SaltedEncrypt(Global_Username, change_password)
        password_check_bytes=change_password.encode('utf-8')
        old_password= hashlib.sha256(password_check_bytes).hexdigest() #encrypt password
        if old_password != Encryped_pass_Check:
            old_password[Global_Username]+=Encryped_pass_Check
            with open('oldpass.json', 'w') as f:    #and then the dictionary is written to the json file
                json.dump(old_password, f)
            if Pass_quirements(change_password):
                check_pass=getpass.getpass('please re-enter your new password: ')
                if change_password == check_pass:
                    Create_SaltedEncrypt(Global_Username, change_password)
                    change_pass_bytes = change_password.encode('utf-8')
                    encrypted_change_pass = hashlib.sha256(change_pass_bytes).hexdigest() #encrypt password and save
                    valid_login[Global_Username]=encrypted_change_pass
                    with open('validlogin.json', 'w') as f:    #and then the dictionary is written to the json file
                        json.dump(valid_login, f)
                    return 
        else: 
            cls()
            print ('Password has been user before')
            time.sleep(3)
            cls()
            return False
    else:
        print ("password is incorrect")
        return


def ReturnUsername(Current_User):
    Current_User=Global_Username
    return Current_User

def Snoopy():
    print("""
           _
          (:)_
        ,'    `.
        :        :
        |        |              ___
        |       /|    ______   // _\\
        ; -  _,' :  ,'      `. \\\\  -\\
        /          \\/          \\\\ \\\\:  
       (            :  ------.  `-'    |
    ____\\___    ____|______   \\______|_______
            |::|           '--`           SSt
            |::|
            |::|
            |::|
            |::;
            `:/
""")

""""
    print("Congratulations, you have successfully logged in as:", Global_Username)

    print("error getting", Global_Username)"""

if __name__ == '__main__':
    cls()
    print("This is a Module That can be used to login and create users securely")
    print("heres a list of all functions that can be used")
    print("(Loginusers, CreateUser and ChangingPassword)")