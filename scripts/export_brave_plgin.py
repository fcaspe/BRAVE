from absl import app, flags, logging
import torch, os, gin
import h5py
import rave
import numpy as np
import cached_conv as cc

def store_state_dict_as_h5(filename:str,state_dict:dict):
    # Save the state dict to an HDF5 file
    
    prefixes = ["discriminator", "audio", "multiband"]
    filtered_dict = state_dict.copy()
    for prefix in prefixes:
        filtered_dict = {k: v for k, v in filtered_dict.items() if not k.startswith(prefix)}.copy()

    suffixes = ["pad","cache"]
    filtered_dict_2 = filtered_dict.copy()
    for suffix in suffixes:
        filtered_dict_2 = {k: v for k, v in filtered_dict_2.items() if not k.endswith(suffix)}.copy()

    with h5py.File(filename, 'w') as f:
        for k in filtered_dict_2.keys():
            f.create_dataset(k, data=filtered_dict_2[k].numpy())

FLAGS = flags.FLAGS
flags.DEFINE_string('model', required=True, default=None, help="Pretrained model path")
flags.DEFINE_string('output_path', required=True, default=None, help="Output exported model path")

@torch.no_grad()
def main(argv):
    cc.use_cached_conv(False)
    dtype = torch.float32
    torch.set_default_dtype(torch.float32)
    torch.manual_seed(3402)

    model_path = FLAGS.model
    # load model
    logging.info("building rave")
    is_scripted = False
    if not os.path.exists(model_path):
        logging.error('path %s does not seem to exist.'%model_path)
        exit()
    if os.path.splitext(model_path)[1] == ".ts":
        print('[ERROR] Torchscript models not supported.')
        quit()
    else:
        config_path = rave.core.search_for_config(model_path)
        print(f'Gin config path is {config_path}')
        if config_path is None:
            logging.error('config not found in folder %s'%model_path)
        gin.parse_config_file(config_path)
        model = rave.RAVE()
        run = rave.core.search_for_run(model_path)
        if run is None:
            logging.error("run not found in folder %s"%model_path)
        model = model.load_from_checkpoint(run)
        model = model.eval()

    for m in model.modules():
        if hasattr(m, "weight_g"):
            torch.nn.utils.remove_weight_norm(m)

    store_state_dict_as_h5(FLAGS.output_path,model.state_dict())

if __name__ == "__main__": 
    app.run(main)
