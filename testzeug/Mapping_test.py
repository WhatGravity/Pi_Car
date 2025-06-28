import pygame
from pygame._sdl2 import controller

pygame.init()
controller.init()

if controller.get_count() == 0:
    print("Kein Controller verbunden.")
    pygame.quit()
    exit()
ctrl = controller.Controller(0)

mapping = ctrl.get_mapping()
print("Mapping des Controllers:")
for key, value in mapping.items():
    print(f"{key}: value")


# Event-Loop (um z. B. zu warten – Mapping braucht oft keine Events)
running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

pygame.quit()