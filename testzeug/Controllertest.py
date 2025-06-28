import pygame
import sys

# Pygame initialisieren
pygame.init()

# Fenster für die Anzeige
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Controller Test")

# Schriftart
font = pygame.font.Font(None, 30)

# Joystick initialisieren
pygame.joystick.init()

# Prüfe, ob ein Controller angeschlossen ist
if pygame.joystick.get_count() == 0:
    print("Kein Controller gefunden!")
    pygame.quit()
    sys.exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller verbunden: {joystick.get_name()}")

def draw_text(text, x, y):
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (x, y))

# Hauptloop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_text(f"Controller: {joystick.get_name()}", 20, 20)

    # Tasten
    draw_text("Tasten:", 20, 60)
    for i in range(joystick.get_numbuttons()):
        pressed = joystick.get_button(i)
        draw_text(f"Button {i}: {'gedrückt' if pressed else 'frei'}", 40, 90 + i * 20)

    # Achsen
    draw_text("Achsen:", 300, 60)
    for i in range(joystick.get_numaxes()):
        axis = joystick.get_axis(i)
        draw_text(f"Achse {i}: {axis:.2f}", 320, 90 + i * 20)

    # D-Pad (Hat)
    draw_text("D-Pad:", 20, 250)
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        draw_text(f"Hat {i}: {hat}", 40, 280 + i * 20)

    pygame.display.flip()
    clock.tick(30)

# Aufräumen
pygame.quit()
