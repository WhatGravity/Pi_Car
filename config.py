# ───── GPIO Pins ─────
SERVO_STEERING_PIN = 18
SERVO_PIN_X = 12
SERVO_PIN_Y = 16
PWM_FWD = 13 #PWM1 Channel 1
PWM_REV = 19 #PWM1 Channel 1, alternativ Pin

# ───── Joystick ─────
AXIS_FOWARD = 4    # rechter Trigger (A5)
AXIS_REVERSE = 5    # linker Trigger (A4)
AXIS_STEER = 0      # linker Stick X
AXIS_CAM_Y = 3      # rechter Stick Y
AXIS_CAM_X = 2      # rechter Stick X

# ───── Servos ─────
DEADZONE_STEER = 0.15
SERVO_MID_PWM = 1500         # Mittelstellung als PWM
SERVO_MID_DEG = 90
MAX_LEFT = -60        # maximaler Einschlag links
MAX_RIGHT = 60         # maximaler Einschlag rechts

# ───── Cam ─────
DEADZONE_CAM = 0.25
CAM_MIN = -90
CAM_MAX = 90

# ───── Motor ─────
DEADZONE_MOTOR = 0.1
PWM_MAX = 100  # Maximaler PWM-Wert für Motorsteuerung

# ───── Constant ─────
TO_DEG = 80  # Umrechnungsfaktor für Joystick-Achsen