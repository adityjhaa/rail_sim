import json


class Stop:
    """
    Represents a single stop in a train route.
    """

    def __init__(self, station, track, platform, arrival, departure):
        self.station = station
        self.track = track
        self.platform = platform
        self.arrival = arrival
        self.departure = departure

    def is_pass_through(self):
        return self.arrival == self.departure

    def __repr__(self):
        return f"Stop({self.station}, {self.track}, arr={self.arrival}, dep={self.departure})"


class Train:
    """
    Represents a train and its route.
    """

    def __init__(self, train_id, direction):
        self.id = train_id
        self.direction = direction
        self.stops = []

    def add_stop(self, stop):
        self.stops.append(stop)

    def first_departure(self):
        if not self.stops:
            return None
        return self.stops[0].departure

    def last_arrival(self):
        if not self.stops:
            return None
        return self.stops[-1].arrival

    def __repr__(self):
        return f"Train({self.id}, stops={len(self.stops)})"


class Schedule:
    """
    Container for all trains.
    """

    def __init__(self):
        self.trains = []

    def add_train(self, train):
        self.trains.append(train)

    def get_trains(self):
        return self.trains

    def get_first_train_time(self):
        times = [
            t.first_departure() for t in self.trains if t.first_departure() is not None
        ]
        return min(times) if times else None

    def get_last_train_time(self):
        times = [t.last_arrival() for t in self.trains if t.last_arrival() is not None]
        return max(times) if times else None

    def get_trains_active_at(self, time):
        """
        Returns trains active at given simulation time.
        """
        active = []

        for train in self.trains:

            start = train.first_departure()
            end = train.last_arrival()

            if start is None or end is None:
                continue

            if start <= time <= end:
                active.append(train)

        return active


def load_schedule(json_file):
    """
    Reads schedule.json and returns a Schedule object.
    """

    with open(json_file) as f:
        data = json.load(f)

    schedule = Schedule()

    for train_data in data["trains"]:

        train = Train(train_data["train_id"], train_data["direction"])

        for stop_data in train_data["route"]:

            stop = Stop(
                station=stop_data["station"],
                track=stop_data["line"],
                platform=stop_data["platform"],
                arrival=stop_data["arr"],
                departure=stop_data["dep"],
            )

            train.add_stop(stop)

        schedule.add_train(train)

    return schedule
