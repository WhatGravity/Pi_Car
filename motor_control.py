import RPi.GPIO as GPIO
from config import *

# ───── Setup ─────
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_FWD, GPIO.OUT)
GPIO.setup(PWM_REV, GPIO.OUT)

# ───── Initialize PWM for forward and reverse motors ─────
pwm_fwd = GPIO.PWM(PWM_FWD, 100)
pwm_rev = GPIO.PWM(PWM_REV, 100)
pwm_fwd.start(0)
pwm_rev.start(0)

# ───── Motor controlling ─────
def forward(dc):
    pwm_rev.ChangeDutyCycle(0)
    pwm_fwd.ChangeDutyCycle(dc)

def reverse(dc):
    pwm_fwd.ChangeDutyCycle(0)
    pwm_rev.ChangeDutyCycle(dc)

def stop():
    pwm_fwd.ChangeDutyCycle(0)
    pwm_rev.ChangeDutyCycle(0)

def cleanup():
    stop()
    pwm_fwd.stop()
    pwm_rev.stop()
