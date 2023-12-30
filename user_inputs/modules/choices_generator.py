import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.abspath(current_dir))
project_dir = os.path.dirname(parent_dir)
sys.path.append(project_dir)
from us_states.us_state_loader import load_states
us_state_all_list, _ = load_states()


def generate_year_choices(source: str, raw_data_dir: str):
    if source.lower().strip() == "internet":
        year_choices = None
    elif source.lower().strip() == "files":
        year_choices = sorted([y for y in os.listdir(raw_data_dir) if not y.startswith(".")])
    return year_choices


def generate_chamber_choices():
    chamber_choices = ["house", "senate"]
    return chamber_choices


def generate_state_choices(source: str, raw_data_dir: str, year: str, chamber: str):
    if source.lower().strip() == "internet":
        state_choices = us_state_all_list
    elif source.lower().strip() == "files":
        states_dir = os.path.join(raw_data_dir, year, chamber)
        state_choices = sorted([s for s in os.listdir(states_dir) if not s.startswith(".")])
    return state_choices


def generate_district_choices(source: str, raw_data_dir: str, year: str, chamber: str, state: str):
    if source.lower().strip() == "internet":
        district_choices = None
    elif source.lower().strip() == "files":
        districts_dir = os.path.join(raw_data_dir, year, chamber, state)
        district_choices = sorted([d for d in os.listdir(districts_dir) if not d.startswith(".")])
    return district_choices


def generate_candidate_choices(source: str, raw_data_dir: str, year: str, chamber: str, state: str, district: str = None):
    if source.lower().strip() == "internet":
        candidate_choices = None
    elif source.lower().strip() == "files":
        if chamber.lower() == "house":
            candidates_dir = os.path.join(raw_data_dir, year, chamber, state, district)
        elif chamber.lower() == "senate":
            candidates_dir = os.path.join(raw_data_dir, year, chamber, state)
        candidate_choices = sorted(
            [c for c in os.listdir(candidates_dir) if not c.startswith(".") and c.endswith(".csv") and c.count("_") == 6]
        )
    return candidate_choices