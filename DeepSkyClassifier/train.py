import pandas as pd
import torch 
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from model import DeepSkyClassifier
from pathlib import Path  # model kayıt için
import joblib

df = pd.read_csv("DeepSkyClassifier/data/stars.csv")
df = df.rename(columns={
    'Temperature (K)': 'temperature',
    'Luminosity(L/Lo)': 'luminosity',
    'Radius(R/Ro)': 'radius',
    'Absolute magnitude(Mv)': 'magnitude',
    'Star type': 'type',
    'Star color': 'color',
    'Spectral Class': 'spectralClass'
})

le_color = LabelEncoder()
df["color"] = le_color.fit_transform(df["color"])

le_spectral = LabelEncoder()
df["spectralClass"] = le_spectral.fit_transform(df["spectralClass"])

X_raw = df.drop("type", axis=1) 
y = df["type"].values

scaler = StandardScaler()
X = scaler.fit_transform(X_raw) 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)

y_train = torch.tensor(y_train, dtype=torch.long)  
y_test = torch.tensor(y_test, dtype=torch.long) 


model = DeepSkyClassifier()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=0.001)

def calculate_accuracy(y_test, y_pred):
    correct = torch.eq(y_test, y_pred).sum().item()
    accuracy = correct / len(y_test) * 100
    return accuracy

epochs = 1400
for epoch in range(epochs):
    model.train()
    logits = model(X_train)
    y_pred = torch.softmax(logits, dim=1).argmax(dim=1)
    accuracy = calculate_accuracy(y_train, y_pred)

    loss = loss_fn(logits, y_train)
    optimizer.zero_grad()

    loss.backward()
    optimizer.step()

    model.eval()
    with torch.inference_mode():
        test_logits = model(X_test)
        test_loss = loss_fn(test_logits, y_test)
        test_pred = torch.softmax(test_logits, dim=1).argmax(dim=1)
        test_acc = calculate_accuracy(y_test, test_pred)

    if epoch % 20 == 0:
        print(f"Epoch: {epoch}, Loss: {loss:.2f}, Acc: {accuracy:.2f} -- Test Loss: {test_loss:.2f}, Test Accuracy: {test_acc:.2f}, ")


MODEL_PATH = Path("DeepSkyClassifier/models")
MODEL_PATH.mkdir(parents=True, exist_ok=True) 

MODEL_NAME = "star_model.pth"
MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME
torch.save(obj=model.state_dict(), f=MODEL_SAVE_PATH)

# 3. Preprocessing nesnelerini kaydet (Tercümanlar)
joblib.dump(scaler, MODEL_PATH / "scaler.pkl")
joblib.dump(le_color, MODEL_PATH / "le_color.pkl")
joblib.dump(le_spectral, MODEL_PATH / "le_spectral.pkl")