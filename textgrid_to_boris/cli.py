import argparse

from . import core


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('textgrid', help='Praat TextGrid file')
    parser.add_argument('boris', help='BORIS project file')
    parser.add_argument('mapping', nargs='*',
                        help='mappings of tier:behavior_code:subject_name')
    return parser.parse_args()


def parse_mapping(mapping):
    parts = mapping.split(':')
    if len(parts) == 2:
        subject_name = None
    elif len(parts) == 3:
        subject_name = parts[-1]
    else:
        raise ValueError(f'Invalid mapping: "{mapping}"')
    tier_name, behavior_code, *_ = parts
    return {
        'tier_name': tier_name,
        'behavior_code': behavior_code,
        'subject_name': subject_name,
    }


def main():
    args = parse_arguments()
    mappings = [parse_mapping(m) for m in args.mapping]
    return core.convert(args.textgrid, args.boris, mappings)
