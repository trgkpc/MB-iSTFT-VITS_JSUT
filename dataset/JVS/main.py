import sys
import os
from pathlib import Path
include_path = os.path.join(str(Path(__file__).resolve().absolute().parents[1]), "preprocess_code")
sys.path.append(include_path)
from construct_corpus import construct_corpus

if __name__ == '__main__':
    input_top_dir = 'jvs_ver1'
    utterance_list = []
    for spk_id in range(1, 101):
        spk = 'jvs' + str(spk_id).zfill(3)
        spk_dir = os.path.join(input_top_dir, spk)
        for subset in ['parallel100', 'nonpara30']:
            input_dir = os.path.join(spk_dir, subset)
            lines = open(os.path.join(input_dir, 'transcripts_utf8.txt'), 'r').readlines()
            for l in lines:
                bname, txt = l.strip("\n").split(":")
                utt = {
                    "spk": spk,
                    "txt": txt,
                    "wav_path": os.path.join(input_dir, "wav24kHz16bit", bname+".wav"),
                    "resample_wav_fname": os.path.join("wav", spk, subset, bname+".wav") # ここは自分で設定する
                }
                utterance_list.append(utt)
    
    construct_corpus(os.path.abspath(__file__), utterance_list)
