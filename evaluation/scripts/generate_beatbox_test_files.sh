#!/bin/bash

# Description: Download the Beatbox dataset from Zenodo
wget "https://zenodo.org/records/5036529/files/AVP_Dataset.zip?download=1" -O beatbox.zip
unzip beatbox.zip

# Get the root directory (first directory) from the script's location
cd AVP_Dataset
rm noise_sample.wav
root_dir="$(pwd)"

# Find all .wav files in subdirectories and copy them to the root directory
find "$root_dir" -type f -name "*.wav" -exec cp {} "$root_dir" \;

# Get the first 80 .wav files in alphabetical order
first_files=$(find "$root_dir" -maxdepth 1 -type f -name "*.wav" | sort | head -n 80)

# Copy each file to the destination directory
destination_dir="../experiments/test_audios/beatbox/"
mkdir -p "$destination_dir"

#echo "Copying .wav files to $destination_dir"
echo "$first_files" | while read -r file; do
    cp "$file" "$destination_dir"
    #echo "Copied: $file"
done

cd ..
rm -rf AVP_Dataset/
rm beatbox.zip
# Loudness normalize
python scripts/loud_tool.py experiments/test_audios/beatbox/ --target-lufs -36