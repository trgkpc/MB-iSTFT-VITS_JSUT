""" from https://github.com/keithito/tacotron """
import re
from .symbols import symbols


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

_accent_to_id = {'0':0, '[':1, ']':2, '#':3}
_id_to_accent = {i: a for a, i in _accent_to_id.items()}

accent_symbols = list(_accent_to_id.keys())

def text_to_sequence(text):
  return [_symbol_to_id[t] for t in text]

def sequence_to_text(sequence):
  return ''.join([_id_to_symbol[symbol_id] for symbol_id in sequence])

def accent_to_sequence(accent):
  return [_accent_to_id[a] for a in accent]

def sequence_to_text(sequence):
  return ''.join([_id_to_accent[accent_id] for accent_id in sequence])
