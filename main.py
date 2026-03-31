import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame

from core.network import load_network
from core.schedule import load_schedule
from core.simulation import Simulation

from render.layout import Layout
from render.renderer import Renderer


network = load_network("input/network.json")

schedule = load_schedule("input/schedule.json")

layout = Layout(network)

simulation = Simulation(network, schedule, layout)

renderer = Renderer(network, layout)

clock = pygame.time.Clock()

running = True
dragging = False
last_mouse_pos = (0, 0)

while running:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if renderer.btn_rect.collidepoint(event.pos):
                    simulation.is_paused = not simulation.is_paused
                else:
                    dragging = True
                    last_mouse_pos = event.pos
            elif event.button == 4:
                renderer.camera.zoom_at(0.5, *event.pos)
            elif event.button == 5:
                renderer.camera.zoom_at(-0.5, *event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                renderer.camera.x -= dx / renderer.camera.zoom
                renderer.camera.y -= dy / renderer.camera.zoom
                last_mouse_pos = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                renderer.camera.zoom_at(0.5, 700, 400)
            elif event.key == pygame.K_DOWN:
                renderer.camera.zoom_at(-0.5, 700, 400)

    simulation.update(dt)

    if getattr(simulation, "is_finished", False):
        running = False

    renderer.draw(simulation)
