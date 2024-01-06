import torchaudio
import os
from tqdm import tqdm

input_dir = "jsut_ver1.1"
output_dir = "wav"
fs_target = 22050

os.makedirs(output_dir, exist_ok=True)
for domain in tqdm(os.listdir(input_dir)):
    wav_in_dir = os.path.join(input_dir, domain, "wav")
    if not os.path.exists(wav_in_dir):
        continue
    for fname in os.listdir(wav_in_dir):
        x, fs = torchaudio.load(os.path.join(wav_in_dir, fname))
        x = torchaudio.transforms.Resample(fs, fs_target)(x)
        torchaudio.save(os.path.join(output_dir, fname), x, fs_target)
        
