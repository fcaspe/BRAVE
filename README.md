<h1 align="center">Designing Neural Synthesizers for Low Latency Interaction</h1>
<div align="center">
<h3>
    <a href="http://insert_link_here" target="_blank">paper</a> - <a href="https://fcaspe.github.io/brave" target="_blank">website</a> - <a href="https://fcaspe.github.io/brave" target="_blank">evaluation</a> - <a href="https://fcaspe.github.io/brave" target="_blank">plugin</a>
</h3>

</div>


This repo contains the official Pytorch implementaiton of **BRAVE** a low-latency real-time audio variational encoder for instrumental performance. It also implements all of the [other models tested on the paper](link_to_replication).

## Install

We use the **acids-rave** package for preprocessing the data and training the models.

```bash
pip install acids-rave==2.3 h5py # may work with lower versions too.
conda install ffmpeg
# [TODO] git clone the repo chdir
```
## Preparing Dataset

We use the same `rave preprocess` tool as RAVE for dataset preparation. RAVE datasets will work with this repo's models. [Check RAVE's repo for more info on dataset preparation](https://github.com/acids-ircam/RAVE).

```bash
rave preprocess --input_path /audio/folder --output_path /dataset/path --channels X
```

## Training

We use the same `rave train` CLI for training. Make sure to specify with `--config` a path to one of the `.gin` configs provided in this repo. For instance, to train BRAVE:

```bash
rave train --config ./configs/brave.gin --name my_brave_run --db_path path/to/my/dataset
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

BRAVE is also compatible with many creative coding tools and plugins that use RAVE models.  
You can use this method to export a BRAVE model to some the great tools created by the community, such as:

 - [nn~](https://github.com/acids-ircam/nn_tilde) for Max-MSP & PureData
 - [SuperCollider](https://github.com/victor-shepardson/rave-supercollider)
 - [RAVE VST](https://forum.ircam.fr/projects/detail/rave-vst/)
 - And probably more!

Please note these might show **higher latency** than the BRAVE plugin.
 ```bash
rave export --run path/to/model_checkpoint.ckpt
```
This will store a TorchScript `(.ts)` model next to the checkpoint file which you can load on your selected applications.


## Cite Us

If you find this work useful please consider citing our work:

```bibtex
@article{caspe2025designing,
    title={{Designing Neural Synthesizers for Low Latency Interaction}},
    author={Caspe, Franco and Shier, Jordie and Sandler, Mark and Saitis, Charis and McPherson, Andrew},
    journal={Journal of the Audio Engineering Society},
    year={2025}
}
```