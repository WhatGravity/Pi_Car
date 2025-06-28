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

try:
    while True:
        pygame.event.pump()

        fwd = joystick.get_axis(4)    # rechter Trigger (A5)
        rev = joystick.get_axis(5)    # linker Trigger (A4)
        steer = joystick.get_axis(0)  # linker Stick X
        cam_y = joystick.get_axis(3)  # rechter Stick Y
        cam_x = joystick.get_axis(2)  # rechter Stick X

        # ─── Motorsteuerung ───
        if fwd > 0.1 and rev < 0.1:
            dc = fwd * PWM_MAX
            motor_control.forward(dc)
        elif rev > 0.1 and fwd < 0.1:
            dc = rev * PWM_MAX
            motor_control.reverse(dc)
        else:
            motor_control.stop()

        # ─── Lenkung (linker Stick) mit Centering ───
        if abs(steer) > DEADZONE:
            angle = -steer * 80
            rounded_steering_angle = round(angle)
            if rounded_steering_angle != last_steering_angle:
                steering.set_steering_angle(angle)
                last_steering_angle = rounded_steering_angle                
        else:
            steering.set_steering_angle(0)
            
        # ─── CAM (rechter Stick) ───
        if abs(cam_x) > DEADZONE:
            cam_angle_x = cam_x * 80
            rounded_cam_angle_x = round(cam_angle_x)
            if rounded_cam_angle_x != last_cam_angle_x:
                cam_servo.set_servo_cam_angle_x(cam_angle_x)
                last_cam_angle_x = rounded_cam_angle_x
        elif abs(cam_y) > DEADZONE:
            cam_angle_y = cam_y * 80
            rounded_cam_angle_y = round(cam_angle_y)
            if rounded_cam_angle_y != last_cam_angle_y:
                    cam_servo.set_servo_cam_angle_y(cam_angle_y)
                    last_cam_angle_y = rounded_cam_angle_y        
        else:
            cam_servo.set_servo_cam_angle_x(0)
            cam_servo.set_servo_cam_angle_y(0)

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
