# Replicating the results of the paper

Hereby we provide a set of scripts for dataset preparation and evaluation of the trained models.
## Installing Eval Tools

Some additional tools are required for running the evaluations of the paper:

```bash
pip install frechet_audio_distance
pip install git+https://github.com/jorshi/neural-latency-eval #installs nleval package

```

## Training models from the paper

All implementations are available at the `configs` directory of this repo. Just change the config model accordingly:

```bash
rave train --config ./configs/SELECTED_MODEL.gin --gpu 0
```
After 1.5M steps, the training script will write a checkpoint named `epoch_1500000.ckpt` in the corresponding directory. We use these checkpoints for all trained models.
## Fetching Datasets

We provide scripts for fetching and splitting the datasets used in the paper, **with the exception of the filosax** dataset, which is open but requires a [download permission](https://zenodo.org/records/6335779#.Y_OMgy-l3T9) from the authors.

The scripts will downlaod and create directories with the decompressed files, assuming you are working from the this directory, the `evaluation` folder:

```bash
cd evaluation
source scripts/generate_drumset.sh #Example for downloading the drumset dataset.
```
This will create a `dataset` directory with the audio files and preprocessed data, and a `experiments/test_audios` tree with the drumset test audios.  
The other scripts also work on this tree as they just download the test audios.

## Evaluations
Here we detail how to run the evaluation scripts we use for producing the results in the paper.

### Running the models on audio files

We use the standard `rave generate` to process directories with audio files.  
Consider a checkpoint trained on the `drumset` dataset. To perform *resynthesis* just process the left-out drumset test set:

```bash
rave generate --model path/to/my_drumset_model.ckpt \
    --input ./experiments/test_audios/drumset \ # Perform resynthesis on test set

```

To perform *timbre transfer*, point the generation to one of the other percussive test sets.
```bash
rave generate --model path/to/my_drumset_model.ckpt \
    --input ./experiments/test_audios/beatbox \ # Perform voice to drumset transfer

```

### Audio Quality (Using Frechet Audio Distance)
We compute the Frechet Audio Distance with the `fad.py` script. This script consumes a `json` config file that specifies where to find the **background** audio files (we use the train set files) and the **resynthesized** files of all of the models you may wish to test. You can include here the reference test data.

We provide an example config file at `experiments/fad` to compute FAD on drumset for a series of models.

```bash
python ./scripts/fad.py ./experiments/fad/drumset.json
```
Edit the `json` file to point to the resynthesis folders.

The script will print the distance between the background and each resynthesized distribution using VGGish embeddings.

### Latency

The latency test requires a GPU to perform fast inference on a battery of synthetic test data, measuring the delay of the response when given known excitations. The results are stored under the name `EXPERIMENT_ID`.

```bash
python ./scripts/latency.py --model /path/to/checkpoint.ckpt --gpu 0 --name EXPERIMENT_ID
```

### Timbre Transfer Evaluation

This evaluation requires two directory trees with a similar structure: 

1. References Tree: Contains the test set audio files in separate directories.  
    - Example: `experiments/test_audios/` storing `drumset` `candombe` and `beatbox` directories with the test audio files.
2. Reconstructions Tree: Containing *timbre transfer* and *resynthesis* results organized per model, with each model directory following the same structure as the References Tree.
    - Example: `reconstructions/` directory storing `model_1` `model_2` and `model_3` directories.
     - Each model directory contains a tree with directories `drumset` `candombe` and `beatbox`, containing resynthesis and timbre transfer results respectively.

**Examples:**
With that structrure prepared, you can compute the MMD distance between the references, and the `beatbox` dataset *timbre transferred* to `drumset`, as performed by all models, with: 
```bash
nleval-mmd --matrix beatbox-drumset --references ./experiments/test_audios/ --reconstructions ./reconstructions/
```


Likewise, you can compute the MMD distance between the references and the resynthesized `drumset` as performed by all models with:
```bash
nleval-mmd --matrix drumset-drumset --references ./experiments/test_audios/ --reconstructions ./reconstructions/
```

Please refer to the `nleval` [evaluation pack](https://github.com/jorshi/neural-latency-eval) for further details on how to perform timbre transfer evaluation.

### Content Preservation

```bash
nleval-content --eval loudness
nleval-content --eval pitch
```

Please refer to the `nleval` [evaluation pack](https://github.com/jorshi/neural-latency-eval) for further details on how to perform content preservation evaluation.
