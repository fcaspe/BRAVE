INSTRUMENT='viola'

SOURCE=$1
if [ $SOURCE = "dir" ]; then
    TMP_DIR=/path/to/decompressed/URMP/folder/
    python scripts/datasets/separate_urmp.py $TMP_DIR/URMP $INSTRUMENT
else
    echo Will Download the complete URMP dataset and then split it. This may take a while . . .
    TMP_DIR=/tmp/urmp_dset
    mkdir -p $TMP_DIR
    wget https://datadryad.org/stash/downloads/file_stream/99348 -O $TMP_DIR/urmp.tar.gz --user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    cd $TMP_DIR
    tar -xzvf urmp.tar.gz
    cd -

    # separate and store in ./files
    python scripts/datasets/separate_urmp.py $TMP_DIR/Dataset $INSTRUMENT
fi

mkdir -p experiments/test_audios/$INSTRUMENT
cp -r files/$INSTRUMENT/*.wav experiments/test_audios/$INSTRUMENT/

# Cleanup
rm -rf files
#rm -rf $TMP_DIR

# Loudness normalize
python scripts/loud_tool.py experiments/test_audios/$INSTRUMENT/ --target-lufs -18