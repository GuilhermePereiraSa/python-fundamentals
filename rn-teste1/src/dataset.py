from torch.utils.data import Dataset
from torchvision.io import read_image
import torch
import pandas as pd

def default_transform(image):
    return image / 255 # 0 -> 1; granulanidade - rede perceber pequenas diferenças


class MNISTDataset(Dataset):
    def __init__(self, dataframe: pd.DataFrame, transform=default_transform):
        self.dataframe = dataframe
        self.transform = transform
        
    def __len__(self):
        return len(self.dataframe)
    
    def __getitem__(self, index):
        
        row = self.dataframe.iloc[index]
        img_path = row["path"]
        label = row["label"] 
        
        # to tensor 
        label_t = torch.tensor(label, dtype=torch.long)
        image = read_image(img_path).to(torch.float32) # read_image returns as tensor
        if self.transform:
            image = self.transform(image)
        return image, label_t
    