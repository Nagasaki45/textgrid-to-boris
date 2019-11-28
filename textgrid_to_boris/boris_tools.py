from datetime import datetime
import json


def read_boris(filepath):
    # TODO input validation
    with open(filepath) as f:
        return json.load(f)


def write_boris(boris, filepath):
    with open(filepath, 'w') as f:
        json.dump(boris, f)


def get_behavior_by_code(boris, code):
    for behavior in boris['behaviors_conf'].values():
        if behavior['code'] == code:
            return behavior
    raise ValueError(f'Behavior doesn\'t exist: "{code}"')


def get_subject_by_name(boris, name):
    for subject in boris['subjects_conf'].values():
        if subject['name'] == name:
            return subject
    raise ValueError(f'Subject doesn\'t exist: "{name}"')


def create_event(start_time, subject_name, behavior_code):
    return [start_time, subject_name, behavior_code, '', '']


def create_observation(events, timestamp):
    date = datetime.fromtimestamp(timestamp)
    return {
        'events': events,
        'type': 'LIVE',  # Otherwise we need to take care of media.
                         # The user can do it later.
        'date': date.isoformat(),
        'description': '',
        'time offset': 0,
        'file': {i: [] for i in range(1, 9)},
    }


def add_observation(boris, name, observation):
    boris['observations'][name] = observation
    return boris
