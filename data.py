import torchvision
import torchvision.transforms as T
from torch.utils.data import Dataset
import os

preprocess = T.Compose([
    #TODO: Swap resize and centercrop
    T.Resize(32),
    T.CenterCrop(32)
])

#TODO: Update path to include folders
def process_images(path, d_size=32):
    processed = []
    i = 0

    for filename in os.listdir(path):
        if filename.endswith('jpg'):
            if (i % 500 == 0):
                print("[PREPROCESSING] Processed {} images".format(i))

        img = torchvision.io.read_image(filename)
        processed.append(preprocess(img))

        i+=1

    return processed, len(processed)

class Spectrogram_Dataset(Dataset):
    def __init__(self):
        i, l = process_images("")
        self.images = i
        self.length = l

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return self.images[idx]