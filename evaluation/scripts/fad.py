import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def main():

    with open("./experiments/fad/drumset.json", "r") as config_file:
        config = json.load(config_file)

    background_path = config.get("background_path")
    resynth_paths = config.get("resynth_paths", [])
    if not background_path or not resynth_paths:
        logging.error("Configuration file must specify a 'background_path' and a list of 'resynth_paths'.")
        exit(1)

    from frechet_audio_distance import FrechetAudioDistance
    modname = "vggish"
    # Initialize FrechetAudioDistance
    frechet = FrechetAudioDistance(
        model_name=modname,
        sample_rate=16000,  # VGGish resamples files to 16kHz
        use_pca=False,
        use_activation=False,
        verbose=False,
    )

    # Compute distances for each resynth path
    results = {}
    for resynth_path in resynth_paths:
        if not os.path.exists(resynth_path):
            logging.warning(f"Resynth path does not exist: {resynth_path}")
            continue

        distance = frechet.score(
            background_path,
            resynth_path,
            background_embds_path=background_path + f"/bkg_embeddings_{modname}.npy",
            eval_embds_path=resynth_path + f"/resynth_embeddings_{modname}.npy",
            dtype="float32",
        )
        results[resynth_path] = distance
        logging.info(f"Distance for {resynth_path}: {distance:.2f}")


if __name__ == "__main__":
    main()
