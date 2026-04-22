import pandas as pd

station_dict = {
    "pun": {
        "tracks": {"s1": 1, "s2": 2, "s3": 0, "s4": 3},
        "connections": {
            "pun_nwp_0_s1": 0,
            "pun_nwp_0_s2": 0,
            "pun_nwp_1_s1": 1,
            "pun_nwp_1_s3": 1,
            "pun_nwp_1_s4": 1,
        },
    },
    "nwp": {
        "tracks": {"s1": 1, "s2": 0, "s3": 3, "s4": 4, "s5": 0},
        "connections": {
            "pun_nwp_0_s1": 0,
            "pun_nwp_0_s2": 0,
            "pun_nwp_0_s3": 0,
            "nwp_kbm_0_s2": 0,
            "nwp_kbm_0_s3": 0,
            "pun_nwp_1_s2": 1,
            "pun_nwp_1_s4": 1,
            "pun_nwp_1_s5": 1,
            "nwp_kbm_1_s2": 1,
            "nwp_kbm_1_s4": 1,
            "nwp_kbm_1_s5": 1,
        },
    },
    "kbm": {
        "tracks": {"s1": 1, "s2": 0, "s3": 2, "s4": 3},
        "connections": {
            "nwp_kbm_0_s1": 0,
            "nwp_kbm_0_s2": 0,
            "kbm_tiu_0_s1": 0,
            "kbm_tiu_0_s2": 0,
            "nwp_kbm_1_s1": 1,
            "nwp_kbm_1_s3": 1,
            "nwp_kbm_1_s4": 1,
            "kbm_tiu_1_s1": 1,
            "kbm_tiu_1_s3": 1,
            "kbm_tiu_1_s4": 1,
        },
    },
    "tiu": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 4},
        "connections": {
            "kbm_tiu_0_s1": 0,
            "kbm_tiu_0_s2": 0,
            "tiu_ulm_0_s1": 0,
            "tiu_ulm_0_s2": 0,
            "kbm_tiu_1_s1": 1,
            "kbm_tiu_1_s3": 1,
            "kbm_tiu_1_s4": 1,
            "tiu_ulm_1_s1": 1,
            "tiu_ulm_1_s3": 1,
            "tiu_ulm_1_s4": 1,
        },
    },
    "ulm": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 4},
        "connections": {
            "tiu_ulm_0_s1": 0,
            "tiu_ulm_0_s2": 0,
            "ulm_che_0_s1": 0,
            "ulm_che_0_s2": 0,
            "tiu_ulm_1_s1": 1,
            "tiu_ulm_1_s3": 1,
            "tiu_ulm_1_s4": 1,
            "ulm_che_1_s1": 1,
            "ulm_che_1_s3": 1,
            "ulm_che_1_s4": 1,
        },
    },
    "che": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 4, "s5": 0},
        "connections": {
            "ulm_che_0_s1": 0,
            "ulm_che_0_s2": 0,
            "ulm_che_0_s4": 0,
            "ulm_che_0_s5": 0,
            "che_dusi_0_s1": 0,
            "che_dusi_0_s2": 0,
            "che_dusi_0_s4": 0,
            "che_dusi_0_s5": 0,
            "ulm_che_1_s3": 1,
            "ulm_che_1_s4": 1,
            "ulm_che_1_s5": 1,
            "che_dusi_1_s3": 1,
            "che_dusi_1_s4": 1,
            "che_dusi_1_s5": 1,
        },
    },
    "dusi": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 0},
        "connections": {
            "che_dusi_0_s1": 0,
            "che_dusi_0_s2": 0,
            "dusi_pdu_0_s1": 0,
            "dusi_pdu_0_s2": 0,
            "che_dusi_1_s3": 1,
            "che_dusi_1_s4": 1,
            "dusi_pdu_1_s3": 1,
            "dusi_pdu_1_s4": 1,
        },
    },
    "pdu": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 0},
        "connections": {
            "dusi_pdu_0_s1": 0,
            "dusi_pdu_0_s2": 0,
            "dusi_pdu_0_s3": 0,
            "pdu_sgdm_0_s1": 0,
            "pdu_sgdm_0_s2": 0,
            "pdu_sgdm_0_s3": 0,
            "dusi_pdu_1_s1": 1,
            "dusi_pdu_1_s2": 1,
            "dusi_pdu_1_s4": 1,
            "pdu_sgdm_1_s1": 1,
            "pdu_sgdm_1_s2": 1,
            "pdu_sgdm_1_s4": 1,
        },
    },
    "sgdm": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 4},
        "connections": {
            "pdu_sgdm_0_s1": 0,
            "pdu_sgdm_0_s2": 0,
            "pdu_sgdm_0_s3": 0,
            "sgdm_cpp_0_s1": 0,
            "sgdm_cpp_0_s2": 0,
            "sgdm_cpp_0_s3": 0,
            "pdu_sgdm_1_s3": 1,
            "pdu_sgdm_1_s4": 1,
            "sgdm_cpp_1_s3": 1,
            "sgdm_cpp_1_s4": 1,
        },
    },
    "cpp": {
        "tracks": {"s1": 1, "s2": 0, "s3": 2, "s4": 3, "s5": 0},
        "connections": {
            "sgdm_cpp_0_s1": 0,
            "sgdm_cpp_0_s2": 0,
            "cpp_gvi_0_s1": 0,
            "sgdm_cpp_0_s4": 0,
            "cpp_gvi_0_s2": 0,
            "cpp_gvi_0_s4": 0,
            "sgdm_cpp_1_s2": 1,
            "sgdm_cpp_1_s3": 1,
            "sgdm_cpp_1_s4": 1,
            "sgdm_cpp_1_s5": 1,
            "cpp_gvi_1_s3": 1,
            "cpp_gvi_1_s4": 1,
            "cpp_gvi_1_s5": 1,
        },
    },
    "gvi": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 4},
        "connections": {
            "cpp_gvi_0_s1": 0,
            "cpp_gvi_0_s2": 0,
            "cpp_gvi_0_s4": 0,
            "gvi_nml_0_s1": 0,
            "gvi_nml_0_s2": 0,
            "gvi_nml_0_s4": 0,
            "cpp_gvi_1_s3": 1,
            "cpp_gvi_1_s4": 1,
            "gvi_nml_1_s3": 1,
            "gvi_nml_1_s4": 1,
        },
    },
    "nml": {
        "tracks": {"s1": 1, "s2": 0, "s3": 2},
        "connections": {
            "gvi_nml_0_s1": 0,
            "gvi_nml_0_s3": 0,
            "nml_vzm_0_s1": 0,
            "nml_vzm_0_s3": 0,
            "gvi_nml_1_s2": 1,
            "gvi_nml_1_s3": 1,
            "nml_vzm_1_s2": 1,
            "nml_vzm_1_s3": 1,
        },
    },
    "vzm": {
        "tracks": {
            "s1": 1,
            "s2": 2,
            "s3": 3,
            "s4": 4,
            "s5": 5,
            "s6": 0,
            "s7": 0,
            "s8": 0,
            "s9": 0,
        },
        "connections": {
            "nml_vzm_0_s1": 0,
            "nml_vzm_0_s2": 0,
            "nml_vzm_0_s3": 0,
            "nml_vzm_0_s4": 0,
            "nml_vzm_0_s5": 0,
            "nml_vzm_0_s6": 0,
            "nml_vzm_0_s8": 0,
            "nml_vzm_0_s9": 0,
            "vzm_kuk_0_s1": 0,
            "vzm_kuk_0_s2": 0,
            "vzm_kuk_0_s3": 0,
            "vzm_kuk_0_s4": 0,
            "vzm_kuk_0_s5": 0,
            "vzm_kuk_0_s6": 0,
            "vzm_kuk_0_s8": 0,
            "vzm_kuk_0_s9": 0,
            "nml_vzm_1_s1": 1,
            "nml_vzm_1_s2": 1,
            "nml_vzm_1_s3": 1,
            "nml_vzm_1_s4": 1,
            "nml_vzm_1_s5": 1,
            "nml_vzm_1_s7": 1,
            "nml_vzm_1_s8": 1,
            "nml_vzm_1_s9": 1,
            "vzm_kuk_1_s1": 1,
            "vzm_kuk_1_s2": 1,
            "vzm_kuk_1_s3": 1,
            "vzm_kuk_1_s4": 1,
            "vzm_kuk_1_s5": 1,
            "vzm_kuk_1_s7": 1,
            "vzm_kuk_1_s8": 1,
            "vzm_kuk_1_s9": 1,
            "vzm_kuk_2_s1": 2,
            "vzm_kuk_2_s2": 2,
            "vzm_kuk_2_s3": 2,
            "vzm_kuk_2_s4": 2,
            "vzm_kuk_2_s5": 2,
            "vzm_kuk_2_s6": 2,
            "vzm_kuk_2_s7": 2,
            "vzm_kuk_2_s8": 2,
            "vzm_kuk_2_s9": 2,
        },
    },
    "kuk": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 4, "s5": 5},
        "connections": {
            "vzm_kuk_0_s1": 0,
            "vzm_kuk_0_s2": 0,
            "kuk_alm_0_s1": 0,
            "kuk_alm_0_s2": 0,
            "kuk_alm_0_s3": 0,
            "vzm_kuk_1_s2": 1,
            "vzm_kuk_1_s3": 1,
            "vzm_kuk_1_s4": 1,
            "vzm_kuk_1_s5": 1,
            "kuk_alm_1_s2": 1,
            "kuk_alm_1_s3": 1,
            "kuk_alm_1_s4": 1,
            "kuk_alm_1_s5": 1,
            "vzm_kuk_2_s2": 2,
            "vzm_kuk_2_s3": 2,
            "kuk_alm_2_s2": 2,
            "kuk_alm_2_s3": 2,
        },
    },
    "alm": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 4, "s5": 5},
        "connections": {
            "kuk_alm_0_s1": 0,
            "kuk_alm_0_s2": 0,
            "kuk_alm_0_s3": 0,
            "kuk_alm_0_s5": 0,
            "alm_kpl_0_s1": 0,
            "alm_kpl_0_s2": 0,
            "alm_kpl_0_s3": 0,
            "kuk_alm_1_s3": 1,
            "kuk_alm_1_s4": 1,
            "kuk_alm_1_s5": 1,
            "alm_kpl_1_s3": 1,
            "alm_kpl_1_s4": 1,
            "alm_kpl_1_s5": 1,
            "kuk_alm_2_s2": 2,
            "kuk_alm_2_s3": 2,
            "kuk_alm_2_s4": 2,
            "kuk_alm_2_s5": 2,
            "alm_kpl_2_s2": 2,
            "alm_kpl_2_s3": 2,
            "alm_kpl_2_s4": 2,
            "alm_kpl_2_s5": 2,
        },
    },
    "kpl": {
        "tracks": {"s1": 1, "s2": 2, "s3": 3, "s4": 4, "s5": 5, "s6": 0},
        "connections": {
            "alm_kpl_0_s1": 0,
            "alm_kpl_0_s2": 0,
            "alm_kpl_0_s3": 0,
            "alm_kpl_0_s5": 0,
            "alm_kpl_0_s6": 0,
            "kpl_ktv_0_s1": 0,
            "kpl_ktv_0_s2": 0,
            "kpl_ktv_0_s3": 0,
            "kpl_ktv_0_s6": 0,
            "alm_kpl_1_s3": 1,
            "alm_kpl_1_s4": 1,
            "alm_kpl_1_s5": 1,
            "alm_kpl_1_s6": 1,
            "kpl_ktv_1_s3": 1,
            "kpl_ktv_1_s4": 1,
            "kpl_ktv_1_s5": 1,
            "kpl_ktv_1_s6": 1,
            "alm_kpl_2_s2": 2,
            "alm_kpl_2_s3": 2,
            "alm_kpl_2_s4": 2,
            "alm_kpl_2_s5": 2,
            "alm_kpl_2_s6": 2,
            "kpl_ktv_2_s1": 2,
            "kpl_ktv_2_s2": 2,
            "kpl_ktv_2_s3": 2,
            "kpl_ktv_2_s4": 2,
            "kpl_ktv_2_s5": 2,
            "kpl_ktv_2_s6": 2,
        },
    },
    "ktv": {
        "tracks": {
            "s1": 1,
            "s2": 2,
            "s3": 3,
            "s4": 4,
            "s5": 5,
            "s6": 0,
            "s7": 0,
            "s8": 0,
            "s9": 6,
        },
        "connections": {
            "kpl_ktv_0_s1": 0,
            "kpl_ktv_0_s2": 0,
            "kpl_ktv_0_s3": 0,
            "kpl_ktv_0_s4": 0,
            "kpl_ktv_0_s5": 0,
            "kpl_ktv_0_s6": 0,
            "kpl_ktv_0_s7": 0,
            "kpl_ktv_0_s8": 0,
            "kpl_ktv_0_s9": 0,
            "kpl_ktv_1_s1": 1,
            "kpl_ktv_1_s2": 1,
            "kpl_ktv_1_s3": 1,
            "kpl_ktv_1_s6": 1,
            "kpl_ktv_1_s7": 1,
            "kpl_ktv_1_s8": 1,
            "kpl_ktv_1_s9": 1,
            "kpl_ktv_2_s1": 2,
            "kpl_ktv_2_s2": 2,
            "kpl_ktv_2_s3": 2,
            "kpl_ktv_2_s4": 2,
            "kpl_ktv_2_s5": 2,
            "kpl_ktv_2_s6": 2,
            "kpl_ktv_2_s7": 2,
            "kpl_ktv_2_s8": 2,
            "kpl_ktv_2_s9": 2,
        },
    },
}


