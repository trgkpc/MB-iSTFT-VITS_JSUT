from tqdm import tqdm
import os
import torchaudio
import random

import sys
import os
from pathlib import Path
include_path = os.path.join(str(Path(__file__).resolve().absolute().parents[3]), "include")
sys.path.append(include_path)
from preprocess_japanese import preprocess_japanese

def make_filedir(file_path):
    file_dir = os.path.dirname(file_path)
    if len(file_dir) > 0:
        os.makedirs(file_dir, exist_ok=True)

def resample(ifname, ofname, fs_target):
    x, fs = torchaudio.load(ifname)
    x = torchaudio.transforms.Resample(fs, fs_target)(x)
    torchaudio.save(ofname, x, fs_target)

def write_filelist(path, lis):
    make_filedir(path)
    with open(path, "w") as f:
        for l in lis:
            print("\t".join(l), file=f)

def construct_corpus(utterance_list, filelist_dir='filelist', val_size=100, fs=22050, verbose=False):
    files = list()
    for utt in tqdm(utterance_list):
        spk = utt["spk"]
        txt = utt["txt"]
        ifname = utt["wav_path"]
        ofname = utt["resample_wav_fname"]
        phonemes,accent = preprocess_japanese(txt)
        
        if len(phonemes) != len(accent):
            if verbose:
                print("[[WARNING]] skip file:", ifname)
                print("text:", txt)
            continue

        if os.path.exists(ifname):
            make_filedir(ofname)
            resample(ifname, ofname, fs)

            files.append([ofname, " ".join(phonemes), "".join(accent), spk])
        else:
            if verbose:
                print("[[WARNING]] file not exists:", ifname)
    
    random.seed(765)
    random.shuffle(files)

    train = files[:-val_size]
    val = files[-val_size:]
    
    write_filelist(os.path.join(filelist_dir, "train.txt"), train)
    write_filelist(os.path.join(filelist_dir, "val.txt"), val)
    

