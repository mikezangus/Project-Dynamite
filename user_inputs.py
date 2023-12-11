import json
import os


def get_user_inputs(action: str, chamber: bool = None, data_dir = None):


    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "us_states_all.json"), "r") as us_states_all_file:
        us_states_all = json.load(us_states_all_file)
    with open(os.path.join(current_dir, "us_states_at_large.json"), "r") as us_states_at_large_file:
        us_states_at_large = json.load(us_states_at_large_file)


    def input_choice(subject: str, action: str, choices: list = None):
        choices_text = f"\n{', '.join(choices)}" if choices else ""
        input_message = input(f"From which {subject} do you want to {action} data?:{choices_text}\n> ")
        return input_message
        

    def print_retry_message(subject: str):
        retry_message = print(f"You've entered an invalid {subject}, try again")
        return retry_message
        

    def is_valid_input(choice: str, choices: list):
        return choice in choices or choice.lower() == "all"


    def decide_year(chamber: bool = None):
        subject = "year"
        if chamber:
            year_input = input_choice(subject = subject, action = action)
            return year_input
        years = sorted([y for y in os.listdir(data_dir) if not y.startswith(".")])
        while True:
            year_input = input_choice(subject = subject, action = action, choices = years)
            if year_input in years:
                return year_input
            print_retry_message(subject = subject)
            continue
                    

    def decide_chamber():
        subject = "chamber"
        chambers = ["House", "Senate"]
        while True:
            chamber_input = input_choice(subject = subject, action = action, choices = chambers).capitalize()
            if is_valid_input(choice = chamber_input, choices = chambers):
                return chamber_input.lower()
            print_retry_message(subject = subject)
            continue         


    def decide_state(year: str, chamber: str = None):
        subject = "state"
        if chamber:
            all_states = list(us_states_all.values())
            while True:
                state_input = input_choice(subject = subject, action = action, choices = all_states).upper()
                if is_valid_input(choice = state_input, choices = all_states):
                    return state_input
                print_retry_message(subject = subject)
                continue
        states_dir = os.path.join(data_dir, year)
        all_states = sorted([s for s in os.listdir(states_dir) if not s.startswith(".")])
        while True:
            state_input = input_choice(subject = subject, action = action, choices = all_states).upper()
            if is_valid_input(choice = state_input, choices = all_states):
                return state_input
            print_retry_message(subject = subject)
            continue


    def decide_district(year: str, state: str, chamber: str = None):
        subject = "district"
        if chamber:
            district_input = str(input_choice(subject = subject, action = action)).zfill(2)
            return district_input
        districts_dir = os.path.join(data_dir, year, state)
        districts = sorted([d for d in os.listdir(districts_dir) if not d.startswith(".")])
        if len(districts) == 1:
            district_input = districts[0]
            return district_input
        while True:
            district_input = str(input_choice(subject = subject, action = action, choices = districts)).zfill(2)
            if is_valid_input(choice = district_input, choices = districts):
                return district_input
            print_retry_message(subject = subject)
            continue
        

    def decide_candidate(year: str, state: str, district: str):
        subject = "candidate"
        candidates_dir = os.path.join(data_dir, year, state, district)
        source_file_names = sorted([f for f in os.listdir(candidates_dir) if not f.startswith(".") and f.endswith(".csv") and f.count("_") == 6])
        candidate_last_names = [file.split("_")[3] for file in source_file_names]
        while True:
            candidate_input = input_choice(subject = subject, action = action, choices = candidate_last_names).upper()
            if is_valid_input(choice = candidate_input, choices = candidate_last_names):
                return candidate_input
            print_retry_message(subject = subject)  
            continue
        

    year = decide_year(chamber = chamber)

    if chamber:
        chamber = decide_chamber()
    else:
        chamber = None

    state = decide_state(year = year, chamber = chamber)

    if isinstance(state, list) or state.lower() == "all":
        district = None
    elif chamber == "senate":
        district = None
    elif chamber == "house":
        if state in us_states_at_large.values():
            district = "00"
        else:
            district = decide_district(chamber = chamber, year = year, state = state)

    if chamber:
        candidate = None
    else:
        candidate = decide_candidate(year = year, state = state, district = district)
    
    
    return year, chamber, state, district, candidate
