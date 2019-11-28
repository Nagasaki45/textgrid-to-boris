'''
Convert a Praat TextGrid to BORIS observation.
'''

import argparse
import collections
import os
import sys

import tgt

from . import boris_tools

Mapping = collections.namedtuple(
    'Mapping',
    ['tier_name', 'behavior_code', 'subject_name'],
)

tier_type_to_behavior_type = {
    'TextTier': 'Point event',
    'PointTier': 'Point event',
    'IntervalTier': 'State event',
}


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('textgrid', help='Praat TextGrid file')
    parser.add_argument('boris', help='BORIS project file')
    parser.add_argument('mapping', nargs='*',
                        help='mappings of tier:behavior_code:subject_name')
    return parser.parse_args(argv)


def parse_mapping(mapping):
    parts = mapping.split(':')
    if len(parts) == 2:
        subject_name = None
    elif len(parts) == 3:
        subject_name = parts[-1]
    else:
        raise ValueError(f'Invalid mapping: "{mapping}"')
    tier_name, behavior_code, *_ = parts
    return Mapping(tier_name, behavior_code, subject_name)


def validate_tier_behavior_compatibility(tier, behavior):
    tier_type = tier.tier_type()
    behavior_type = behavior['type']
    if tier_type_to_behavior_type[tier_type] != behavior_type:
        msg = f'Tier type {tier_type} is incompatible with behavior type {behavior_type}'
        raise TypeError(msg)


def annotation_to_events(annotation, behavior_code, subject_name):
    if isinstance(annotation, tgt.core.Point):
        return [
            boris_tools.create_event(
                annotation.start_time,
                behavior_code,
                subject_name,
            ),
        ]
    return [
        boris_tools.create_event(
            annotation.start_time,
            behavior_code,
            subject_name,
        ),
        boris_tools.create_event(
            annotation.end_time,
            behavior_code,
            subject_name,
        ),
    ]


def cli(argv):
    args = parse_arguments(argv)

    boris = boris_tools.read_boris(args.boris)
    textgrid = tgt.io.read_textgrid(args.textgrid)

    mappings = [parse_mapping(m) for m in args.mapping]

    events = []

    for mapping in mappings:
        tier = textgrid.get_tier_by_name(mapping.tier_name)
        behavior = boris_tools.get_behavior_by_code(boris, mapping.behavior_code)
        validate_tier_behavior_compatibility(tier, behavior)
        # We don't need the subject, only to fail if it doesn't exist
        boris_tools.get_subject_by_name(boris, mapping.subject_name)

        for annotation in tier:
            events += annotation_to_events(
                annotation,
                mapping.behavior_code,
                mapping.subject_name,
            )

    observation_name = os.path.basename(args.textgrid)
    observation = boris_tools.create_observation(
        events=events,
        timestamp=os.path.getmtime(args.textgrid),
    )
    boris = boris_tools.add_observation(boris, observation_name, observation)
    boris_tools.write_boris(boris, args.boris)


def main():
    return cli(sys.argv[1:])
