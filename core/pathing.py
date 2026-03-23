import math


class PathSegment:
    def __init__(self, points):

        self.points = points
        self.lengths = []
        self.total_length = 0

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            length = math.hypot(x2 - x1, y2 - y1)

            self.lengths.append(length)
            self.total_length += length

    def get_position(self, t):

        if not self.points:
            return (0, 0)

        if len(self.points) == 1:
            return self.points[0]

        t = max(0.0, min(1.0, t))

        target_dist = t * self.total_length
        current_dist = 0

        for i in range(len(self.lengths)):

            seg_len = self.lengths[i]

            if current_dist + seg_len >= target_dist:

                local = (target_dist - current_dist) / seg_len if seg_len > 0 else 0

                x1, y1 = self.points[i]
                x2, y2 = self.points[i + 1]

                x = x1 + (x2 - x1) * local
                y = y1 + (y2 - y1) * local

                return (x, y)

            current_dist += seg_len

        return self.points[-1]


def get_connection_point(layout, station, track, block):

    tx, ty = layout.track_positions[station][track]

    key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)
    bx, by = layout.block_positions[key]

    if layout.station_positions[station] < bx:
        cx = tx + abs(bx - tx) * 0.5
    else:
        cx = tx - abs(bx - tx) * 0.5

    cy = ty

    return (cx, cy)


def build_path(layout, block, start_station, start_track, end_station, end_track):

    if block is None:
        raise Exception(f"No block for {start_station}->{end_station}")

    sx, sy = layout.track_positions[start_station][start_track]
    ex, ey = layout.track_positions[end_station][end_track]

    key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)
    bx, by = layout.block_positions[key]

    entry = get_connection_point(layout, start_station, start_track, block)
    exit = get_connection_point(layout, end_station, end_track, block)

    moving_right = ex > sx

    if moving_right:
        points = [(sx, sy), entry, (bx - 60, by), (bx + 60, by), exit, (ex, ey)]
    else:
        points = [(sx, sy), entry, (bx + 60, by), (bx - 60, by), exit, (ex, ey)]

    return PathSegment(points)
