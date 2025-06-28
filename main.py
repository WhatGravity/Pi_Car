import RPi.GPIO as GPIO
import time
import pygame
import os
import sys
import subprocess
from config import *
import motor_control
import steering
import cam_servo

# ───── Variables ─────
last_steering_angle = 0
rounded_steering_angle = 0
last_cam_angle_x = 0
rounded_cam_angle_x = 0
last_cam_angle_y = 0
rounded_cam_angle_y = 0

# ───── Pygame Controller Init ─────
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Kein Controller erkannt.")
    sys.exit(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()

# ───── Livestream starten ─────
cam_proc = subprocess.Popen(["python3", "cam_livestream.py"])

# ───── Main Loop ─────
print("Steuerung aktiv – STRG+C zum Beenden")

def process_motor_control(forward, reverse):
    if forward > DEADZONE_MOTOR and reverse < DEADZONE_MOTOR:
        dc = forward * PWM_MAX
        motor_control.forward(dc)
    elif reverse > DEADZONE_MOTOR and forward < DEADZONE_MOTOR:
        dc = reverse * PWM_MAX
        motor_control.reverse(dc)
    else:
        motor_control.stop()

def process_steering(steer):
    if abs(steer) > DEADZONE_STEER:
        angle = -steer * TO_DEG
        rounded_steering_angle = round(angle)
        if rounded_steering_angle != last_steering_angle:
            steering.set_steering_angle(angle)
            last_steering_angle = rounded_steering_angle                
    else:
        steering.center_steering()

def process_camera(cam_x, cam_y):
    if abs(cam_x) > DEADZONE_CAM:
        cam_angle_x = cam_x * TO_DEG
        rounded_cam_angle_x = round(cam_angle_x)
        if rounded_cam_angle_x != last_cam_angle_x:
            cam_servo.set_servo_cam_angle_x(cam_angle_x)
            last_cam_angle_x = rounded_cam_angle_x
    elif abs(cam_y) > DEADZONE_CAM:
        cam_angle_y = cam_y * TO_DEG
        rounded_cam_angle_y = round(cam_angle_y)
        if rounded_cam_angle_y != last_cam_angle_y:
                cam_servo.set_servo_cam_angle_y(cam_angle_y)
                last_cam_angle_y = rounded_cam_angle_y        
    else:
        cam_servo.set_servo_cam_angle_x(0)
        cam_servo.set_servo_cam_angle_y(0)

try:
    while True:
        pygame.event.pump()

        forward = joystick.get_axis(AXIS_FOWARD)    # rechter Trigger (A5)
        reverse = joystick.get_axis(AXIS_REVERSE)    # linker Trigger (A4)
        steer = joystick.get_axis(AXIS_STEER)  # linker Stick X
        cam_y = joystick.get_axis(AXIS_CAM_Y)  # rechter Stick Y
        cam_x = joystick.get_axis(AXIS_CAM_X)  # rechter Stick X

        process_motor_control(forward, reverse)
        process_steering(steer)
        process_camera(cam_x, cam_y)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n Beendet durch Benutzer.")

finally:
    motor_control.cleanup()
    steering.cleanup()
    cam_servo.cleanup()
    GPIO.cleanup()
    pygame.quit()
    cam_proc.terminate()
    cam_proc.wait()
    print("Sauber beendet.")
