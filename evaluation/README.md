# Replicating the results of the paper

Hereby we provide a set of scripts for dataset preparation and evaluation of the trained models.
## Installing Eval Tools

```bash
pip install frechet_audio_distance
pip install git+https://github.com/jorshi/neural-latency-eval #installs nleval package

```

## Training other models from the paper

All implementations are available at the `configs` directory of this repo. Just change the config model accordingly: `rave train --config ./configs/SELECTED_MODEL.gin`.

## Fetching Datasets

We provide scripts for fetching the datasets used in the paper, **with the exception of the filosax** dataset, which is open but requires a [download permission](https://zenodo.org/records/6335779#.Y_OMgy-l3T9) from the authors.

The scripts will downlaod and create directories with the decompressed files, assuming you are working from the this directory, the `evaluation` folder:

```bash
cd evaluation
source scripts/generate_drumset.sh #Example for downloading the drumset dataset.
```
This will create a `dataset` directory with the audio files and preprocessed data, and a `experiments/test_audios` tree with the drumset test audios.  
The other scripts also work on this tree as they just download the test audios.

## Evaluations
Here we detail how to run the evaluation scripts we use for producing the results in the paper.

### Audio Quality (Using Frechet Audio Distance)
We compute the Frechet Audio Distance with the `fad.py` script. This script consumes a `json` config file that specifies where to find the background data and the resynthesis files of all of the models you may wish to test, including the reference test data.

We provide an example config file at `experiments/fad` to compute FAD on drumset for a series of models.

```bash
python ./scripts/fad.py
```

### Latency

The latency test requires a GPU to perform fast inference on a battery of synthetic test data, measuring the delay of the response when given known excitations. The results are stored under the name EXPERIMENT_ID.

```bash
python ./scripts/test_latency.py --model /path/to/checkpoint.ckpt --gpu 0 --name EXPERIMENT_ID
```

### Timbre Transfer Evaluation

Add an example here

Please refer to the `nleval` [evaluation pack](https://github.com/jorshi/neural-latency-eval) for further details on how to perform timbre transfer evaluation.

### Content Preservation
nleval-content --eval loudness
nleval-content --eval pitch

Please refer to the `nleval` [evaluation pack](https://github.com/jorshi/neural-latency-eval) for further details on how to perform content preservation evaluation.
