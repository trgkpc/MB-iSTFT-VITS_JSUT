""" from https://github.com/Wataru-Nakata/FastSpeech2-JSUT """
import pyopenjtalk
from .prepare_tg_accent import pp_symbols
from .convert_label import openjtalk2julius

def preprocess_japanese(text:str):
    fullcontext_labels = pyopenjtalk.extract_fullcontext(text)
    phonemes , accents = pp_symbols(fullcontext_labels)
    phonemes = [openjtalk2julius(p) for p in phonemes if p != '']
    return phonemes, accents

if __name__ == '__main__':
    p, a = preprocess_japanese("吾輩は猫である．")
    print(p)
    print(a)

