from Database.database import DatabaseClass
import hashlib

# Constants
LOCATION = 1;

db = DatabaseClass()

while True:
    email = input("Name: ")
    pw = input("PW: ")

    # TODO: Replace login with NFC reader
    # Sha1 encryption for password
    sha1 = hashlib.sha1()
    sha1.update(pw.encode(encoding='UTF-8'))
    # Check if there is a customer with given login
    user = db.get_customer(email, sha1.hexdigest())

    # if there is one, login is success
    if user:
        log = db.get_check_in_state(user['User_ID'])

        # Already checked in, so we check out
        if log and log['Is_checkin']:
            db.check_in_out(user['User_ID'], LOCATION, False)
            print('Bye')

        # Already checked out, so we check in
        else:
            db.check_in_out(user['User_ID'], LOCATION)
            print('Welcome')

    # TODO: Login should be moved to a different thread and then we need to move login failed too
    # Login failed
    else:
        print('Log in failed')

    print("\n")
