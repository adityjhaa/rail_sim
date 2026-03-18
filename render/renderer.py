import pygame


class Camera:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.zoom = 1

    def world_to_screen(self, x, y):

        sx = (x - self.x) * self.zoom
        sy = (y - self.y) * self.zoom

        return sx, sy


class Renderer:

    def __init__(self, network, layout):

        self.network = network
        self.layout = layout

        pygame.init()

        pygame.display.set_caption("Railway Simulator")

        self.screen = pygame.display.set_mode((1400, 800))

        self.font = pygame.font.SysFont(None, 20)

        self.camera = Camera()

    # -------------------------------------------------

    def draw_station(self, station):

        x = self.layout.station_positions[station]

        tracks = self.layout.track_positions[station]
        station_obj = self.network.get_station(station)

        for track_id, (tx, ty) in tracks.items():

            sx, sy = self.camera.world_to_screen(tx, ty)

            # draw track
            pygame.draw.line(
                self.screen, (0, 120, 255), (sx - 40, sy), (sx + 40, sy), 4
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
            pygame.draw.line(self.screen, color, (sx - 60, sy), (sx + 60, sy), 4)

            # draw label
            label = self.font.render(
                f"BSN_{block.branch_id + 1}", True, (255, 255, 255)
            )

            self.screen.blit(label, (sx - 25, sy - 20))

    # -------------------------------------------------

    def draw_trains(self, trains):

        for train in trains:

            sx, sy = self.camera.world_to_screen(train.x, train.y)

            rect = pygame.Rect(sx - 8, sy - 5, 16, 10)

            pygame.draw.rect(self.screen, (255, 80, 80), rect)

    # -------------------------------------------------

    def draw_connections(self):

        for block in self.network.get_blocks():

            key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)

            if key not in self.layout.block_positions:
                continue

            bx, by = self.layout.block_positions[key]
            bx, by = self.camera.world_to_screen(bx, by)

            color = (0, 200, 200) if block.branch_id == 0 else (200, 0, 120)

            for station, track in block.connections:

                tx, ty = self.layout.track_positions[station][track]
                tx, ty = self.camera.world_to_screen(tx, ty)

                station_x = self.layout.station_positions[station]

                if station_x < bx:
                    start = (tx + 40, ty)
                    end = (bx - 60, by)
                else:
                    start = (tx - 40, ty)
                    end = (bx + 60, by)

                pygame.draw.line(self.screen, color, start, end, 3)

    def draw(self, simulation):

        self.screen.fill((30, 30, 30))
        self.draw_connections()

        for station in self.network.stations:
            self.draw_station(station)

        self.draw_blocks()


        trains = simulation.get_active_trains()

        self.draw_trains(trains)

        pygame.display.flip()
