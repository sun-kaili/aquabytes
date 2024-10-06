import RPi.GPIO as GPIO
import time
from aquarium_controller import relay_control

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set up the GPIO pin for the servo
servo_pin = 16
GPIO.setup(servo_pin, GPIO.OUT)
# Set the PWM signal on the pin
pwm = GPIO.PWM(servo_pin, 35)  # 50Hz for the servo
pwm.start(0)

def set_servo_angle(angle):
    # Calculate the duty cycle for the given angle
    duty = 2 + (angle / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(2)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def turn_on_servo(angle, return_angle, status, times):
    """
    Controls the servo to turn on a specified number of times.
    
    :param angle: The angle for feeding.
    :param return_angle: The angle for resting the servo.
    :param status: 'on' to activate the servo, 'off' to deactivate.
    :param times: The number of times to activate the servo.
    """
    
    if status == "on":
        for _ in range(times):
            set_servo_angle(angle)  # Move servo to feeding position
            # Add delay if needed for servo to stay in this position (e.g., time.sleep(seconds))
            set_servo_angle(return_angle)  # Move servo back to rest position
            # Add a delay here if needed between repetitions
    else:
        relay_control.feeder_off()
        pwm.stop()




