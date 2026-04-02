import os
import warnings

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
warnings.filterwarnings(
    "ignore",
    message=".*Window.get_surface and Window.flip.*",
    category=DeprecationWarning,
)

import pygame
import pygame._sdl2 as sdl2
import tkinter as tk
from tkinter import filedialog

from core.network import load_network
from core.schedule import load_schedule
from core.simulation import Simulation

from render.layout import Layout
from render.renderer import Renderer


pygame.init()
pygame.display.set_caption("Railway Simulator")

screen_info = pygame.display.Info()
screen = pygame.display.set_mode(
    (screen_info.current_w, screen_info.current_h - 60), pygame.RESIZABLE
)

window = sdl2.Window.from_display_module()
window.maximize()

width = screen.get_width()
height = screen.get_height()

state = "HOME"

network_path = ""
schedule_path = ""

network = None
schedule = None
layout = None
simulation = None
renderer = None

clock = pygame.time.Clock()


first_browse_done = False


def select_file(title):
    global first_browse_done
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    kwargs = {"title": title, "filetypes": [("JSON files", "*.json")]}
    if not first_browse_done:
        kwargs["initialdir"] = os.getcwd()
        first_browse_done = True

    path = filedialog.askopenfilename(**kwargs)
    root.destroy()
    return path


# --- HOME SCREEN CONSTANTS ---
title_font = pygame.font.SysFont("Arial", 50, bold=True)
label_font = pygame.font.SysFont("Arial", 30)

