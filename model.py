
import torch.nn as nn
import torch
import random 
from datetime import datetime
import torch.optim as optim
import numpy as np 
from modules import bag_of_words

class ChatNet(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, output_size),
        )

    def forward(self, x):
        return self.net(x)
    
def train_model(intents: dict, vocab: list, epochs: int = 500):
    intent_names = [k for k in intents.keys() if k != "inconnu"]
    X, y = [], []

    for idx, (intent_name, data) in enumerate(intents.items()):
        if intent_name == "inconnu":
            continue
        for pattern in data["patterns"]:
            X.append(bag_of_words(pattern, vocab))
            y.append(intent_names.index(intent_name))

    X_tensor = torch.tensor(np.array(X), dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)

    model = ChatNet(len(vocab), 64, len(intent_names))
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        output = model(X_tensor)
        loss = criterion(output, y_tensor)
        loss.backward()
        optimizer.step()

    model.eval()
    return model, intent_names


def predict_intent(model, sentence: str, vocab: list, intent_names: list, threshold: float = 0.5):
    bow = bag_of_words(sentence, vocab)
    x = torch.tensor(bow, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        output = model(x)
        probs = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probs, dim=1)

    if confidence.item() < threshold:
        return "inconnu", confidence.item()
    return intent_names[predicted.item()], confidence.item()


def get_response(intent_name: str, intents: dict) -> str:
    responses = intents[intent_name]["responses"]
    resp = random.choice(responses)
    if resp == "__heure__":
        now = datetime.now().strftime("%H:%M")
        return f"Il est actuellement {now} ⏰"
    return resp