import RPi.GPIO as GPIO
import time
import pygame
import os
import sys

# ───── GPIO Setup ─────
GPIO.setmode(GPIO.BCM)

# Motor Pins
PWM_FWD = 13
PWM_REV = 19
GPIO.setup(PWM_FWD, GPIO.OUT)
GPIO.setup(PWM_REV, GPIO.OUT)
pwm_fwd = GPIO.PWM(PWM_FWD, 10000)
pwm_rev = GPIO.PWM(PWM_REV, 10000)
pwm_fwd.start(0)
pwm_rev.start(0)

# Servo 1 – Lenkung (GPIO 18)
SERVO_STEERING_PIN = 18
GPIO.setup(SERVO_STEERING_PIN, GPIO.OUT)
steer_pwm = GPIO.PWM(SERVO_STEERING_PIN, 50)
steer_pwm.start(7.5)

# Servo 2 – Zusatzfunktion (GPIO 12)
SERVO_CAM_PIN = 12
GPIO.setup(SERVO_CAM_PIN, GPIO.OUT)
cam_pwm = GPIO.PWM(SERVO_CAM_PIN, 50)
cam_pwm.start(7.5)

# ───── Steuerungswerte ─────
last_angle = 90

PWM_MAX = 100
STEERING_MAX_WINKEL = 85
SERVO_MID = 90
DEADZONE = 0.1            # für Stick-Jitter
JITTER_TOLERANZ = 5.0     # Gradänderung, unter der nicht reagiert wird
STICK_ANGLE_STEPS = 5   # Schrittweite für Servo2 bei Stickbewegung

# ───── Pygame Controller Init ─────
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ Kein Controller erkannt.")
    sys.exit(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()

# ───── Funktionen ─────
def motor_forward(dc):
    pwm_rev.ChangeDutyCycle(0)
    pwm_fwd.ChangeDutyCycle(dc)

def motor_reverse(dc):
    pwm_fwd.ChangeDutyCycle(0)
    pwm_rev.ChangeDutyCycle(dc)

def motor_stop():
    pwm_fwd.ChangeDutyCycle(0)
    pwm_rev.ChangeDutyCycle(0)

def set_steering_angle(angle):
    global last_angle
    angle = max(-STEERING_MAX_WINKEL, min(STEERING_MAX_WINKEL, angle))
    target_angle = SERVO_MID + angle
    if abs(target_angle - last_angle) >= JITTER_TOLERANZ:
        duty = 2.5 + (target_angle / 180.0) * 10.0
        steer_pwm.ChangeDutyCycle(duty)
        last_angle = target_angle

def set_servo_cam_angle(angle):
    global last_angle
    angle = max(-STEERING_MAX_WINKEL, min(STEERING_MAX_WINKEL, angle))
    target_angle = SERVO_MID + angle
    if abs(target_angle - last_angle) >= JITTER_TOLERANZ:
        duty = 2.5 + (target_angle / 180.0) * 10.0
        cam_pwm.ChangeDutyCycle(duty)
        last_angle = target_angle

# ───── Hauptloop ─────
print("🚗 Steuerung aktiv – STRG+C zum Beenden")

try:
    while True:
        pygame.event.pump()

        fwd = joystick.get_axis(5)      # rechter Trigger (A5)
        rev = joystick.get_axis(4)     # linker Trigger (A4)
        steer = joystick.get_axis(0)    # linker Stick X
        cam = joystick.get_axis(3)      # rechter Stick Y

        # ─── Motorsteuerung ───
        if fwd > 0.1 and rev < 0.1:
            dc = fwd * PWM_MAX
            motor_forward(dc)
        elif rev > 0.1 and fwd < 0.1:
            dc = rev * PWM_MAX
            motor_reverse(dc)
        else:
            motor_stop()

        # ─── Lenkung (linker Stick) ───
        if abs(steer) > DEADZONE:
            angle = steer * STEERING_MAX_WINKEL
            set_steering_angle(angle)

        # ─── CAM (rechter Stick Y) ───
        if abs(cam) > DEADZONE:
            target = last_angle + cam * STICK_ANGLE_STEPS
            set_servo_cam_angle(target)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n🛑 Beendet durch Benutzer.")

finally:
    motor_stop()
    pwm_fwd.stop()
    pwm_rev.stop()
    steer_pwm.stop()
    cam_pwm.stop()
    GPIO.cleanup()
    pygame.quit()
    print("✅ Sauber beendet.")
