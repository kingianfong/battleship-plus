import pandas as pd
import hashlib
import re
import os.path
from time import time, sleep

from settings import user_data_file
file_name = user_data_file()

def hash_info(info):
    """ Returns hashe of input string. """
    return hashlib.sha256(info.encode()).hexdigest()
    
def username_exists(username):
    """ Returns True if username is in existing username list, returns False otherwise. """
    file_exists = os.path.isfile(file_name)
    if file_exists:
        existing_usernames = pd.read_csv(file_name).username.tolist()
        return username in existing_usernames  #returns true if username exists
    else:
        return False
    
def get_new_username():
    """ Returns new username using user input. """    
    new_name = input("Username: ")
    while True:
        
        if username_exists(new_name): # username is taken
            print("Username is taken, please choose another username")
            new_name = input("Username: ")
            continue
        
        elif new_name.isalnum() == False:  # username is not alphanumeric
            print("Please enter letters and numbers only")
            new_name = input("Username: ")
            continue
        
        else:
            break
        
    return new_name

def password_valid(new_pw, new_name):
    """ Returns True if username and password meets all criteria, returns False otherwise. """
    print()  # line break for readability
    if new_name.lower() in new_pw.lower():
        print("Password should not contain username '{}'.".format(new_name))
        return False
    
    elif len(new_pw) < 8:
        print("Password must be longer than 8 characters.")
        return False
    
    elif not re.search("[a-z]",new_pw):
        print("Password must include at least one lowercase letter.")
        return False
    
    elif not re.search("[A-Z]",new_pw):
        print("Password must include at least one uppercase letter.")
        return False
    
    elif not re.search("[0-9]",new_pw):
        print("Password must include at least one number.")
        return False
    
    elif not re.search("[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]",new_pw):
        print("Password must contain at least one special character.")
        return False
    
    else:
        print("Password accepted")
        return True

def get_new_pw(new_name):
    """ Returns new password using user input. """
    print("""\
Please enter a password.

It should be at least 8 characters long and contain the following:
\t1. at least one lowercase letter
\t2. at least one uppercase letter
\t3. at least one number and
\t4. at least one special character

Additionally, it should not contain your username
""")

    while True:
        new_pw = input("Password: ")
        while not password_valid(new_pw, new_name):
            # checks if password satisfies criteria
            new_pw = input("Password: ")
            
        reenter_pw = input("Please re-enter password: ")  # ensures password is entered correctly
        if reenter_pw == new_pw:  # if password entered correctly, returns new password
            return new_pw
        else:
            tries = 3
            while tries > 0:
                # prints error message and gets reentered password if no match
                print("\nPasswords do not match")
                print("Attempts left: {}".format(tries))
                tries -= 1
                reenter_pw = input("Please re-enter password: ")
                
                if reenter_pw == new_pw:  # if re-entered password matches, returns new password
                    return new_pw
                
            else:  # when out of tries, takes new password again
                print("\nNo more attempts")
                print("Please enter a new password\n")
                continue

def get_new_dob():
    """ Returns date of birth in the form ddmmyyyy using user input. """
    error_msg = "Invalid. Please use ddmmyyyy format\n\te.g.: 01121990 for 01 Dec 1990"
    while True:
        dob = input("Please enter date of birth for account recovery (ddmmyyyy): ")
        if len(dob) != 8:
            # checks if there are enough characters
            print(error_msg)
        else:
            try:
                # attempts to convert slices into integers
                day = int(dob[0:2])
                month = int(dob[2:4])
                year = int(dob[4:8])
            except:
                print(error_msg)
                continue
            
            if 0 < day <= 31 and 0 < month <= 12 and year < 2020:
                # checks that the day, month, and year contain valid numbers
                return dob
            else:
                print("Please enter a valid date.")

