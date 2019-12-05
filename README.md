# TextGrid-to-BORIS

Convert [Praat](http://www.fon.hum.uva.nl/praat/) TextGrid to [BORIS](http://www.boris.unito.it/) observation.

## Installation

This project requires python >= 3.6.

```bash
pip install --user git+https://github.com/nagasaki45/textgrid-to-boris.git
```

For more information see the [official packages installation guide](https://packaging.python.org/tutorials/installing-packages/).

## Usage

### Command line interface

```bash
tgtb your.textgrid your.boris textgrid_tier_name:boris_behavior_code:boris_subject_name another_tier_name:boris_behavior_code:subject_name
```

`subject_name` is optional.

### As a library

```python
import textgrid_to_boris

# Add as many mappings as you want!
# Tier name, behavior code, and subject name should all
# exist beforehand. The script won't create them for you.
mappings = [
    {
        'tier_name': 'nose scratching',   # From TextGrid
        'behavior_code': 'NS',            # From BORIS
        'subject_name': 'participant01',  # From BORIS
    },
    {
        'tier_name': 'farting',
        'behavior_code': 'F',
        'subject_name': 'participant02',
    },
]

# This will add a new observation to your BORIS project
textgrid_to_boris.convert(
    'path/to/textgrid',
    'path/to/boris',
    mappings,
)
