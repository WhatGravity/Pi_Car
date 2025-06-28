import pigpio
import pygame
import time

# --- pigpio Setup ---
SERVO_PIN = 18  # GPIO18
pi = pigpio.pi()
if not pi.connected:
    print("Fehler: pigpio Daemon nicht verbunden.")
    exit()

# --- Servo-Pulsewerte (µs) ---
PULSE_LEFT = 1000   # ca. 0°
PULSE_MID = 1500    # ca. 90°
PULSE_RIGHT = 2000  # ca. 180°

# --- Schwellen ---
DEADZONE = 0.2
CHANGE_THRESHOLD = 50  # in µs (nur setzen wenn >50µs Unterschied)

last_pulse = None

# --- Xbox Controller mit pygame ---
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Kein Controller erkannt.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller verbunden: {joystick.get_name()}")

try:
    while True:
        pygame.event.pump()
        x_axis = joystick.get_axis(0)  # linker Stick, horizontal

        if x_axis < -DEADZONE:
            pulse = PULSE_LEFT
        elif x_axis > DEADZONE:
            pulse = PULSE_RIGHT
        else:
            pulse = PULSE_MID

        if last_pulse is None or abs(pulse - last_pulse) > CHANGE_THRESHOLD:
            pi.set_servo_pulsewidth(SERVO_PIN, pulse)
            last_pulse = pulse

        time.sleep(0.05)  # 20Hz Update

except KeyboardInterrupt:
    print("Beende Programm")

finally:
    pi.set_servo_pulsewidth(SERVO_PIN, 0)  # Servo-Signal aus
    pi.stop()
    pygame.quit()
