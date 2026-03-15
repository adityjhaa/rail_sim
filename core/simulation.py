class Segment:
    """
    Represents movement between two stations.
    """

    def __init__(self, start_stop, end_stop):
        self.start_station = start_stop.station
        self.end_station = end_stop.station

        self.departure = start_stop.departure
        self.arrival = end_stop.arrival

        self.start_track = start_stop.track
        self.end_track = end_stop.track

    def duration(self):
        return self.arrival - self.departure


class SimTrain:
    """
    Runtime train object used by the simulator.
    """

    def __init__(self, train):

        self.id = train.id
        self.direction = train.direction

        self.segments = []

        for i in range(len(train.stops) - 1):
            self.segments.append(Segment(train.stops[i], train.stops[i + 1]))

        self.current_segment_index = 0

        self.x = 0
        self.y = 0

        self.finished = False

    def get_current_segment(self):

        if self.current_segment_index >= len(self.segments):
            return None

        return self.segments[self.current_segment_index]


class Simulation:
    """
    Main simulation engine.
    """

    def __init__(self, network, schedule):

        self.network = network
        self.schedule = schedule

        self.sim_time = 0

        self.trains = []
        self.active_trains = []

        for train in schedule.get_trains():
            self.trains.append(SimTrain(train))

    def update(self, dt):
        """
        Advance simulation time.
        """

        self.sim_time += dt

        self.spawn_trains()

        for train in self.active_trains:
            self.update_train(train)

    def spawn_trains(self):

        for train in self.trains:

            if train in self.active_trains:
                continue

            first_segment = train.segments[0]

            if self.sim_time >= first_segment.departure:
                self.active_trains.append(train)

    def update_train(self, train):

        segment = train.get_current_segment()

        if segment is None:
            train.finished = True
            return

        if self.sim_time < segment.departure:
            return

        duration = segment.duration()

        if duration <= 0:
            progress = 1
        else:
            progress = (self.sim_time - segment.departure) / duration

        if progress >= 1:

            train.current_segment_index += 1

            if train.current_segment_index >= len(train.segments):
                train.finished = True

            return

        start_pos = self.get_station_position(segment.start_station)
        end_pos = self.get_station_position(segment.end_station)

        train.x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        train.y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress

    def get_station_position(self, station_name):
        """
        Placeholder.
        The renderer or layout module will provide real coordinates.
        """

        index = list(self.network.stations.keys()).index(station_name)

        x = 200 + index * 400
        y = 300

        return (x, y)

    def get_active_trains(self):

        return [t for t in self.active_trains if not t.finished]
