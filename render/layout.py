class Layout:

    def __init__(self, network):

        self.network = network

        self.station_positions = {}
        self.track_positions = {}
        self.block_positions = {}

        self.station_spacing = 400
        self.track_spacing = 60

        self.compute_layout()

    def compute_layout(self):

        stations = list(self.network.stations.keys())

        for i, station in enumerate(stations):

            x = 200 + i * self.station_spacing
            self.station_positions[station] = x

            tracks = self.network.stations[station].tracks

            self.track_positions[station] = {}

            for j, track_id in enumerate(tracks):

                y = 200 + j * self.track_spacing
                self.track_positions[station][track_id] = (x, y)

        # block sections

        for block in self.network.get_blocks():

            s1 = block.station_a
            s2 = block.station_b

            key = tuple(sorted([s1, s2])) + (block.branch_id,)

            x1 = self.station_positions[s1]
            x2 = self.station_positions[s2]

            mid_x = (x1 + x2) / 2

            y = 300 if block.branch_id == 0 else 360

            self.block_positions[key] = (mid_x, y)
