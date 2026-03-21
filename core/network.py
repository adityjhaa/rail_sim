import json
from collections import defaultdict


class Track:
    def __init__(self, track_id, platform):
        self.id = track_id
        self.platform = platform

    def __repr__(self):
        return f"Track({self.id}, PF={self.platform})"


class Station:
    def __init__(self, name):
        self.name = name
        self.tracks = {}

    def add_track(self, track_id, platform):
        self.tracks[track_id] = Track(track_id, platform)

    def get_track(self, track_id):
        return self.tracks.get(track_id)

    def __repr__(self):
        return f"Station({self.name})"


class BlockSection:
    """
    Represents the section between two stations.
    Each section can have multiple lines (up/down).
    """

    def __init__(self, station_a, station_b, branch_id):
        self.station_a = station_a
        self.station_b = station_b
        self.branch_id = branch_id
        self.connections = []  # (station, track)

    def add_connection(self, station, track):
        self.connections.append((station, track))

    def __repr__(self):
        return f"Block({self.station_a}-{self.station_b}, branch={self.branch_id})"


class Network:
    """
    Main network object used by the simulator.
    """

    def __init__(self):
        self.stations = {}
        self.blocks = []
        self.block_lookup = {}

    def add_station(self, station):
        self.stations[station.name] = station

    def get_station(self, name):
        return self.stations.get(name)

    def get_stations(self):
        return list(self.stations.values())

    def get_or_create_block(self, station_a, station_b, branch):

        key = (station_a, station_b, branch)

        if key not in self.block_lookup:
            block = BlockSection(station_a, station_b, branch)
            self.block_lookup[key] = block
            self.blocks.append(block)

        return self.block_lookup[key]

    def get_blocks(self):
        return self.blocks


def load_network(json_file):
    """
    Reads network.json and returns a Network object
    """

    with open(json_file) as f:
        data = json.load(f)

    network = Network()

    for station_name, station_data in data.items():

        station = Station(station_name)

        for track_id, platform in station_data["tracks"].items():
            station.add_track(track_id, platform)

        network.add_station(station)

    for station_name, station_data in data.items():

        for conn_key, branch in station_data["connections"].items():

            src, dst, branch_id, track_id = conn_key.split("_")
            branch_id = int(branch_id)

            block = network.get_or_create_block(src, dst, branch_id)

            # register connection from this station
            block.add_connection(station_name, track_id)

    return network
