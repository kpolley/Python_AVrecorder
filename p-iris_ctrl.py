import RPi.GPIO as GPIO
import time
import sys

# pin definitions
coil_a_plus = 2
coil_a_minus = 3
coil_b_plus = 4
coil_b_minus = 14

# GPIO setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(coil_a_plus, GPIO.OUT)
GPIO.setup(coil_a_minus, GPIO.OUT)
GPIO.setup(coil_b_plus, GPIO.OUT)
GPIO.setup(coil_b_minus, GPIO.OUT)

# variable declarations
try:
    if not len(sys.argv)-1 == 1:
        print("Must pass exactly 1 argument to p-iris_ctrl")
        exit()
        
    target = sys.argv[1]
    if not target.isdecimal():
        print("Target must be a number between 0 and 100")
        exit()
    target_count = int(target)
    if target_count > 92:
        target_count = 92
    if target_count < 0:
        target_count = 0
        
    file = open("iris_state.txt", "r")
    current = file.readline()
    file.close()
    if not current.isdecimal():
        print("Invalid state in iris_state.txt")
        exit()
    current_count = int(current)
    
    print("Moving to target...")
    while current_count != target_count:
        if current_count < target_count:
            current_count += 1
        if current_count > target_count:
            current_count -= 1
        count_mod = current_count % 4

        if count_mod == 0:
            GPIO.output(coil_a_plus, GPIO.LOW)
            GPIO.output(coil_a_minus, GPIO.HIGH)
            GPIO.output(coil_b_plus, GPIO.LOW)
            GPIO.output(coil_b_minus, GPIO.HIGH)

        elif count_mod == 1:
            GPIO.output(coil_a_plus, GPIO.HIGH)
            GPIO.output(coil_a_minus, GPIO.LOW)
            GPIO.output(coil_b_plus, GPIO.LOW)
            GPIO.output(coil_b_minus, GPIO.HIGH)

        elif count_mod == 2:
            GPIO.output(coil_a_plus, GPIO.HIGH)
            GPIO.output(coil_a_minus, GPIO.LOW)
            GPIO.output(coil_b_plus, GPIO.HIGH)
            GPIO.output(coil_b_minus, GPIO.LOW)

        else :
            GPIO.output(coil_a_plus, GPIO.LOW)
            GPIO.output(coil_a_minus, GPIO.HIGH)
            GPIO.output(coil_b_plus, GPIO.HIGH)
            GPIO.output(coil_b_minus, GPIO.LOW)

        time.sleep(0.01)
    
    file = open("iris_state.txt", "w")
    file.write(str(current_count))
    file.close()
    print("Target reached")

finally:
    GPIO.cleanup()
