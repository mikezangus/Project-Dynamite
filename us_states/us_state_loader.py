import json
import os


def load_states():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "us_states_all.json"), "r") as us_states_all_file:
        us_state_all_list = json.load(us_states_all_file)
    with open(os.path.join(current_dir, "us_states_at_large.json"), "r") as us_states_at_large_file:
        us_state_at_large_list = json.load(us_states_at_large_file)
    return us_state_all_list, us_state_at_large_list