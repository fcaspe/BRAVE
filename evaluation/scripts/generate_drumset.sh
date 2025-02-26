# Download the filtered drumset dataset
wget https://pub-814e66019388451395cf43c0b6f10300.r2.dev/lhnas-drumset-raw-v3.tar.gz
tar -xf lhnas-drumset-raw-v3.tar.gz

# Get dataset info
python scripts/loud_tool.py dataset/drumset/

# Preprocess the dataset
rave preprocess --input_path dataset/drumset/train --output_path dataset/drumset/data

mkdir -p experiments/test_audios/
mv dataset/drumset/test experiments/test_audios/drumset
# Clean up
rm -rf lhnas-drumset-raw-v3.tar.gz
