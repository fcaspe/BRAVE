from absl import app, flags, logging
import torch, torchaudio, os, tqdm, gin
import cached_conv as cc
from rave.core import get_rave_receptive_field
from rave.masker import SpectrogramMasking
from nleval import NeuralLatencyEvaluator, ModelWrapper

import numpy
try:
    import rave
except:
    import sys, os 
    sys.path.append(os.path.abspath('.'))
    import rave


FLAGS = flags.FLAGS
flags.DEFINE_string('model', required=True, default=None, help="model path")
#flags.DEFINE_multi_string('input', required=True, default=None, help="model inputs (file or folder)")
flags.DEFINE_string('name', default='noname', help="Results name")
flags.DEFINE_integer('gpu', default=-1, help='GPU to use')

def get_audio_files(path):
    audio_files = []
    valid_exts = rave.core.get_valid_extensions()
    for root, _, files in os.walk(path):
        valid_files = list(filter(lambda x: os.path.splitext(x)[1] in valid_exts, files))
        audio_files.extend([(path, os.path.join(root, f)) for f in valid_files])
    return audio_files


@torch.no_grad()
def main(argv):
    torch.set_float32_matmul_precision('high')
    torch.manual_seed(3402)
    cc.use_cached_conv(True)

    model_path = FLAGS.model
    # load model
    logging.info("building rave")
    is_scripted = False
    if not os.path.exists(model_path):
        logging.error('path %s does not seem to exist.'%model_path)
        exit()
    if os.path.splitext(model_path)[1] == ".ts":
        model = torch.jit.load(model_path)
        is_scripted = True
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
        if (model.decoder.cumulative_delay % 2) == 1:
            model.pqmf.reverse_half = rave.pqmf.reverse_half_alternative
            print('[INFO] PQMF Adjusted for odd cumulative delay.')

    # device
    if FLAGS.gpu >= 0:
        device = torch.device('cuda:%d'%FLAGS.gpu)
        model = model.to(device)
    else:
        device = torch.device('cpu')
    
    wrapper = ModelWrapper()
    def eval_reset():
        x = torch.zeros(1,1,1024*64).to(model.device)
        model(x)
    def eval_forward(x):
        return model(x)
    def samplerate():
        return model.sr
    def current_device():
        return model.device
    wrapper.forward = eval_forward
    wrapper.reset = eval_reset
    wrapper.samplerate = samplerate
    wrapper.current_device = current_device

    evaluator = NeuralLatencyEvaluator(wrapper,FLAGS.name)
    evaluator.evaluate()

if __name__ == "__main__": 
    app.run(main)
