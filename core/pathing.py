import math

def cubic_bezier(p0, p1, p2, p3, num_points=20):
    points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    return points

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
            return (0, 0, 0)

        if len(self.points) == 1:
            return (*self.points[0], 0)

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
                
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

                return (x, y, angle)

            current_dist += seg_len

        # If we reach here, we're right at the end
        x1, y1 = self.points[-2]
        x2, y2 = self.points[-1]
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        return (*self.points[-1], angle)


def build_path(layout, block, start_station, start_track, end_station, end_track):

    if block is None:
        raise Exception(f"No block for {start_station}->{end_station}")

    sx, sy = layout.track_positions[start_station][start_track]
    ex, ey = layout.track_positions[end_station][end_track]

    key = tuple(sorted([block.station_a, block.station_b])) + (block.branch_id,)
    bx, by = layout.block_positions[key]

    moving_right = ex > sx

    points = []

    if moving_right:
        entry_x = bx - 60
        entry_y = by
        station_exit_x = sx + 40
        c_len = abs(entry_x - station_exit_x) * 0.5
        
        points.append((sx, sy))
        points.extend(cubic_bezier((station_exit_x, sy), (station_exit_x + c_len, sy), (entry_x - c_len, entry_y), (entry_x, entry_y)))
        
        exit_x = bx + 60
        exit_y = by
        points.append((exit_x, exit_y))
        
        station_entry_x = ex - 40
        c_len2 = abs(station_entry_x - exit_x) * 0.5
        points.extend(cubic_bezier((exit_x, exit_y), (exit_x + c_len2, exit_y), (station_entry_x - c_len2, ey), (station_entry_x, ey))[1:])
        points.append((ex, ey))
    else:
        entry_x = bx + 60
        entry_y = by
        station_exit_x = sx - 40
        c_len = abs(entry_x - station_exit_x) * 0.5
        
        points.append((sx, sy))
        points.extend(cubic_bezier((station_exit_x, sy), (station_exit_x - c_len, sy), (entry_x + c_len, entry_y), (entry_x, entry_y)))
        
        exit_x = bx - 60
        exit_y = by
        points.append((exit_x, exit_y))
        
        station_entry_x = ex + 40
        c_len2 = abs(station_entry_x - exit_x) * 0.5
        points.extend(cubic_bezier((exit_x, exit_y), (exit_x - c_len2, exit_y), (station_entry_x + c_len2, ey), (station_entry_x, ey))[1:])
        points.append((ex, ey))

    return PathSegment(points)
