from Database.database import DatabaseClass
from timeit import default_timer as timer
import RPi.GPIO as GPIO
import hashlib
import threading

# TODO: IMPLEMENT NFC reader

# Constants
BLINK_TIME = 2
LED_RED = 8
LED_GREEN = 7
SERVO_MOTOR = 25
SERVO_MOTOR_TIME = 2
SERVO_MOTOR_CLOSED = float(90) / 10.0 + 2.5
SERVO_MOTOR_OPEN_CLOCK_WISE = float(0) / 10.0 + 2.5
SERVO_MOTOR_OPEN_COUNTER_CLOCK_WISE = float(180) / 10.0 + 2.5


# GLOBALS
db = DatabaseClass()
user = None
servo_run = False
servo_clockwise = False # True = Clock wise, False = Counter clock wise
blink_red = False
blink_green = False


# Led thread
def led():
    global blink_red
    global blink_green

    while True:
        if blink_red or blink_green:
            start = timer()
            end = timer()
            GPIO.output(LED_RED, blink_red) # Turn light on
            GPIO.output(LED_GREEN, blink_green) # Turn light on
            while end - start < BLINK_TIME:
                end = timer()

            GPIO.output(LED_RED, False) # Turn light off
            GPIO.output(LED_GREEN, False) # Turn light off
            blink_red = False
            blink_green = False


# Servo thread
def servo():
    global servo_run

    while True:
        if servo_run:
            start = timer()
            end = timer()
            pwm.ChangeDutyCycle(SERVO_MOTOR_OPEN_CLOCK_WISE if servo_clockwise else SERVO_MOTOR_OPEN_COUNTER_CLOCK_WISE)
            while end - start < SERVO_MOTOR_TIME:
                end = timer()
            pwm.ChangeDutyCycle(SERVO_MOTOR_CLOSED)
            servo_run = False


# Login check
def login_check():
    global db
    global user
    global blink_red

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
                blink_red = True

            print('\n')


# MAIN LOOP
def main():
    global db
    global user
    global servo_run
    global servo_clockwise
    global blink_green

    # SELECT LOCATION
    location_selected = False
    locations = db.get_locations()

    print('Select a location: ')
    for i in locations:
        print(i['ID'], '-', i['name'])

    while not location_selected:
        location = int(input('Location ID: '))
        for i in locations:
            if location == i['ID']:
                location_selected = True
                break
    print('\n')


    # START THREADS

    # Create thread for login check
    login_thread = threading.Thread(target = login_check)
    login_thread.daemon = True # thread dies when program ends
    login_thread.start() # Start the thread

    # Create thread for servo motor
    servo_thread = threading.Thread(target = servo)
    servo_thread.daemon = True # thread dies when program ends
    servo_thread.start() # Start the thread

    # Create thread for LED's motor
    led_thread = threading.Thread(target = led)
    led_thread.daemon = True # thread dies when program ends
    led_thread.start() # Start the thread

    while True:
        # If the global variable has a value, we can assume the login was a success in the other thread
        if user:
            print('Login success')
            blink_green = True

            log = db.get_check_in_state(user['User_ID'])

            # Already checked in, so we check out
            if log and log['Is_checkin']:
                db.check_in_out(user['User_ID'], location, False)
                # Open gate clockwise
                servo_clockwise = True
                servo_run = True
                print('{0} checks out!'.format(user['Email']))

            # Already checked out, so we check in
            else:
                db.check_in_out(user['User_ID'], location)
                # Open gate counter-clockwise
                servo_clockwise = False
                servo_run = True
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
pwm.start(SERVO_MOTOR_CLOSED)

# pwm.ChangeDutyCycle(SERVO_MOTOR_CLOSED) # Start servo in closed state

try:
    # START MAIN LOOP
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    # Close gate
    pwm.ChangeDutyCycle(SERVO_MOTOR_CLOSED)
    print('Program exit \n')
