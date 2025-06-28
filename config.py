# ───── Constants ─────
DEADZONE = 0.25
PWM_MAX = 100  # Maximaler PWM-Wert für Motorsteuerung

# ───── Steering ─────
SERVO_STEERING_PIN = 18
SERVO_MID = 1500         # Mittelstellung als PWM
SERVO_MID_DEG = 90
MAX_LEFT = -60        # maximaler Einschlag links
MAX_RIGHT = 60         # maximaler Einschlag rechts

# ───── Cam ─────
SERVO_PIN_X = 12
SERVO_PIN_Y = 16
CAM_MIN = -90
CAM_MAX = 90

# ───── Motor ─────
PWM_FWD = 13 #PWM1 Channel 1
PWM_REV = 19 #PWM1 Channel 1, alternativ Pin