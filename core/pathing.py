class PathSegment:
    def __init__(self, points):
        self.points = points

    def get_position(self, t):
        if not self.points:
            return (0, 0)

        if len(self.points) == 1:
            return self.points[0]

        t = max(0.0, min(1.0, t))

        total_segments = len(self.points) - 1
        seg_float = t * total_segments
        seg_idx = int(seg_float)

        if seg_idx >= total_segments:
            return self.points[-1]

        local_t = seg_float - seg_idx

        x1, y1 = self.points[seg_idx]
        x2, y2 = self.points[seg_idx + 1]

        x = x1 + (x2 - x1) * local_t
        y = y1 + (y2 - y1) * local_t

        return (x, y)


def get_connection_point(layout, station, track, block):
    tx, ty = layout.track_positions[station][track]

    key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)
    bx, by = layout.block_positions[key]

    # midpoint toward block (matches renderer direction)
    cx = tx + (bx - tx) * 0.5
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

    points = [
        (sx, sy),   # start track
        entry,      # switch entry
        (bx, by),   # block
        exit,       # switch exit
        (ex, ey)    # end track
    ]

    return PathSegment(points)