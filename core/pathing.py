class PathSegment:
    def __init__(self, points):
        self.points = points

    def get_position(self, t):
        """
        t: 0 → 1
        """
        total = len(self.points) - 1
        if total <= 0:
            return self.points[0]

        seg = int(t * total)
        seg = min(seg, total - 1)

        local_t = (t * total) - seg

        x1, y1 = self.points[seg]
        x2, y2 = self.points[seg + 1]

        x = x1 + (x2 - x1) * local_t
        y = y1 + (y2 - y1) * local_t

        return x, y


def build_path(layout, block, start_station, start_track, end_station, end_track):

    # station positions
    sx, sy = layout.track_positions[start_station][start_track]
    ex, ey = layout.track_positions[end_station][end_track]

    key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)
    bx, by = layout.block_positions[key]

    # determine entry/exit points
    if layout.station_positions[start_station] < bx:
        entry = (bx - 60, by)
    else:
        entry = (bx + 60, by)

    if layout.station_positions[end_station] < bx:
        exit = (bx - 60, by)
    else:
        exit = (bx + 60, by)

    points = [
        (sx, sy),  # station track
        entry,  # switch entry
        (bx, by),  # block center
        exit,  # switch exit
        (ex, ey),  # destination track
    ]

    return PathSegment(points)
