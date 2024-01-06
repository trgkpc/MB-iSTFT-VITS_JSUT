import argparse
import os
import re
import sys
import glob
import random

from tqdm import tqdm

""" this function is from https://github.com/Wataru-Nakata/FastSpeech2-JSUT """
def numeric_feature_by_regex(regex, s):
    match = re.search(regex, s)
    if match is None:
        return -50
    return int(match.group(1))

""" this function is from https://github.com/Wataru-Nakata/FastSpeech2-JSUT """
def pp_symbols(labels, drop_unvoiced_vowels=True):
    PP = []
    accent = []
    N = len(labels)

    for n in range(len(labels)):
        lab_curr = labels[n]


        p3 = re.search(r"\-(.*?)\+", lab_curr).group(1)

        if drop_unvoiced_vowels and p3 in "AEIOU":
            p3 = p3.lower()

        if p3 == 'sil':
            assert n== 0 or n == N-1
            if n == N-1:
                e3 = numeric_feature_by_regex(r"!(\d+)_", lab_curr)
                if e3 == 0:
                    PP.append("")
                elif e3 == 1:
                    PP.append("")
            continue
        elif p3 == "pau":
            PP.append("sp")
            accent.append('0')
            continue
        else:
            PP.append(p3)
        # アクセント型および位置情報（前方または後方）
        a1 = numeric_feature_by_regex(r"/A:([0-9\-]+)\+", lab_curr)
        a2 = numeric_feature_by_regex(r"\+(\d+)\+", lab_curr)
        a3 = numeric_feature_by_regex(r"\+(\d+)/", lab_curr)
        # アクセント句におけるモーラ数
        f1 = numeric_feature_by_regex(r"/F:(\d+)_", lab_curr)
        if n+1 == N:
            # TODO(future): 例外処理の整合性？
            a1_next = -50
        else:
            lab_next = labels[n + 1]
            a2_next = numeric_feature_by_regex(r"\+(\d+)\+", lab_next)
        # アクセント境界
        if a3 == 1 and a2_next == 1:
            accent.append("#")
        # ピッチの立ち下がり（アクセント核）
        elif a1 == 0 and a2_next == a2 + 1 and a2 != f1:
            accent.append("]")
        # ピッチの立ち上がり
        elif a2 == 1 and a2_next == 2:
            accent.append("[")
        else:
            accent.append('0')
    return PP, accent

def convert_pp(lis):
    ret = []
    for p in lis:
        if p in list("AIUEO"):
            p = p.lower()
        if p == "cl":
            p = "q"
        if p == "pau":
            p = "sp"
        ret.append(p)
    return ret

def write_filelist(path, lis):
    fl_dir = os.path.dirname(path)
    if len(fl_dir) > 0:
        os.makedirs(fl_dir, exist_ok=True)
    with open(path, "w") as f:
        for l in lis:
            print("\t".join(l), file=f)

if __name__ == '__main__':
    result = []
    for lab_file in tqdm(sorted(glob.glob("jsut-lab/*/lab/*.lab"))):
        with open(lab_file) as f:
            lines = f.readlines()
        lab, accent = pp_symbols(lines)

        bname = os.path.basename(lab_file).split(".")[0]
        wav_path = os.path.join("dataset/JSUT", "wav", bname+".wav")

        if lab[-1] == "":
            del lab[-1]
        lab = convert_pp(lab)
        assert len(lab) == len(accent)

        result.append([wav_path, " ".join(lab), "".join(accent), "JSUT"])
    
    random.seed(765)
    random.shuffle(result)
    val_size = 100
    train = result[:-val_size]
    val = result[-val_size:]
    
    out_dir = "filelist"
    write_filelist(os.path.join(out_dir, "train.txt"), train)
    write_filelist(os.path.join(out_dir, "val.txt"), val)
    

