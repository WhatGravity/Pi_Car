import pigpio
from config import *

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio-Daemon nicht verbunden. Starte mit: sudo pigpiod")

def set_steering_angle(angle):
    angle = max(MAX_LEFT, min(MAX_RIGHT, angle))
    
    if angle == 0:
        pi.set_servo_pulsewidth(SERVO_STEERING_PIN, SERVO_MID)
    else:
        target_deg = SERVO_MID_DEG + angle
        pulsewidth = 1000 + (target_deg / 180.0) * 1000
        pi.set_servo_pulsewidth(SERVO_STEERING_PIN, pulsewidth)

def cleanup():
    pi.set_servo_pulsewidth(SERVO_STEERING_PIN, 0)
    pi.stop()
