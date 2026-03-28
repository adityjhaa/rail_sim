import pygame
import math
from core.pathing import cubic_bezier

class Camera:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.zoom = 1

    def world_to_screen(self, x, y):

        sx = (x - self.x) * self.zoom
        sy = (y - self.y) * self.zoom

        return sx, sy

    def zoom_at(self, delta, screen_x, screen_y):
        new_zoom = self.zoom + delta
        new_zoom = max(0.5, min(2.5, new_zoom))
        
        if new_zoom == self.zoom:
            return

        wx = (screen_x / self.zoom) + self.x
        wy = (screen_y / self.zoom) + self.y

        self.zoom = new_zoom

        self.x = wx - (screen_x / self.zoom)
        self.y = wy - (screen_y / self.zoom)


class Renderer:

    def __init__(self, network, layout):

        self.network = network
        self.layout = layout

        pygame.init()

        pygame.display.set_caption("Railway Simulator")

        self.screen = pygame.display.set_mode((1400, 800))

        self.font = pygame.font.SysFont(None, 20)

        self.camera = Camera()
        self.btn_rect = pygame.Rect(1200, 50, 100, 40)

    # -------------------------------------------------

    def draw_station(self, station):

        x = self.layout.station_positions[station]

        tracks = self.layout.track_positions[station]
        station_obj = self.network.get_station(station)

        for track_id, (tx, ty) in tracks.items():

            sx, sy = self.camera.world_to_screen(tx, ty)
            sx1, sy1 = self.camera.world_to_screen(tx - 40, ty)
            sx2, sy2 = self.camera.world_to_screen(tx + 40, ty)

            # draw track
            pygame.draw.line(
                self.screen, (0, 120, 255), (sx1, sy1), (sx2, sy2), max(1, int(4 * self.camera.zoom))
            )

            # draw track label (s1, s2...)
            label = self.font.render(track_id, True, (255, 255, 255))
            self.screen.blit(label, (sx - 70, sy - 10))

            # get platform
            platform = station_obj.tracks[track_id].platform

            if platform > 0:

                pf_label = self.font.render(f"PF_{platform}", True, (255, 255, 0))

                self.screen.blit(pf_label, (sx + 50, sy - 10))

        # station name
        label = self.font.render(station, True, (0, 255, 0))
        sx, sy = self.camera.world_to_screen(x, 150)

        self.screen.blit(label, (sx - 10, sy))

    # -------------------------------------------------

    def draw_blocks(self):

        for block in self.network.get_blocks():

            key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)

            if key not in self.layout.block_positions:
                continue

            x, y = self.layout.block_positions[key]

            sx, sy = self.camera.world_to_screen(x, y)

            # color by direction
            color = (0, 200, 200) if block.branch_id == 0 else (200, 0, 120)

            # draw block track
            sx1, sy1 = self.camera.world_to_screen(x - 60, y)
            sx2, sy2 = self.camera.world_to_screen(x + 60, y)
            pygame.draw.line(self.screen, color, (sx1, sy1), (sx2, sy2), max(1, int(4 * self.camera.zoom)))

            # draw label
            label = self.font.render(
                f"BSN_{block.branch_id + 1}", True, (255, 255, 255)
            )

            self.screen.blit(label, (sx - 25, sy - 20))

    # -------------------------------------------------

    def draw_trains(self, trains):

        for train in trains:
            sx, sy = self.camera.world_to_screen(train.x, train.y)
            angle_rad = math.radians(getattr(train, 'angle', 0))
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            
            def rotate(pt):
                return (sx + pt[0]*cos_a - pt[1]*sin_a, sy + pt[0]*sin_a + pt[1]*cos_a)

            length = 24 * self.camera.zoom
            width = 12 * self.camera.zoom
            hw = width / 2
            hl = length / 2
            
            # main body
            pts = [
                rotate((-hl, -hw)),
                rotate((hl, -hw)),
                rotate((hl, hw)),
                rotate((-hl, hw))
            ]
            
            # cab (windshield)
            cab_len = 6 * self.camera.zoom
            cab_pad = 2 * self.camera.zoom
            cab_pts = [
                rotate((hl - cab_len, -hw + cab_pad)),
                rotate((hl, -hw + cab_pad)),
                rotate((hl, hw - cab_pad)),
                rotate((hl - cab_len, hw - cab_pad))
            ]

            pygame.draw.polygon(self.screen, (220, 220, 220), pts)
            pygame.draw.polygon(self.screen, (50, 150, 255), cab_pts)
            pygame.draw.lines(self.screen, (30, 30, 30), True, pts, 2)
            
            train_id = self.font.render(f"{train.id}", True, (255, 255, 255))
            id_rect = train_id.get_rect()
            id_rect.center = (sx, sy - 20)
            self.screen.blit(train_id, id_rect)

    # -------------------------------------------------

    def draw_connections(self):

        for block in self.network.get_blocks():

            key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)

            if key not in self.layout.block_positions:
                continue

            bx, by = self.layout.block_positions[key]
            color = (0, 200, 200) if block.branch_id == 0 else (200, 0, 120)

            for station, track in block.connections:

                tx, ty = self.layout.track_positions[station][track]
                station_x = self.layout.station_positions[station]

                if station_x < bx:
                    entry_x = bx - 60
                    station_edge_x = tx + 40
                    c_len = abs(entry_x - station_edge_x) * 0.5
                    p0 = (station_edge_x, ty)
                    p1 = (station_edge_x + c_len, ty)
                    p2 = (entry_x - c_len, by)
                    p3 = (entry_x, by)
                else:
                    entry_x = bx + 60
                    station_edge_x = tx - 40
                    c_len = abs(entry_x - station_edge_x) * 0.5
                    p0 = (station_edge_x, ty)
                    p1 = (station_edge_x - c_len, ty)
                    p2 = (entry_x + c_len, by)
                    p3 = (entry_x, by)

                curve_points = cubic_bezier(p0, p1, p2, p3)
                screen_points = [self.camera.world_to_screen(px, py) for px, py in curve_points]

                if len(screen_points) >= 2:
                    line_w = max(1, int(3 * self.camera.zoom))
                    pygame.draw.lines(self.screen, color, False, screen_points, line_w)

    def draw_ui(self, simulation):
        time_font = pygame.font.SysFont("Arial", 30)
        time_surface = time_font.render(f"Time: {int(simulation.sim_time)}", True, (0, 255, 0))
        time_rect = time_surface.get_rect()
        time_rect.center = (1300, 20)
        self.screen.blit(time_surface, time_rect)

        is_paused = getattr(simulation, 'is_paused', False)
        color = (100, 200, 100) if is_paused else (200, 100, 100)
        text = "PLAY" if is_paused else "PAUSE"

        pygame.draw.rect(self.screen, color, self.btn_rect, border_radius=5)
        
        msg = time_font.render(text, True, (255, 255, 255))
        msg_rect = msg.get_rect(center=self.btn_rect.center)
        self.screen.blit(msg, msg_rect)

    def draw(self, simulation):

        self.screen.fill((30, 30, 30))
        self.draw_connections()

        for station in self.network.stations:
            self.draw_station(station)

        self.draw_blocks()

        trains = simulation.get_active_trains()

        self.draw_trains(trains)

        self.draw_ui(simulation)

        pygame.display.flip()
