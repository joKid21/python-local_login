import time
from Login import CreateUser
from Login import LoginUser
from Login import ChangingPassword
from Login import ReturnUsername
from Login import Snoopy

def wait(x):
    time.sleep(x)

def cls():  #this defining clear screen command so it can be called from anywhere
   print('\033c')

cls()
try:    #this is so the user doesnt get overwhemed if there's an error
    #main program //login
    questions=True
    signed_Up=False
    loged_in=False
    while questions: 
        is_signed_up= input("are you signed up? yes or no: ")
        if is_signed_up == 'no':
            signed_Up = False
            questions=False
        elif is_signed_up == 'yes':
            signed_Up = True
            questions=False
        else:
            print("Invalid input")  #if user type anything other then yes or no
            wait(2)
            cls()
    while not loged_in: #this loop is for the login if user is not logged in it will keep looping until user is logged in
#        issignedup= input("are you signed up? yes or no: ")
        if not signed_Up:      #if user not signed up call back Createuser function
            if CreateUser():
                print("User has been created")
                loged_in=True
            else:
                print("User has not been created")
                wait(2)
                cls()
        elif signed_Up:   #if user is signed up call back login function
            cls()
            if LoginUser():
                loged_in=True
    #this is outside the loop it comes after the break's up top

    Snoopy()
    print("Congratulations, you have successfully logged in as:", ReturnUsername(CreateUser))
    Password_Change=input("Do you want to change your password? yes or no: ")

    while Password_Change == "yes":
        if ChangingPassword():
            print("You have successfully changed your password")
            break
        else:
            print("Password has not been changed")
    else:
        cls()
        Snoopy()
        print("Thanks for trying out my program.")
        wait(5)

except Exception:
    print("Sorry, coder is still beginner")