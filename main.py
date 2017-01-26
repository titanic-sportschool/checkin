from Database.database import DatabaseClass
from timeit import default_timer as timer
import RPi.GPIO as GPIO
import hashlib
import threading

# TODO: IMPLEMENT NFC reader

# Constants
# TODO: Maybe ask the user for location (for demonstration purposes)
BLINK_TIME = 2
LOCATION = 1
LED_RED = 8
LED_GREEN = 7
SERVO_MOTOR = 25
SERVO_MOTOR_CLOSED = float(1) / 10.0 + 2.5
SERVO_MOTOR_OPEN = float(90) / 10.0 + 2.5


# GLOBALS
db = DatabaseClass()
user = None


def blink(pin):
    start = timer()
    end = timer()
    GPIO.output(pin, True) # Turn light on
    while end - start < BLINK_TIME:
        end = timer()

    GPIO.output(pin, False) # Turn light off


# Login check
def login_check():
    global db
    global user

    blink_on = True

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
                blink(LED_RED)

            print('\n')


# MAIN LOOP
def main():
    global db
    global user

    while True:
        # If the global variable has a value, we can assume the login was a success in the other thread
        if user:
            print('Login success')
            # TODO: Move to thread?
            blink(LED_GREEN)

            log = db.get_check_in_state(user['User_ID'])

            # Already checked in, so we check out
            if log and log['Is_checkin']:
                db.check_in_out(user['User_ID'], LOCATION, False)
                pwm.ChangeDutyCycle(SERVO_MOTOR_OPEN)
                print('{0} checks out!'.format(user['Email']))

            # Already checked out, so we check in
            else:
                db.check_in_out(user['User_ID'], LOCATION)
                pwm.ChangeDutyCycle(SERVO_MOTOR_CLOSED)
                print('{0} checks in!'.format(user['Email']))

            # Clear user to prevent multiple check_in's
            user = None

    # Close database connection
    db.close_connection()

    # GPIO cleanup
    GPIO.cleanup()

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)
# Turn of warnings to keep the console clean
GPIO.setwarnings(False)

# SETUP
GPIO.setup(LED_RED, GPIO.OUT, initial = False)
GPIO.setup(LED_GREEN, GPIO.OUT, initial = False)
GPIO.setup(SERVO_MOTOR, GPIO.OUT, initial = False)

pwm = GPIO.PWM(SERVO_MOTOR, 100)
pwm.start(5)

# Create thread for login check
login_thread = threading.Thread(target = login_check)
login_thread.daemon = True # thread dies when program ends
login_thread.start() # Start the thread

# START MAIN LOOP
main()

GPIO.cleanup()
# Close gate
pwm.ChangeDutyCycle(SERVO_MOTOR_CLOSED)
