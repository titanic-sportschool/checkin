from Database.database import DatabaseClass
import hashlib
import threading

# TODO: IMPLEMENT NFC reader

# Constants
# TODO: Maybe ask the user for location (for demonstration purposes)
LOCATION = 1

# GLOBALS
db = DatabaseClass()
user = None


# Login check
def login_check():
    global db
    global user

    while True:
        # If there is no login
        if not user:
            email = input('Name: ')
            pw = input('PW: ')

            # Sha1 encryption for password
            sha1 = hashlib.sha1()
            sha1.update(pw.encode(encoding='UTF-8'))

            # Check if there is a customer with given login
            user = db.get_customer(email, sha1.hexdigest())

            # Login failed
            if not user:
                print('Log in failed')

            print('\n')


# MAIN LOOP
def main():
    global db
    global user

    while True:
        # If the global variable has a value, we can assume the login was a success in the other thread
        if user:
            print('Login success')
            log = db.get_check_in_state(user['User_ID'])

            # Already checked in, so we check out
            if log and log['Is_checkin']:
                db.check_in_out(user['User_ID'], LOCATION, False)
                print('{0} checks out!'.format(user['Email']))

            # Already checked out, so we check in
            else:
                db.check_in_out(user['User_ID'], LOCATION)
                print('{0} checks in!'.format(user['Email']))

            # Clear user to prevent multiple check_in's
            user = None

    # Close database connection
    db.close_connection()


# Create thread for login check
login_thread = threading.Thread(target = login_check)
login_thread.daemon = True # thread dies when program ends
login_thread.start() # Start the thread

# START MAIN LOOP
main()
