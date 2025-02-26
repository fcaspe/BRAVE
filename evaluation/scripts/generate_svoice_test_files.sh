mkdir -p svoice
mkdir -p experiments/test_audios/svoice

cd svoice
wget "http://www.isophonics.net/sites/isophonics.net/files/SingingDatabase.zip" -O svoice.zip
unzip svoice.zip
cd ..

# Extract from first female chinese voice and the western female voice
cp svoice/monophonic/chinese/fem_01/pos*.wav ./svoice/
cp svoice/monophonic/western/fem_12/pos_3.wav ./svoice/w_pos_3.wav
cp svoice/monophonic/western/fem_12/pos_4.wav ./svoice/w_pos_4.wav

cp ./svoice/*.wav ./experiments/test_audios/svoice/

# Cleanup
rm -rf svoice

# Loudness normalize
python scripts/loud_tool.py experiments/test_audios/svoice/ --target-lufs -18