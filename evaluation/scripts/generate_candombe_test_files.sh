# Description: Download the Candombe dataset from Zenodo
wget "https://zenodo.org/records/6533068/files/candombe_audio.zip?download=1" -O candombe_audio.zip
unzip candombe_audio.zip

cd candombe_audio
# Loop through each .flac file in the current directory
for file in *.flac; do
    # Use ffmpeg to convert the .flac file to .wav
    # The new file will have the same name but with a .wav extension
    ffmpeg -i "$file" "${file%}.wav" -hide_banner -loglevel error
done
rm *.flac
cd ..

# Preprocess the dataset
mkdir -p experiments/test_audios/candombe
#mkdir -p dataset/candombe/files
mv candombe_audio/zavala.muniz.2014_49.flac.wav experiments/test_audios/candombe
mv candombe_audio/csic.1995_ansina1_05.flac.wav experiments/test_audios/candombe
mv candombe_audio/proyecto.1992_magarinos_02.flac.wav experiments/test_audios/candombe
#mv candombe_audio/*.wav dataset/candombe/files

# Clean up
rm -rf candombe_audio.zip candombe_audio
# Loudness normalize
python scripts/loud_tool.py experiments/test_audios/candombe/ --target-lufs -36