# for automatic block signalling
# vzm and kuk are the stations and 'a' and 'b' are two dummy stations, so we get three sub-blocsections bet them

# e.g. : { 'vzm-a': {
#                       'tracks' : { 's1': 1 , 's2': 2  },
#                        'connections': { 'vzm_a_0_s1' : 0, 'a_b_0_s1' : 0,
#                                          'vzm_a_1_s2' : 1, 'a_b_1_s2' : 1}
# },

# 'a-b': {  'tracks' : { 's1': 0 , 's2': 0  },
#         'connections': { 'a_b_0_s1' : 0, 'b_kuk_0_s1' : 0,
#                         'a_b_1_s2' : 1, 'b_kuk_1_s2' : 1}
# },

# 'b-kuk': {  'tracks' : { 's1': 1 , 's2': 2  },
#         'connections': { 'b_kuk_0_s1' : 0, 'b_kuk_0_s1' : 0,
#                         'b_kuk_1_s2' : 1, 'b_kuk_1_s2' : 1}
#       }
# }


global station_list


def create_station_class(station_name, station_config):
    class DynamicStation:
        def __init__(self):
            self.name = station_name
            self.tracks = {}
            self.connections = {}

            for track_name, platform_num in station_config["tracks"].items():
                self.tracks[track_name] = [0, platform_num, 0, 0, pd.Timedelta(0), ""]

            for conn_name, direction in station_config["connections"].items():
                self.connections[conn_name] = [0, direction, ""]

        def set_occupancy_arr(self, stn_track_name, occ_start, occ_end, train_name):
            if stn_track_name in self.tracks:
                self.tracks[stn_track_name][0] = 1
                self.tracks[stn_track_name][2] = occ_start
                self.tracks[stn_track_name][3] = occ_end
                # self.tracks[stn_track_name][4] = occ_end - occ_start + self.tracks[stn_track_name][4]
                self.tracks[stn_track_name][5] = train_name
            else:
                print("\n Track is not found")

        def set_occupancy_dep(self, stn_track_name, t):
            if stn_track_name in self.tracks:
                self.tracks[stn_track_name][0] = 0
                self.tracks[stn_track_name][4] = (
                    t - self.tracks[stn_track_name][2] + self.tracks[stn_track_name][4]
                )
                self.tracks[stn_track_name][2] = pd.Timestamp("2100-06-01 22:52:00")
                self.tracks[stn_track_name][3] = pd.Timestamp("2100-06-01 22:52:00")
                self.tracks[stn_track_name][5] = ""
            else:
                print("\n Track is not found")

        def set_occ_conn_in(self, blsec_in_stn_track_name, train_name, status):
            self.connections[blsec_in_stn_track_name][0] = status
            self.connections[blsec_in_stn_track_name][2] = train_name

        def set_occ_conn_out(self, blsec_out_stn_track_name, train_name, status):
            self.connections[blsec_out_stn_track_name][0] = status
            self.connections[blsec_out_stn_track_name][2] = train_name

        # if station line is being occupied for longer duration, update the occupancy end time
        def set_occupancy_updt(self, stn_line_name, occ_end):
            self.tracks[stn_line_name][3] = occ_end

        def is_occupied(self, track_name):
            if self.tracks[track_name][0] == 1:
                a = track_name + " is occupied"
            else:
                a = track_name + " is not occupied"
            return a

    return DynamicStation()


