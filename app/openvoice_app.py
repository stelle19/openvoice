import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from melo.api import TTS
import nltk

ckpt_converter = 'checkpoints_v2/converter'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs_v2'


nltk.download('averaged_perceptron_tagger_eng', download_dir='nltk_data')

nltk.data.path.append('nltk_data')

tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

os.makedirs(output_dir, exist_ok=True)

reference_speaker = 'resources/Trumpvoice.mp3' # This is the voice you want to clone
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=True)


texts = {
    'EN_NEWEST': "Did you ever hear a folk tale about a giant turtle?",  # The newest English base speaker model
    'EN': "Did you ever hear a folk tale about a giant turtle?",
    'FR': "La lueur dorée du soleil caresse les vagues, peignant le ciel d'une palette éblouissante.",
}

language = "EN"
# speaker_id = 0  #speaker_ids: {'EN-US': 0, 'EN-BR': 1, 'EN_INDIA': 2, 'EN-AU': 3, 'EN-Default': 4}
# speaker_key = "en-us"

text = "Did you ever hear a folk tale about a giant turtle?"

src_path = f'{output_dir}/tmp.wav'

# Speed is adjustable
speed = 1.0

model = TTS(language=language, device=device)
speaker_ids = model.hps.data.spk2id
speaker_id =  speaker_ids[0][1]
speaker_key  =  speaker_ids[0][0].lower().replace('_', '-')
source_se = torch.load(f'checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
if torch.backends.mps.is_available() and device == 'cpu':
    torch.backends.mps.is_available = lambda: False
model.tts_to_file(text, speaker_id, src_path, speed=speed)
save_path = f'{output_dir}/output_v2_{speaker_key}.wav'
encode_message = "@MyShell"
tone_color_converter.convert(
    audio_src_path=src_path, 
    src_se=source_se, 
    tgt_se=target_se, 
    output_path=save_path,
    message=encode_message)
