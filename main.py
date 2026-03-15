import pygame

from core.network import load_network
from core.schedule import load_schedule
from core.simulation import Simulation

from render.layout import Layout
from render.renderer import Renderer


network = load_network("input/network.json")

schedule = load_schedule("input/schedule.json")

layout = Layout(network)

simulation = Simulation(network, schedule)

renderer = Renderer(network, layout)

clock = pygame.time.Clock()

running = True

while running:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    simulation.update(dt)

    renderer.draw(simulation)
