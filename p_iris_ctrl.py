import time
import sys
from pathlib import Path

import RPi.GPIO as GPIO


# pin definitions
coil_a_plus = 2
coil_a_minus = 3
coil_b_plus = 4
coil_b_minus = 14


def p_iris_ctrl(target_aperture):
    # GPIO setup
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(coil_a_plus, GPIO.OUT)
    GPIO.setup(coil_a_minus, GPIO.OUT)
    GPIO.setup(coil_b_plus, GPIO.OUT)
    GPIO.setup(coil_b_minus, GPIO.OUT)

    try:
        if target_aperture > 92:
            target_aperture = 92
        if target_aperture < 0:
            target_aperture = 0
        home = str(Path.home())
        file = open(home + "/aa-cam/iris_state.txt", "r")
        current = file.readline()
        file.close()
        if not current.isdecimal():
            print("Invalid state in iris_state.txt")
            exit()
        current_count = int(current)

        print("Moving to target aperture...")
        while current_count != target_aperture:
            if current_count < target_aperture:
                current_count += 1
            if current_count > target_aperture:
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

            else:
                GPIO.output(coil_a_plus, GPIO.LOW)
                GPIO.output(coil_a_minus, GPIO.HIGH)
                GPIO.output(coil_b_plus, GPIO.HIGH)
                GPIO.output(coil_b_minus, GPIO.LOW)

            time.sleep(0.01)

        file = open(home + "/aa-cam/iris_state.txt", "w")
        file.write(str(current_count))
        file.close()
        print("Target reached")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    # variable declarations
    if not len(sys.argv) - 1 == 1:
        print("Must pass exactly 1 argument to p_iris_ctrl")
        exit()

    target = sys.argv[1]
    if not target.isdecimal():
        print("Target must be a number between 0 and 100")
        exit()
    target_count = int(target)
    p_iris_ctrl(target_count)
