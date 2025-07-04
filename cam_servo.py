import pigpio
from config import *

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio-Daemon nicht verbunden. Starte mit: sudo pigpiod")

def set_servo_cam_angle_x(angle_x):
    angle_x = max(CAM_MIN, min(CAM_MAX, angle_x))
    pulse_x = int(SERVO_MID_PWM + (angle_x / SERVO_MID_DEG) * 500)   
    pi.set_servo_pulsewidth(SERVO_PIN_X, pulse_x)
        
        
def set_servo_cam_angle_y(angle_y):
    angle_y = max(CAM_MIN, min(CAM_MAX, angle_y))
    pulse_y = int(SERVO_MID_PWM + (angle_y / SERVO_MID_DEG) * 500) 
    pi.set_servo_pulsewidth(SERVO_PIN_Y, pulse_y)

    
def cleanup():
    pi.set_servo_pulsewidth(SERVO_PIN_Y, 0)
    pi.set_servo_pulsewidth(SERVO_PIN_X, 0)
    pi.stop()
