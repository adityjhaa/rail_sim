class Layout:

    def __init__(self, network):

        self.network = network

        self.station_positions = {}
        self.track_positions = {}
        self.block_positions = {}
        self.block_counts = {}

        self.station_spacing = 400
        self.track_spacing = 60

        self.bounds = {
            "min_x": float("inf"),
            "max_x": float("-inf"),
            "min_y": float("inf"),
            "max_y": float("-inf"),
        }

        self.compute_layout()

    def compute_layout(self):

        common_y = 400

        stations = list(self.network.stations.keys())

        for i, station in enumerate(stations):

            x = 200 + i * self.station_spacing
            self.station_positions[station] = x

            tracks = self.network.stations[station].tracks
            self.track_positions[station] = {}

            n_tracks = len(tracks)
            if n_tracks > 0:
                start_y = common_y - (n_tracks - 1) * self.track_spacing / 2
            else:
                start_y = common_y

            for j, track_id in enumerate(tracks):

                y = start_y + j * self.track_spacing
                self.track_positions[station][track_id] = (x, y)
                self.bounds["min_x"] = min(self.bounds["min_x"], x)
                self.bounds["max_x"] = max(self.bounds["max_x"], x)
                self.bounds["min_y"] = min(self.bounds["min_y"], y)
                self.bounds["max_y"] = max(self.bounds["max_y"], y)

        # block sections
        pair_to_blocks = {}
        for block in self.network.get_blocks():
            s1 = block.station_a
            s2 = block.station_b
            pair_key = tuple(sorted([s1, s2]))
            if pair_key not in pair_to_blocks:
                pair_to_blocks[pair_key] = []
            pair_to_blocks[pair_key].append(block)

        for pair_key, blocks in pair_to_blocks.items():
            s1, s2 = pair_key
            x1 = self.station_positions[s1]
            x2 = self.station_positions[s2]

            mid_x = (x1 + x2) / 2
            num_blocks = len(blocks)
            self.block_counts[pair_key] = num_blocks

            def get_visual_order(b):
                if b.branch_id == 0:
                    return 0
                elif b.branch_id == 1:
                    return float('inf')
                else:
                    return b.branch_id

            blocks.sort(key=get_visual_order)

            # Since everything is centered on common_y
            start_y = common_y - (num_blocks - 1) * self.track_spacing / 2

            for i, block in enumerate(blocks):
                y = start_y + i * self.track_spacing
                key = pair_key + (block.branch_id,)
                self.block_positions[key] = (mid_x, y)
                self.bounds["min_x"] = min(self.bounds["min_x"], mid_x)
                self.bounds["max_x"] = max(self.bounds["max_x"], mid_x)
                self.bounds["min_y"] = min(self.bounds["min_y"], y)
                self.bounds["max_y"] = max(self.bounds["max_y"], y)
