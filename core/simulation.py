from core.pathing import build_path


class Segment:
    def __init__(self, start_stop, end_stop, network, layout):

        self.start_station = start_stop.station
        self.end_station = end_stop.station

        self.start_track = start_stop.track
        self.end_track = end_stop.track

        self.departure = start_stop.departure
        self.arrival = end_stop.arrival

        self.block = self.find_block(network)

        if self.block is None:
            raise Exception(
                f"No valid block for {self.start_station}:{self.start_track} "
                f"→ {self.end_station}:{self.end_track}"
            )

        self.path = build_path(
            layout,
            self.block,
            self.start_station,
            self.start_track,
            self.end_station,
            self.end_track,
        )

    def duration(self):
        return self.arrival - self.departure

    def find_block(self, network):

        for block in network.get_blocks():

            if {block.station_a, block.station_b} != {
                self.start_station,
                self.end_station,
            }:
                continue

            has_start = False
            has_end = False

            for st, tr in block.connections:

                if st == self.start_station and tr == self.start_track:
                    has_start = True

                if st == self.end_station and tr == self.end_track:
                    has_end = True

            if has_start and has_end:
                return block

        return None


class SimTrain:
    def __init__(self, train, network, layout):

        self.id = train.id
        self.direction = train.direction

        self.segments = []

        for i in range(len(train.stops) - 1):
            self.segments.append(
                Segment(train.stops[i], train.stops[i + 1], network, layout)
            )

        self.current_segment_index = 0
        self.finished = False

        if self.segments:
            self.x, self.y, self.angle = self.segments[0].path.get_position(0)
        else:
            self.x = 0
            self.y = 0
            self.angle = 0

    def get_current_segment(self):
        if self.current_segment_index >= len(self.segments):
            return None
        return self.segments[self.current_segment_index]


class Simulation:
    def __init__(self, network, schedule, layout):

        self.network = network
        self.schedule = schedule
        self.layout = layout

        self.sim_time = 0
        self.is_paused = False

        self.trains = []

        for train in schedule.get_trains():
            self.trains.append(SimTrain(train, network, layout))

    def update(self, dt):
        if self.is_paused:
            return

        self.sim_time += dt

        for train in self.trains:
            self.update_train(train)



    def update_train(self, train):

        segment = train.get_current_segment()

        if segment is None:
            train.finished = True
            return

        if self.sim_time < segment.departure:
            return

        duration = segment.duration()

        progress = (
            1.0 if duration <= 0 else (self.sim_time - segment.departure) / duration
        )
        progress = max(0.0, min(1.0, progress))

        x, y, angle = segment.path.get_position(progress)

        train.x = x
        train.y = y
        train.angle = angle

        if progress >= 1.0:
            train.current_segment_index += 1

            if train.current_segment_index >= len(train.segments):
                train.finished = True

    def get_active_trains(self):
        return self.trains
