'''
Convert a Praat TextGrid to BORIS observation.
'''
import os

import tgt

from . import boris_tools

tier_type_to_behavior_type = {
    'TextTier': 'Point event',
    'PointTier': 'Point event',
    'IntervalTier': 'State event',
}


def _validate_tier_behavior_compatibility(tier, behavior):
    tier_type = tier.tier_type()
    behavior_type = behavior['type']
    if tier_type_to_behavior_type[tier_type] != behavior_type:
        msg = f'Tier type {tier_type} is incompatible with behavior type {behavior_type}'
        raise TypeError(msg)


def _annotation_to_events(annotation, behavior_code, subject_name):
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


def convert(textgrid_path, boris_path, mappings):
    boris = boris_tools.read_boris(boris_path)
    textgrid = tgt.io.read_textgrid(textgrid_path)

    events = []

    for mapping in mappings:
        tier = textgrid.get_tier_by_name(mapping['tier_name'])
        behavior = boris_tools.get_behavior_by_code(boris, mapping['behavior_code'])
        _validate_tier_behavior_compatibility(tier, behavior)
        # We don't need the subject, only to fail if it doesn't exist
        boris_tools.get_subject_by_name(boris, mapping['subject_name'])

        for annotation in tier:
            events += _annotation_to_events(
                annotation,
                mapping['behavior_code'],
                mapping['subject_name'],
            )

    observation_name = os.path.basename(textgrid_path)
    observation = boris_tools.create_observation(
        events=events,
        timestamp=os.path.getmtime(textgrid_path),
    )
    boris = boris_tools.add_observation(boris, observation_name, observation)
    boris_tools.write_boris(boris, boris_path)
