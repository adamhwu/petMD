import RPi.GPIO as GPIO
import time

# Define your motor driver pins (BCM mode)
LEFT_EN = 18     # ENA → PWM pin for left motor
LEFT_IN1 = 23
LEFT_IN2 = 24

RIGHT_EN = 13    # ENB → PWM pin for right motor
RIGHT_IN1 = 17
RIGHT_IN2 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup motor pins
motor_pins = [LEFT_EN, LEFT_IN1, LEFT_IN2, RIGHT_EN, RIGHT_IN1, RIGHT_IN2]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Create PWM channels
left_pwm = GPIO.PWM(LEFT_EN, 1000)
right_pwm = GPIO.PWM(RIGHT_EN, 1000)
left_pwm.start(0)
right_pwm.start(0)

def move(left_speed, right_speed):
    # Direction control
    GPIO.output(LEFT_IN1, left_speed >= 0)
    GPIO.output(LEFT_IN2, left_speed < 0)
    GPIO.output(RIGHT_IN1, right_speed >= 0)
    GPIO.output(RIGHT_IN2, right_speed < 0)

    # Speed control (absolute value, clamped 0–100)
    left_pwm.ChangeDutyCycle(min(abs(left_speed), 100))
    right_pwm.ChangeDutyCycle(min(abs(right_speed), 100))

def stop():
    left_pwm.ChangeDutyCycle(0)
    right_pwm.ChangeDutyCycle(0)

def cleanup():
    stop()
    GPIO.cleanup()
