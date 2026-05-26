import torch
import torch.nn as nn
import torch.optim as optim

# ---------------------------------------------------
# Training Data
# ---------------------------------------------------
# Each row:
# [number1, number2]
#
# Target:
# number1 + number2
# ---------------------------------------------------

X = torch.tensor([
    [1.0, 2.0],
    [2.0, 3.0],
    [3.0, 4.0],
    [4.0, 5.0],
    [5.0, 6.0],
    [6.0, 7.0],
    [7.0, 8.0],
    [8.0, 9.0]
])

y = torch.tensor([
    [3.0],
    [5.0],
    [7.0],
    [9.0],
    [11.0],
    [13.0],
    [15.0],
    [17.0]
])

# ---------------------------------------------------
# Neural Network
# ---------------------------------------------------
# 2 inputs  -> two numbers
# 8 neurons -> hidden layer
# 1 output  -> predicted sum
# ---------------------------------------------------

model = nn.Sequential(
    nn.Linear(2, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)

# ---------------------------------------------------
# Loss Function + Optimizer
# ---------------------------------------------------

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# ---------------------------------------------------
# Training Loop
# ---------------------------------------------------

epochs = 2000

for epoch in range(epochs):

    # Forward pass
    predictions = model(X)

    # Calculate error
    loss = criterion(predictions, y)

    # Clear previous gradients
    optimizer.zero_grad()

    # Backpropagation
    loss.backward()

    # Update weights
    optimizer.step()

    # Print progress
    if epoch % 200 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.6f}")

# ---------------------------------------------------
# Test the model
# ---------------------------------------------------

test_input = torch.tensor([[10.0, 15.0]])

with torch.no_grad():
    predicted_sum = model(test_input)

print("\nTest Result")
print("------------------")
print(f"Input Numbers : 10 and 15")
print(f"Predicted Sum : {predicted_sum.item():.2f}")