pun = create_station_class("pun", station_dict["pun"])
nwp = create_station_class("nwp", station_dict["nwp"])
kbm = create_station_class("kbm", station_dict["kbm"])
tiu = create_station_class("tiu", station_dict["tiu"])
ulm = create_station_class("ulm", station_dict["ulm"])
che = create_station_class("che", station_dict["che"])
dusi = create_station_class("dusi", station_dict["dusi"])
pdu = create_station_class("pdu", station_dict["pdu"])
sgdm = create_station_class("sgdm", station_dict["sgdm"])
cpp = create_station_class("cpp", station_dict["cpp"])
gvi = create_station_class("gvi", station_dict["gvi"])
nml = create_station_class("nml", station_dict["nml"])
vzm = create_station_class("vzm", station_dict["vzm"])
kuk = create_station_class("kuk", station_dict["kuk"])
alm = create_station_class("alm", station_dict["alm"])
kpl = create_station_class("kpl", station_dict["kpl"])
ktv = create_station_class("ktv", station_dict["ktv"])

stations = [
    pun,
    nwp,
    kbm,
    tiu,
    ulm,
    che,
    dusi,
    pdu,
    sgdm,
    cpp,
    gvi,
    nml,
    vzm,
    kuk,
    alm,
    kpl,
    ktv,
]

stations_list = [
    "pun",
    "nwp",
    "kbm",
    "tiu",
    "ulm",
    "che",
    "dusi",
    "pdu",
    "sgdm",
    "cpp",
    "gvi",
    "nml",
    "vzm",
    "kuk",
    "alm",
    "kpl",
    "ktv",
]

if __name__ == "__main__":
    import json
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "network.json")

    with open(output_path, "w") as f:
        json.dump(station_dict, f, indent=2)
        print(f"Successfully generated {output_path}")
