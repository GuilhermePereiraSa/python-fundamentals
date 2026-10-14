import json
import torch

from pathlib import Path
import torch.nn as nn
import torch.nn.functional as F

from src.dataset import MNISTDataset
import pandas as pd
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np


LEARNING_RATE = 0.05
NUM_EPOCAS = 5
SEED = 42
MODEL_NAME = "mlp"


model_folder = Path("./modelos_treinados/" + MODEL_NAME)
model_folder.mkdir(parents=True, exist_ok=True)


DEVICE = torch.device("cpu")

torch.manual_seed(SEED)
np.random.seed(SEED)


# 3. definir modelo

class Modelo(nn.Module):
    def __init__(self):
        super(Modelo, self).__init__()
        
        self.camadas = nn.Sequential(
            # 28 x 28 = 768 pixels 
            nn.Flatten(), # [BATCH, n1, n2, ...] -> [BATCH, n1*n2*n2...]
            nn.Linear(28*28, 64), # 64
            nn.ReLU(),
            nn.Linear(64, 10) # 10
            
            # MODELO MAIS BASICO - 1 camada so linear;
            # agora 64 -> 10 
        )
        
    # como modelo roda
    def forward(self, x):
        return self.camadas(x)


# validacao 
def evaluate(model, data_loader):
    model.eval()
    
    soma_loss = 0.0
    acertos = 0
    
    dados = []
    
    with torch.no_grad():
        total = 0
        for batch_images, batch_labels in tqdm(data_loader, desc=f"Avaliacao", total=len(data_loader)):
            batch_images = batch_images.to(DEVICE)
            batch_labels = batch_labels.to(DEVICE)
                
            logits = model(batch_images)
            loss = F.cross_entropy(logits, batch_labels)
            
            soma_loss += loss.item()
            
            # soma -> item 
            acertos += (logits.argmax(dim=1) == batch_labels).sum().item()
            
            
            probs = F.softmax(logits, dim=1) # [BATCH, NUM_CLASSES] 
            for idx in range(batch_labels.shape[0]):
                dados.append({
                    "index": idx + total,
                    "target": batch_labels[idx].cpu().item(),
                    "pred": logits[idx].argmax(dim=0).cpu().item(),
                    "trust": probs[idx][logits[idx].argmax(dim=0)].cpu().item(),
                    "correct": (logits[idx].argmax(dim=0) == batch_labels[idx]).cpu().item(),
                })
            total += batch_labels.shape[0]
            
            
    loss_media = soma_loss/len(data_loader)
    precisao = acertos/len(data_loader.dataset)
    
    return loss_media, precisao, dados
        
    

if __name__ == "__main__":

    # 1. preparar e inspecionar os dados

    # 2. criar Dataset e DataLoader
    df_train = pd.read_csv("./data/metadados_treino.csv")
    train_dataset = MNISTDataset(df_train)
    # dataloader - escolha de sample - para aprendizado faz sentido embaralhar 
    # (gradiente -> heterogeneo)
    # workers para carrgear imagem em paralelo - persistente para nao reproduzir 
    # mesmo trabalho novamente 
    # (recarregar)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4, 
                            persistent_workers=True)

    df_test = pd.read_csv("./data/metadados_teste.csv")
    test_dataset = MNISTDataset(df_test)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4, 
                            persistent_workers=True)




    model = Modelo()
    model = model.to(DEVICE)

    # 4. escolher loss e optimizer

    optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)
    contagem = 0
    
    historico = []
    historico_teste = []
    
    # testa modelo antes do treinamneto
    
    loss_medio, acc, dados_teste = evaluate(model, test_loader)
    print(f"Antes Treino - Val Loss: {loss_medio:.4f}, Val Acc: {acc:.4f}")
    
    historico.append({
        "epoca": 0,
        "loss_medio": None,
        "val_loss": loss_medio, 
        "val_acc": acc
    })
    
    historico_teste.append({
        "epoca": 0,
        "dados": dados_teste,
    })
    

    # 5. treinar por batches e epocas
    for epoca in range(NUM_EPOCAS):
        model.train()
        soma_loss = 0.0
        
        for batch_images, batch_labels in tqdm(train_loader, desc=f"Epoca: {epoca+1}/{NUM_EPOCAS}", 
                                               total=len(train_loader)):
            batch_images = batch_images.to(DEVICE)
            batch_labels = batch_labels.to(DEVICE)
            
            optimizer.zero_grad()
            logits = model(batch_images) # inferencia do modelo
            loss = F.cross_entropy(logits, batch_labels) # loss
            loss.backward() 
            optimizer.step()
            
            contagem += 1
            soma_loss += loss.item()
            

        loss_media, acc, dados = evaluate(model, test_loader)
        
        print(f"Epoca: [{epoca+1}/{NUM_EPOCAS}], Loss medio: {soma_loss/len(train_loader):.4f}")
        print(f"Val Loss: {loss_media: .4f}, Val Acc: {acc:.4f}")
        
        historico.append({
            "epoca": epoca+1,
            "loss_medio": soma_loss/len(train_loader),
            "val_loss": loss_media,
            "val_acc": acc
        })
        
        historico_teste.append({
            "epoca": epoca + 1,
            "dados": dados,
        })
        
    from pprint import pprint
    pprint(historico)

    # salvar
    
    with open(model_folder / "historico.json", "w") as f:
        json.dump(historico, f)
    
    with open(model_folder / "historico_teste.json", "w") as f:
        json.dump(historico_teste, f)