btn_w, btn_h = 400, 60
network_browse_rect = pygame.Rect(width // 2 - btn_w // 2, height // 2 - 120, btn_w, btn_h)
schedule_browse_rect = pygame.Rect(width // 2 - btn_w // 2, height // 2 - 10, btn_w, btn_h)

run_w, run_h = 240, 70
run_btn_rect = pygame.Rect(width // 2 - run_w // 2, height // 2 + 130, run_w, run_h)


def draw_home_screen():
    # Fill background with dark blueprint color
    screen.fill((25, 25, 30))
    
    # Subtle blueprint grid overlay
    for x in range(0, width, 60):
        pygame.draw.line(screen, (35, 35, 40), (x, 0), (x, height), 1)
    for y in range(0, height, 60):
        pygame.draw.line(screen, (35, 35, 40), (0, y), (width, y), 1)

    # Main Title with drop shadow
    title_shadow = title_font.render("RAIL SIMULATOR", True, (10, 10, 15))
    screen.blit(title_shadow, title_shadow.get_rect(center=(width // 2 + 4, height // 2 - 266)))
    title_surf = title_font.render("RAIL SIMULATOR", True, (200, 220, 255))
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, height // 2 - 270)))

    # Central Card Graphic
    card_w, card_h = 560, 480
    card_rect = pygame.Rect(width // 2 - card_w // 2, height // 2 - 210, card_w, card_h)
    pygame.draw.rect(screen, (40, 45, 55), card_rect, border_radius=20)
    pygame.draw.rect(screen, (70, 80, 95), card_rect, width=3, border_radius=20)

    btn_color = (100, 120, 140)
    text_color = (255, 255, 255)

    # Network UI
    net_lbl = label_font.render("Network File (.json)", True, (180, 200, 220))
    screen.blit(net_lbl, net_lbl.get_rect(left=network_browse_rect.left + 10, bottom=network_browse_rect.top - 10))

    pygame.draw.rect(screen, btn_color, network_browse_rect, border_radius=10)
    net_btn_text = "Browse..." if not network_path else os.path.basename(network_path)
    net_text_surf = label_font.render(net_btn_text, True, text_color)
    if net_text_surf.get_width() > btn_w - 40:
        net_btn_text = net_btn_text[:25] + "..."
        net_text_surf = label_font.render(net_btn_text, True, text_color)
    screen.blit(net_text_surf, net_text_surf.get_rect(center=network_browse_rect.center))

    # Schedule UI
    sch_lbl = label_font.render("Schedule File (.json)", True, (180, 200, 220))
    screen.blit(sch_lbl, sch_lbl.get_rect(left=schedule_browse_rect.left + 10, bottom=schedule_browse_rect.top - 10))

    pygame.draw.rect(screen, btn_color, schedule_browse_rect, border_radius=10)
    sch_btn_text = "Browse..." if not schedule_path else os.path.basename(schedule_path)
    sch_text_surf = label_font.render(sch_btn_text, True, text_color)
    if sch_text_surf.get_width() > btn_w - 40:
        sch_btn_text = sch_btn_text[:25] + "..."
        sch_text_surf = label_font.render(sch_btn_text, True, text_color)
    screen.blit(sch_text_surf, sch_text_surf.get_rect(center=schedule_browse_rect.center))

    # Run Button
    can_run = bool(network_path and schedule_path)
    run_color = (50, 150, 255) if can_run else (60, 65, 75)
    
    if can_run:
        glow_rect = run_btn_rect.inflate(10, 10)
        pygame.draw.rect(screen, (20, 100, 200), glow_rect, border_radius=25)

    pygame.draw.rect(screen, run_color, run_btn_rect, border_radius=20)
    run_lbl_color = (255, 255, 255) if can_run else (120, 130, 140)
    run_lbl = label_font.render("Run Simulation", True, run_lbl_color)
    screen.blit(run_lbl, run_lbl.get_rect(center=run_btn_rect.center))


def init_sim():
    global network, schedule, layout, simulation, renderer
    network = load_network(network_path)
    schedule = load_schedule(schedule_path)
    layout = Layout(network)
    simulation = Simulation(network, schedule, layout)
    renderer = Renderer(network, layout, screen)


def clear_memory():
    global network_path, schedule_path, network, schedule, layout, simulation, renderer
    network_path = ""
    schedule_path = ""
    network = None
    schedule = None
    layout = None
    simulation = None
    renderer = None


# --- END SCREEN CONSTANTS ---
restart_btn_rect = pygame.Rect(width // 2 - 220, height // 2, 200, 60)
home_btn_rect = pygame.Rect(width // 2 + 20, height // 2, 200, 60)


def draw_end_screen():
    # Draw translucent overlay over the finished simulation frame
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    end_title = title_font.render("SIMULATION ENDED", True, (255, 255, 255))
    screen.blit(end_title, end_title.get_rect(center=(width // 2, height // 2 - 100)))

    # Restart
    pygame.draw.rect(screen, (100, 200, 100), restart_btn_rect, border_radius=10)
    r_lbl = label_font.render("Restart", True, (255, 255, 255))
    screen.blit(r_lbl, r_lbl.get_rect(center=restart_btn_rect.center))

    # Home
    pygame.draw.rect(screen, (200, 100, 100), home_btn_rect, border_radius=10)
    h_lbl = label_font.render("Home", True, (255, 255, 255))
    screen.blit(h_lbl, h_lbl.get_rect(center=home_btn_rect.center))


running = True
dragging = False
last_mouse_pos = (0, 0)

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "HOME":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if network_browse_rect.collidepoint(event.pos):
                    path = select_file("Select Network JSON")
                    if path:
                        network_path = path
                elif schedule_browse_rect.collidepoint(event.pos):
                    path = select_file("Select Schedule JSON")
                    if path:
                        schedule_path = path
                elif run_btn_rect.collidepoint(event.pos):
                    if network_path and schedule_path:
                        init_sim()
                        state = "SIMULATION"

        elif state == "SIMULATION":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if renderer.btn_rect.collidepoint(event.pos):
                        simulation.is_paused = not simulation.is_paused
                    elif renderer.exit_btn_rect.collidepoint(event.pos):
                        state = "END"
                    elif renderer.speed_minus_rect.collidepoint(event.pos):
                        simulation.speed = max(0.5, simulation.speed - 0.5)
                    elif renderer.speed_plus_rect.collidepoint(event.pos):
                        simulation.speed = min(10.0, simulation.speed + 0.5)
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

        elif state == "END":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_btn_rect.collidepoint(event.pos):
                    init_sim()
                    state = "SIMULATION"
                elif home_btn_rect.collidepoint(event.pos):
                    clear_memory()
                    state = "HOME"

    if state == "HOME":
        draw_home_screen()
        pygame.display.flip()

    elif state == "SIMULATION":
        simulation.update(dt)
        if getattr(simulation, "is_finished", False):
            state = "END"
        else:
            if renderer:
                renderer.draw(simulation)
            pygame.display.flip()

    elif state == "END":
        if renderer:
            renderer.draw(simulation)
        draw_end_screen()
        pygame.display.flip()

pygame.quit()