def create_new_profile():
    """ Returns new username and creates a new profile. """
    print("\nCreating new profile")
    
    new_name = get_new_username()
    new_pw = get_new_pw(new_name)
    new_dob = get_new_dob()
    
    pw_hash = hash_info(new_pw)  # hashes password
    dob_hash = hash_info(new_dob)  # hashes date of birth
    attempts = 0
    last_activity = time()  # saves current time
    user_info_list = [new_name, attempts, last_activity, pw_hash, dob_hash]
    
    columns = ["username", "attempts", "last_activity", "pw_hash", "dob_hash"]
        
    user_info_df = pd.DataFrame([user_info_list], columns = columns).set_index(["username"], drop=True)  # creates a dataframe for single user

    file_exists = os.path.isfile(file_name)  # checks if file exists    
    if file_exists:
        # checks if exissting file exists
        df = pd.read_csv(file_name, index_col = 0)  # opens the user data csv file as a dataframe
        df = df.append(user_info_df)  # appends the new user info to existing user info
        df.to_csv(file_name)  # overwrites csv file with new file
        
    else:
        user_info_df.to_csv(file_name)  # saves user dataframe to new csv file
        
    return new_name
        
def retry():
    """ Returns True if user wants to retry, returns False otherwise. """
    while True:
        retry = input("Retry? 'y' or 'n' : ")
        if retry.lower() == 'y':
            return True
        elif retry.lower() == 'n':
            return False
        else:
            print("\nPlease enter 'y' or 'n' only")
    
def log_in():
    """ Returns username of active user. """
    print("\nLogging in")

    username = input("Username: ")
    while not username_exists(username):
        print("\nUsername does not exist")
        if retry():
            username = input("\nUsername: ")
        else:
            return select_user()
            
    login_successful = False
    while not login_successful:
        df = pd.read_csv(file_name, index_col = 0)  # reads csv file
        [attempts, last, pw_hash, dob_hash] = df.loc[username].tolist()  # gets user's data in the csv file 
        df.at[username, "attempts"] = attempts + 1  # increases attempt count
        df.at[username, "last_activity"] = time()  # updates last activity

        remaning_attempts = 3 - attempts        
        if remaning_attempts >= 0:
            # account is not locked, will take password
            pw_input_hash = hash_info(input("Password: "))
            
            if pw_input_hash != pw_hash:
                # password does not match
                print("\nPassword does not match")
                print("Attempts left: {}".format(remaning_attempts))
            else:
                login_successful = True
            
        else:
            # account is locked, will take date of birth only
            print("\nAccount is locked")
            print("Please enter date of birth to reset password")
            if time() - last < 2:  # less than 2 seconds from last attempt
                sleep(2 - time() + last)
                
            dob_input_hash = hash_info(input("Date of Birth (ddmmyyyy): "))
            if dob_input_hash != dob_hash:
                # date of birth does not match
                print("\nDate of birth does not match")
                
            else:
                # date of birth matches
                print("\nDate of birth correct, resetting password\n")
                new_pw_hash = hash_info(get_new_pw(username))
                df.at[username, "pw_hash"] = new_pw_hash  # saves new password hash
                print("\nPassword successfully reset")
                login_successful = True
        df.to_csv(file_name)
        
    else:
        df.at[username, "attempts"] = 0  # resets attempt count
        df.to_csv(file_name)
        return username

def select_user():
    """ Returns username of active user by allowing profile creation or login. """
    file_exists = os.path.isfile(file_name)  # checks if file exists
    if not file_exists:
        # if file does not exist, create new profile
        return create_new_profile()
    
    else:
        # if file exists, give option to login or create new profile
        selection = input("\n1. Log in\n2. Create new profile\n\nSelection: ")
        while selection != "1" and selection != "2":
            print("Please enter '1' or '2' only\n")
            selection = input("1. Log in\n2. Create new profile\n\nSelection: ")
            
        if selection == "1":
            return log_in()
        
        elif selection == "2":
            return create_new_profile()

if __name__ == "__main__":
    username = select_user()
    print(username)
