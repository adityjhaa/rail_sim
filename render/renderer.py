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

    def __init__(self, network, layout, screen):

        self.network = network
        self.layout = layout
        self.screen = screen

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.font = pygame.font.SysFont(None, 20)

        self.camera = Camera()
        self.btn_rect = pygame.Rect(self.width // 2 - 50, self.height - 60, 100, 40)
        self.exit_btn_rect = pygame.Rect(self.width // 2 + 70, self.height - 60, 80, 40)

        # Speed controls to the left of the play/pause button
        gap_to_play = 20
        btn_w, btn_h = 40, 40
        speed_w = 140
        gap = 5

        start_x = self.btn_rect.left - gap_to_play - btn_w
        self.speed_plus_rect = pygame.Rect(start_x, self.height - 60, btn_w, btn_h)

        start_x -= speed_w + gap
        self.speed_text_rect = pygame.Rect(start_x, self.height - 60, speed_w, btn_h)

        start_x -= btn_w + gap
        self.speed_minus_rect = pygame.Rect(start_x, self.height - 60, btn_w, btn_h)

    # -------------------------------------------------

    def render_scaled_text(self, text, color):
        target_size = max(1, int(20 * self.camera.zoom))
        if not hasattr(self, "_font_cache"):
            self._font_cache = {}

        if target_size not in self._font_cache:
            self._font_cache[target_size] = pygame.font.SysFont(None, target_size)

        font = self._font_cache[target_size]
        return font.render(str(text), True, color)

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
                self.screen,
                (0, 120, 255),
                (sx1, sy1),
                (sx2, sy2),
                max(1, int(4 * self.camera.zoom)),
            )

            # draw track label (s1, s2...)
            label = self.render_scaled_text(track_id, (255, 255, 255))
            self.screen.blit(
                label, (sx - 70 * self.camera.zoom, sy - 10 * self.camera.zoom)
            )

            # get platform
            platform = station_obj.tracks[track_id].platform

            if platform > 0:

                pf_label = self.render_scaled_text(f"PF_{platform}", (255, 255, 0))

                self.screen.blit(
                    pf_label, (sx + 50 * self.camera.zoom, sy - 10 * self.camera.zoom)
                )

        # station name
        label = self.render_scaled_text(station, (0, 255, 0))

        top_y = min((ty for tx, ty in tracks.values())) if tracks else 150
        sx, sy = self.camera.world_to_screen(x, top_y - 40)

        self.screen.blit(label, (sx - 10 * self.camera.zoom, sy))

    # -------------------------------------------------

    def draw_blocks(self):

        for block in self.network.get_blocks():

            key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)

            if key not in self.layout.block_positions:
                continue

            x, y = self.layout.block_positions[key]

            sx, sy = self.camera.world_to_screen(x, y)

            # color by direction
            pair_key = tuple(sorted([block.station_a, block.station_b]))
            total_blocks = getattr(self.layout, "block_counts", {}).get(pair_key, 1)

            if total_blocks <= 2:
                color = (0, 200, 200) if block.branch_id == 0 else (200, 0, 120)
            else:
                if block.branch_id == 0:
                    color = (0, 200, 200)
                elif block.branch_id == total_blocks - 1:
                    color = (200, 0, 120)
                else:
                    color = (255, 128, 0)  # Orange

            # draw block track
            sx1, sy1 = self.camera.world_to_screen(x - 60, y)
            sx2, sy2 = self.camera.world_to_screen(x + 60, y)
            pygame.draw.line(
                self.screen,
                color,
                (sx1, sy1),
                (sx2, sy2),
                max(1, int(4 * self.camera.zoom)),
            )

            # draw label
            label = self.render_scaled_text(
                f"BSN_{block.branch_id + 1}", (255, 255, 255)
            )

            self.screen.blit(
                label, (sx - 25 * self.camera.zoom, sy - 20 * self.camera.zoom)
            )

    # -------------------------------------------------

    def draw_trains(self, trains):

        for train in trains:
            sx, sy = self.camera.world_to_screen(train.x, train.y)
            angle_rad = math.radians(getattr(train, "angle", 0))
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            def rotate(pt):
                return (
                    sx + pt[0] * cos_a - pt[1] * sin_a,
                    sy + pt[0] * sin_a + pt[1] * cos_a,
                )

            length = 24 * self.camera.zoom
            width = 12 * self.camera.zoom
            hw = width / 2
            hl = length / 2

            # main body
            pts = [
                rotate((-hl, -hw)),
                rotate((hl, -hw)),
                rotate((hl, hw)),
                rotate((-hl, hw)),
            ]

            # cab (windshield)
            cab_len = 6 * self.camera.zoom
            cab_pad = 2 * self.camera.zoom
            cab_pts = [
                rotate((hl - cab_len, -hw + cab_pad)),
                rotate((hl, -hw + cab_pad)),
                rotate((hl, hw - cab_pad)),
                rotate((hl - cab_len, hw - cab_pad)),
            ]

            pygame.draw.polygon(self.screen, (220, 220, 220), pts)
            pygame.draw.polygon(self.screen, (50, 150, 255), cab_pts)
            pygame.draw.lines(self.screen, (30, 30, 30), True, pts, 2)

            train_id = self.render_scaled_text(f"{train.id}", (255, 255, 255))
            id_rect = train_id.get_rect()
            id_rect.center = (sx, sy - 20 * self.camera.zoom)
            self.screen.blit(train_id, id_rect)

    # -------------------------------------------------

    def draw_connections(self):

        for block in self.network.get_blocks():

            key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)

            if key not in self.layout.block_positions:
                continue

            bx, by = self.layout.block_positions[key]

            pair_key = tuple(sorted([block.station_a, block.station_b]))
            total_blocks = getattr(self.layout, "block_counts", {}).get(pair_key, 1)

            if total_blocks <= 2:
                color = (0, 200, 200) if block.branch_id == 0 else (200, 0, 120)
            else:
                if block.branch_id == 0:
                    color = (0, 200, 200)
                elif block.branch_id == total_blocks - 1:
                    color = (200, 0, 120)
                else:
                    color = (255, 128, 0)  # Orange

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
                screen_points = [
                    self.camera.world_to_screen(px, py) for px, py in curve_points
                ]

                if len(screen_points) >= 2:
                    line_w = max(1, int(3 * self.camera.zoom))
                    pygame.draw.lines(self.screen, color, False, screen_points, line_w)

    def draw_ui(self, simulation):
        from datetime import timedelta

        time_font = pygame.font.SysFont("Arial", 30)
        symbol_font = pygame.font.SysFont("Arial", 42, bold=True)

        current_time_dt = simulation.schedule.start_time + timedelta(
            seconds=simulation.sim_time
        )
        time_str = current_time_dt.strftime("%Y-%m-%d %H:%M")

        time_surface = time_font.render(time_str, True, (0, 255, 0))
        time_rect = time_surface.get_rect()
        time_rect.center = (self.width // 2, 30)
        self.screen.blit(time_surface, time_rect)

        is_paused = getattr(simulation, "is_paused", False)
        color = (100, 200, 100) if is_paused else (200, 200, 100)
        text = "PLAY" if is_paused else "PAUSE"

        pygame.draw.rect(self.screen, color, self.btn_rect, border_radius=5)

        msg = time_font.render(text, True, (255, 255, 255))
        msg_rect = msg.get_rect(center=self.btn_rect.center)
        self.screen.blit(msg, msg_rect)

        # Speed Dial
        speed = getattr(simulation, "speed", 1.0)

        btn_color = (100, 120, 140)
        txt_bg_color = (60, 70, 80)

        # Minus button
        pygame.draw.rect(self.screen, btn_color, self.speed_minus_rect, border_radius=5)
        minus_msg = symbol_font.render("-", True, (255, 255, 255))
        minus_rect = minus_msg.get_rect(
            center=(self.speed_minus_rect.centerx, self.speed_minus_rect.centery - 2)
        )
        self.screen.blit(minus_msg, minus_rect)

        # Text block
        pygame.draw.rect(
            self.screen, txt_bg_color, self.speed_text_rect, border_radius=5
        )
        text_str = f"Speed: {speed:g}"
        speed_msg = time_font.render(text_str, True, (255, 255, 255))
        speed_rect = speed_msg.get_rect(center=self.speed_text_rect.center)
        self.screen.blit(speed_msg, speed_rect)

        # Plus button
        pygame.draw.rect(self.screen, btn_color, self.speed_plus_rect, border_radius=5)
        plus_msg = symbol_font.render("+", True, (255, 255, 255))
        plus_rect = plus_msg.get_rect(
            center=(self.speed_plus_rect.centerx, self.speed_plus_rect.centery - 2)
        )
        self.screen.blit(plus_msg, plus_rect)

        # Exit Button
        pygame.draw.rect(
            self.screen, (200, 50, 50), self.exit_btn_rect, border_radius=5
        )
        exit_msg = time_font.render("EXIT", True, (255, 255, 255))
        exit_msg_rect = exit_msg.get_rect(center=self.exit_btn_rect.center)
        self.screen.blit(exit_msg, exit_msg_rect)

    def clamp_camera(self):
        if hasattr(self.layout, "bounds") and self.layout.bounds["min_x"] != float(
            "inf"
        ):
            b = self.layout.bounds

            half_w = (self.width / 2) / self.camera.zoom
            half_h = (self.height / 2) / self.camera.zoom

            min_cam_x = b["min_x"] - half_w
            max_cam_x = b["max_x"] - half_w

            min_cam_y = b["min_y"] - half_h
            max_cam_y = b["max_y"] - half_h

            if min_cam_x > max_cam_x:
                min_cam_x = max_cam_x = (min_cam_x + max_cam_x) / 2

            if min_cam_y > max_cam_y:
                min_cam_y = max_cam_y = (min_cam_y + max_cam_y) / 2

            self.camera.x = max(min_cam_x, min(max_cam_x, self.camera.x))
            self.camera.y = max(min_cam_y, min(max_cam_y, self.camera.y))

    def draw(self, simulation):
        self.clamp_camera()

        self.screen.fill((30, 30, 30))
        self.draw_connections()

        for station in self.network.stations:
            self.draw_station(station)

        self.draw_blocks()

        trains = simulation.get_active_trains()

        self.draw_trains(trains)

        self.draw_ui(simulation)
