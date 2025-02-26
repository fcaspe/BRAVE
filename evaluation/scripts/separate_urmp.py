import argparse
import os
import sys
from functools import partial
from pathlib import Path
from shutil import copyfile

from tqdm.contrib.concurrent import thread_map

# Create the parser
parser = argparse.ArgumentParser(description="Process a directory.")

# Add a positional argument
parser.add_argument("directory", type=str, help="The directory to process.")

# Add a positional argument
parser.add_argument("instrument", type=str, help="Instrument to separate.")

# Execute the parse_args() method
args = parser.parse_args()


def create_mono_urmp(instrument_key, audio_files, target_dir, instruments_dict):
    target_dir = target_dir / instruments_dict[instrument_key]
    if not target_dir.exists():
        target_dir.mkdir()
    cur_audio_files = [
        audio_file
        for audio_file in audio_files
        if f"_{instrument_key}_" in audio_file.name
    ]
    [
        copyfile(audio_file, target_dir / audio_file.name)
        for audio_file in cur_audio_files
    ]


def separate_urmp(urmp_source_folder, instruments_dict):
    # Phase 0 - copy all urmp wavs to corresponding folders

    CWD = Path("./")

    urmp_path = CWD / urmp_source_folder

    # Create directories if needed
    dirs = ["files"]
    target_dir = CWD
    for d in dirs:
        target_dir = target_dir / d
        # print(target_dir)
        target_dir.mkdir(exist_ok=True)

    # Find relevant audio files.
    urmp_audio_files = list(urmp_path.glob(f"./*/AuSep*.wav"))

    print("[INFO] URMP Path: {}".format(urmp_path))

    print("[INFO] Number of files: {}".format(len(urmp_audio_files)))
    if len(urmp_audio_files) == 0:
        quit()
    # Partial function with instruments pre-configured for processing.
    create_mono_urmp_partial = partial(
        create_mono_urmp,
        audio_files=urmp_audio_files,
        target_dir=target_dir,
        instruments_dict=instruments_dict,
    )

    # Spawn threads to copy files.
    thread_map(create_mono_urmp_partial, list(instruments_dict.keys()))

    return


def main():
    # Check if the provided directory path exists
    if not os.path.isdir(args.directory):
        print(f"The directory '{args.directory}' does not exist or is not a directory.")
        quit()

    print(args.directory)
    urmp_source_folder = args.directory
    all_instruments_dict = {
        "vn": "violin",
        'tpt': 'trumpet',
        'fl' : 'flute',
        'va': 'viola',
        'vc': 'cello',
        'db': 'double_bass',
        'ob': 'oboe',
        'cl': 'clarinet',
        'sax': 'saxophone',
        'bn': 'bassoon',
        'hn': 'horn',
        'tbn': 'trombone',
        'tba': 'tuba',
    }
    instrument_dict = None
    for k in all_instruments_dict.keys():
        if all_instruments_dict[k] == args.instrument:
            instrument_dict = {k:all_instruments_dict[k]}

    if instrument_dict is not None:
        separate_urmp(urmp_source_folder, instrument_dict)
    else:
        print('[ERROR] No matching instrument found in URMP.')


if __name__ == "__main__":
    main()
