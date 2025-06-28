# Raspberry Pi Car

Das ganze ist aus einem Projekt für ein Fach an der Universität entstanden.

# Projekt Flowchart

## Gesamtarchitektur

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PMT2 PI CAR SYSTEM                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐  │
│  │   CONTROLLER    │    │   MAIN CONTROL  │    │    CAMERA LIVESTREAM       │  │
│  │   (Eingabe)     │───▶│   (main.py)     │    │   (cam_livestream.py)      │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────────┘  │
│                                │                                                │
│                                ▼                                                │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐  │
│  │   MOTOR         │    │   STEERING      │    │    CAMERA SERVO            │  │
│  │   CONTROL       │    │   CONTROL       │    │    CONTROL                 │  │
│  │ (motor_control) │    │  (steering.py)  │    │   (cam_servo.py)           │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Haupt-Steuerungsablauf (main.py)

```
START
  │
  ├─ Pygame Controller initialisieren
  │
  ├─ Kamera-Livestream starten (subprocess)
  │  └─ cam_livestream.py läuft parallel
  │
  ├─ MAIN LOOP (Endlosschleife)
  │  │
  │  ├─ Controller-Eingaben lesen:
  │  │  ├─ fwd = Rechter Trigger (vorwärts)
  │  │  ├─ rev = Linker Trigger (rückwärts)
  │  │  ├─ steer = Linker Stick X (Lenkung)
  │  │  ├─ cam_x = Rechter Stick X (Kamera horizontal)
  │  │  └─ cam_y = Rechter Stick Y (Kamera vertikal)
  │  │
  │  ├─ MOTORSTEUERUNG:
  │  │  ├─ Wenn fwd > 0.1 → motor_control.forward(duty_cycle)
  │  │  ├─ Wenn rev > 0.1 → motor_control.reverse(duty_cycle)
  │  │  └─ Sonst → motor_control.stop()
  │  │
  │  ├─ LENKSTEUERUNG:
  │  │  ├─ Wenn |steer| > DEADZONE → steering.set_steering_angle(angle)
  │  │  └─ Sonst → steering.set_steering_angle(0)
  │  │
  │  ├─ KAMERASTEUERUNG:
  │  │  ├─ Wenn |cam_x| > DEADZONE → cam_servo.set_servo_cam_angle_x(angle)
  │  │  ├─ Wenn |cam_y| > DEADZONE → cam_servo.set_servo_cam_angle_y(angle)
  │  │  └─ Sonst → Kamera auf Mittelposition
  │  │
  │  ├─ Sleep 0.05s (20 Hz Update-Rate)
  │  └─ Zurück zum Loop-Anfang
  │
  └─ Bei STRG+C:
     ├─ Cleanup aller Module
     ├─ GPIO zurücksetzen
     ├─ Kamera-Prozess beenden
     └─ Programm beenden
```

## Motor-Steuerung (motor_control.py)

```
MOTOR CONTROL
  │
  ├─ GPIO Setup (PWM Pins für Vorwärts/Rückwärts)
  │
  ├─ forward(duty_cycle):
  │  ├─ Rückwärts-PWM auf 0%
  │  └─ Vorwärts-PWM auf duty_cycle%
  │
  ├─ reverse(duty_cycle):
  │  ├─ Vorwärts-PWM auf 0%
  │  └─ Rückwärts-PWM auf duty_cycle%
  │
  ├─ stop():
  │  ├─ Vorwärts-PWM auf 0%
  │  └─ Rückwärts-PWM auf 0%
  │
  └─ cleanup():
     ├─ Motoren stoppen
     └─ PWM-Kanäle schließen
```

## Lenk-Steuerung (steering.py)

```
STEERING CONTROL
  │
  ├─ pigpio Verbindung aufbauen
  │
  ├─ set_steering_angle(angle):
  │  ├─ Winkel auf MIN/MAX begrenzen (-60° bis +60°)
  │  ├─ Wenn angle = 0 → Servo auf Mittelstellung (1500μs)
  │  ├─ Sonst → Winkel in Pulslänge umrechnen
  │  └─ Servo-Pulslänge setzen
  │
  └─ cleanup():
     ├─ Servo stoppen (0μs)
     └─ pigpio Verbindung schließen
```

## Kamera-Servo-Steuerung (cam_servo.py)

```
CAMERA SERVO CONTROL
  │
  ├─ pigpio Verbindung aufbauen
  │
  ├─ set_servo_cam_angle_x(angle_x):
  │  ├─ Winkel auf MIN/MAX begrenzen (-90° bis +90°)
  │  ├─ Winkel in Pulslänge umrechnen
  │  └─ X-Servo-Pulslänge setzen
  │
  ├─ set_servo_cam_angle_y(angle_y):
  │  ├─ Winkel auf MIN/MAX begrenzen (-90° bis +90°)
  │  ├─ Winkel in Pulslänge umrechnen
  │  └─ Y-Servo-Pulslänge setzen
  │
  └─ cleanup():
     ├─ Beide Servos stoppen (0μs)
     └─ pigpio Verbindung schließen
```

## Kamera-Livestream (cam_livestream.py)

```
CAMERA LIVESTREAM
  │
  ├─ Flask App initialisieren
  ├─ Picamera2 Setup (1280x720, 60fps)
  │
  ├─ gen_frames():
  │  └─ Endlosschleife:
  │     ├─ Kamerabild aufnehmen
  │     ├─ Als JPEG komprimieren
  │     └─ Als MJPEG-Stream ausgeben
  │
  ├─ Flask Routes:
  │  ├─ '/' → index.html anzeigen
  │  └─ '/video_feed' → MJPEG-Stream
  │
  └─ Webserver starten (10.42.0.1:5000)
```

## Datenfluss

```
Controller Input → main.py → Hardware-Module → Physische Reaktion
     ↓
┌─────────────────────────────────────────────────────────────────┐
│ Trigger/Stick-Werte → PWM-Signale → Motor/Servo-Bewegung       │
│                                                                 │
│ Kamera (parallel) → Bilderfassung → MJPEG-Stream → Webserver   │
└─────────────────────────────────────────────────────────────────┘
```

## Pin-Belegung (aus config.py)

```
HARDWARE PINS:
├─ Lenkung: GPIO 18 (Servo)
├─ Kamera X: GPIO 12 (Servo)
├─ Kamera Y: GPIO 16 (Servo)
├─ Motor Vorwärts: GPIO 13 (PWM)
└─ Motor Rückwärts: GPIO 19 (PWM)
```

## Verwendete Bibliotheken

- **pygame**: Controller-Eingabe
- **RPi.GPIO**: GPIO-Pins und PWM für Motoren
- **pigpio**: Präzise Servo-Steuerung
- **Flask**: Webserver für Livestream
- **Picamera2**: Kamera-Interface
- **OpenCV**: Bildverarbeitung/JPEG-Komprimierung

## Wichtige Einstellungen

- **Update-Rate**: 20 Hz (50ms Pause)
- **Deadzone**: 0.25 (Controller-Totbereich)
- **Max PWM**: 100% (Motorleistung)
- **Servo-Bereiche**: 
  - Lenkung: -60° bis +60°
  - Kamera: -90° bis +90°
- **Kamera-Stream**: 1280x720, 60fps, MJPEG
