import torchaudio

def resample(ifname, ofname, fs_target=22050):
    x, fs = torchaudio.load(ifname)
    x = torchaudio.transforms.Resample(fs, fs_target)(x)
    torchaudio.save(ofname, x, fs_target)
 
