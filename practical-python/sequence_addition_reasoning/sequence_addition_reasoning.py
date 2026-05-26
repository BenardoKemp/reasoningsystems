import random
import torch
import torch.nn as nn
import torch.optim as optim

# ---------------------------------------------------
# Settings
# ---------------------------------------------------

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MAX_NUMBER = 99
TRAINING_SAMPLES = 5000
EPOCHS = 30
BATCH_SIZE = 64
EMBED_SIZE = 32
HIDDEN_SIZE = 128
LEARNING_RATE = 0.001

# ---------------------------------------------------
# Vocabulary
# ---------------------------------------------------

tokens = [
    "<PAD>", "<SOS>", "<EOS>",
    "0", "1", "2", "3", "4", "5",
    "6", "7", "8", "9",
    "+", "="
]

stoi = {token: i for i, token in enumerate(tokens)}
itos = {i: token for token, i in stoi.items()}

PAD_ID = stoi["<PAD>"]
SOS_ID = stoi["<SOS>"]
EOS_ID = stoi["<EOS>"]

VOCAB_SIZE = len(tokens)

# ---------------------------------------------------
# Data Generation
# ---------------------------------------------------

def generate_example():
    a = random.randint(0, MAX_NUMBER)
    b = random.randint(0, MAX_NUMBER)

    input_text = f"{a}+{b}="
    target_text = str(a + b)

    return input_text, target_text


def encode_input(text, max_len):
    ids = [stoi[ch] for ch in text]
    ids += [PAD_ID] * (max_len - len(ids))
    return ids


def encode_target(text, max_len):
    ids = [SOS_ID] + [stoi[ch] for ch in text] + [EOS_ID]
    ids += [PAD_ID] * (max_len - len(ids))
    return ids


def create_dataset(num_samples):
    examples = [generate_example() for _ in range(num_samples)]

    max_input_len = max(len(x[0]) for x in examples)
    max_target_len = max(len(x[1]) + 2 for x in examples)

    X = []
    y = []

    for input_text, target_text in examples:
        X.append(encode_input(input_text, max_input_len))
        y.append(encode_target(target_text, max_target_len))

    return torch.tensor(X), torch.tensor(y), max_input_len, max_target_len


X, y, MAX_INPUT_LEN, MAX_TARGET_LEN = create_dataset(TRAINING_SAMPLES)

X = X.to(DEVICE)
y = y.to(DEVICE)

# ---------------------------------------------------
# Encoder
# ---------------------------------------------------

class Encoder(nn.Module):

    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            embed_size,
            padding_idx=PAD_ID
        )

        self.gru = nn.GRU(
            embed_size,
            hidden_size,
            batch_first=True
        )

    def forward(self, x):
        embedded = self.embedding(x)
        outputs, hidden = self.gru(embedded)
        return hidden


# ---------------------------------------------------
# Decoder
# ---------------------------------------------------

class Decoder(nn.Module):

    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            embed_size,
            padding_idx=PAD_ID
        )

        self.gru = nn.GRU(
            embed_size,
            hidden_size,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden):
        embedded = self.embedding(x)

        output, hidden = self.gru(
            embedded,
            hidden
        )

        logits = self.fc(output)

        return logits, hidden


# ---------------------------------------------------
# Seq2Seq Model
# ---------------------------------------------------

class Seq2Seq(nn.Module):

    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()

        self.encoder = Encoder(
            vocab_size,
            embed_size,
            hidden_size
        )

        self.decoder = Decoder(
            vocab_size,
            embed_size,
            hidden_size
        )

    def forward(self, source, target):

        target_len = target.size(1)

        hidden = self.encoder(source)

        decoder_input = target[:, 0].unsqueeze(1)

        outputs = []

        for t in range(1, target_len):

            logits, hidden = self.decoder(
                decoder_input,
                hidden
            )

            outputs.append(logits)

            decoder_input = target[:, t].unsqueeze(1)

        return torch.cat(outputs, dim=1)


model = Seq2Seq(
    VOCAB_SIZE,
    EMBED_SIZE,
    HIDDEN_SIZE
).to(DEVICE)

criterion = nn.CrossEntropyLoss(
    ignore_index=PAD_ID
)

optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)

# ---------------------------------------------------
# Training
# ---------------------------------------------------

for epoch in range(EPOCHS):

    permutation = torch.randperm(X.size(0))

    total_loss = 0

    for i in range(0, X.size(0), BATCH_SIZE):

        indices = permutation[i:i + BATCH_SIZE]

        batch_x = X[indices]
        batch_y = y[indices]

        optimizer.zero_grad()

        outputs = model(batch_x, batch_y)

        loss = criterion(
            outputs.reshape(-1, VOCAB_SIZE),
            batch_y[:, 1:].reshape(-1)
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / (X.size(0) // BATCH_SIZE)

    print(
        f"Epoch {epoch + 1}/{EPOCHS}, "
        f"Loss: {avg_loss:.4f}"
    )

# ---------------------------------------------------
# Inference
# ---------------------------------------------------

def predict(expression):

    model.eval()

    encoded = encode_input(
        expression,
        MAX_INPUT_LEN
    )

    source = torch.tensor([encoded]).to(DEVICE)

    hidden = model.encoder(source)

    decoder_input = torch.tensor(
        [[SOS_ID]]
    ).to(DEVICE)

    result = []

    with torch.no_grad():

        for _ in range(MAX_TARGET_LEN):

            logits, hidden = model.decoder(
                decoder_input,
                hidden
            )

            predicted_id = logits.argmax(dim=-1).item()

            if predicted_id == EOS_ID:
                break

            result.append(itos[predicted_id])

            decoder_input = torch.tensor(
                [[predicted_id]]
            ).to(DEVICE)

    return "".join(result)

# ---------------------------------------------------
# Test Examples
# ---------------------------------------------------

test_expressions = [
    "3+4=",
    "10+15=",
    "27+8=",
    "45+32=",
    "99+99="
]

print("\nTest Results")
print("--------------------")

for expr in test_expressions:

    prediction = predict(expr)

    actual = eval(expr.replace("=", ""))

    print(
        f"{expr} predicted: {prediction} "
        f"| actual: {actual}"
    )