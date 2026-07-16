import os
import urllib.request
import torch

# URL for the Tiny Shakespeare dataset (forked from Andrej Karpathy)
SHAKESPEARE_URL = "https://raw.githubusercontent.com/atilsamancioglu/ShakespeareInput/refs/heads/main/input.txt"
DATA_PATH = "ShakespeareGPT/data/shakespeare.txt"

def download_data():
    if os.path.exists(DATA_PATH):
        print("Dataset already exists.")
        return
    
    os.makedirs("data", exist_ok=True)
    urllib.request.urlretrieve(SHAKESPEARE_URL, DATA_PATH)
    print(f"Downloaded to {DATA_PATH}")


class CharakterTokenizer:
    def __init__(self, text):
        self.characters = sorted(list(set(text)))
        self.vocab_size = len(self.characters)

        self.char_to_id = {}
        for idx, char in enumerate(self.characters):
            self.char_to_id[char] = idx

        self.id_to_char = {}
        for idx, char in enumerate(self.characters):
            self.id_to_char[idx] = char

        print(f"Vocabulary Size: {self.vocab_size} characters")
        print(f"Characters: {(''.join(self.characters))}")
        


    def encode(self, text: str) -> list:
        ids = []
        for char in text:
            ids.append(self.char_to_id[char])
        return ids


    def decode(self, ids: list) -> str:
         
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()

        chars = []
        for id in ids:
            chars.append(self.id_to_char[id])
        return ''.join(chars)

def load_data(train_split: float = 0.9):
    download_data()
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        text = file.read()

    tokenizer = CharakterTokenizer(text)
    
    # örnek 
    """
    print(tokenizer.encode("hello"))  # [46, 43, 50, 50, 53]
    print(tokenizer.decode([46, 43, 50, 50, 53]))  # hello
    """
    
    all_ids = tokenizer.encode(text)
    data = torch.tensor(all_ids, dtype = torch.long)

    split_index = int(train_split * len(data))
    train_data = data[:split_index]
    test_data = data[split_index:]

    print( "-" * 60)
    print(f"train size: {len(train_data)}")
    print(f"test size: {len(test_data)}")


    return train_data, test_data, tokenizer


if __name__ == "__main__":
    train_data, test_data, tokenizer = load_data()