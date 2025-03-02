<h1 align="center">Designing Neural Synthesizers for Low Latency Interaction</h1>
<div align="center">
<h3>
    <a href="http://insert_link_here" target="_blank">paper</a> - <a href="https://fcaspe.github.io/brave" target="_blank">audio examples</a> - <a href="https://fcaspe.github.io/brave" target="_blank">NAS evaluation pack</a> - <a href="https://fcaspe.github.io/braveplugin" target="_blank">low-latency plugin</a>
</h3>

</div>


This repo contains the official Pytorch implementaiton of **BRAVE** a low-latency audio variational autoencoder for instrumental performance. It also implements all of the [other models tested on the paper](https://github.com/fcaspe/BRAVE/tree/main/configs).

Check the [`evaluation`](https://github.com/fcaspe/BRAVE/tree/main/evaluation) directory for info on replicating the results of the paper.


## Install

We use the **acids-rave** package for preprocessing the audio datasets and training the models.

```bash
pip install h5py acids-rave==2.3 # may work with lower versions too.
conda install ffmpeg
# [TODO] git clone the repo chdir
```

## Preparing Dataset

We use the same `rave preprocess` tool as RAVE for dataset preparation. Also, RAVE datasets will work with this repo's models. [Check RAVE's info on dataset preparation](https://github.com/acids-ircam/RAVE?tab=readme-ov-file#dataset-preparation).

```bash
rave preprocess --input_path /audio/folder --output_path path/to/preprocessed/dataset/ --channels X
```

## Training

We use the same `rave train` CLI for training. Make sure to specify with `--config` a path to one of the `.gin` configs provided in this repo. For instance, to train BRAVE:

```bash
rave train --config ./configs/brave.gin --name my_brave_run --db_path path/to/preprocessed/dataset/
```

## Exporting BRAVE for Real-Time Inference

### Low-latency BRAVE Plugin

The [BRAVE plugin](link_to_plugin) can run BRAVE models at < 10 ms latency and low jitter (~3 ms).

Use the `export_brave_plugin.py` utility to export a trained model. This requires a BRAVE checkpoint (`.ckpt`) created with `rave train`.  
It does not work with models exported to TorchScript (`.ts`).

```bash
python ./scripts/export_brave_plgin.py --model path/to/model_checkpoint.ckpt --output_path ./exported_model.h5
```
**NOTE:** BRAVE works better when run at its original sampling rate. For best results, make sure that you run the plugin **at the same sample rate as the data used to train it**.

### Standard RAVE Export Method

BRAVE is compatible with many creative coding tools and plugins that use RAVE models. You can export a BRAVE model to work with some great tools created by the community, such as:

 - [nn~](https://github.com/acids-ircam/nn_tilde) for Max-MSP & PureData
 - [SuperCollider](https://github.com/victor-shepardson/rave-supercollider) UGen
 - IRCAM's [RAVE VST](https://forum.ircam.fr/projects/detail/rave-vst/)
 - And probably some more

Please note these might show **higher latency** than the BRAVE Plugin due to a different audio buffering strategy.
 ```bash
rave export --run path/to/model_checkpoint.ckpt
```
This will store a TorchScript `(.ts)` model next to the checkpoint file which you can load on your selected application.

## Cite Us

If you find this work useful please consider citing our paper:

```bibtex
@article{caspe2025designing,
    title={{Designing Neural Synthesizers for Low Latency Interaction}},
    author={Caspe, Franco and Shier, Jordie and Sandler, Mark and Saitis, Charis and McPherson, Andrew},
    journal={Journal of the Audio Engineering Society},
    year={2025}
}
```