# TextGrid-to-BORIS

Convert [Praat](http://www.fon.hum.uva.nl/praat/) TextGrid to [BORIS](http://www.boris.unito.it/) observation.

## Installation

This project requires python >= 3.6.

```bash
pip install --user git+https://github.com/nagasaki45/textgrid-to-boris.git
```

For more information see the [official packages installation guide](https://packaging.python.org/tutorials/installing-packages/).

## Usage

```bash
tgtb your.textgrid your.boris textgrid_tier_name:boris_behavior_code:boris_subject_name another_tier_name:boris_behavior_code:subject_name
```

`subject_name` is optional.
