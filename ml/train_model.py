import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


# Training data
data = [
    [500, 8, 12, "bank_transfer", 10, 0],
    [1200, 10, 14, "bank_transfer", 12, 0],
    [2500, 9, 13, "card_payment", 8, 0],
    [5000, 11, 16, "bank_transfer", 15, 0],
    [8000, 12, 14, "card_payment", 12, 0],
    [12000, 10, 15, "online_payment", 10, 0],
    [18000, 9, 14, "bank_transfer", 12, 0],
    [22000, 11, 16, "mobile_wallet", 10, 0],

    [50000, 2, 4, "online_payment", 2, 1],
    [75000, 2, 5, "mobile_wallet", 3, 1],
    [100000, 1, 4, "online_payment", 2, 1],
    [150000, 2, 5, "mobile_wallet", 2, 1],
    [200000, 1, 3, "online_payment", 1, 1],
    [300000, 2, 4, "online_payment", 2, 1],

    [45000, 3, 5, "mobile_wallet", 4, 1],
    [90000, 4, 5, "online_payment", 3, 1],

    [3000, 8, 12, "bank_transfer", 8, 0],
    [7000, 9, 13, "card_payment", 9, 0],
    [15000, 10, 14, "bank_transfer", 11, 0],
    [25000, 8, 12, "card_payment", 10, 0],
]


# Create DataFrame
columns = [
    "amount",
    "receiver_length",
    "account_length",
    "transaction_type",
    "purpose_length",
    "fraud",
]

df = pd.DataFrame(data, columns=columns)


# Convert transaction type into numbers
encoder = LabelEncoder()

df["transaction_type"] = encoder.fit_transform(
    df["transaction_type"]
)


# Features
X = df[
    [
        "amount",
        "receiver_length",
        "account_length",
        "transaction_type",
        "purpose_length",
    ]
]


# Target
y = df["fraud"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)


# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)


# Train model
model.fit(X_train, y_train)


# Test model
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions,
)


print("--------------------------------")
print("ShieldPay AI ML Model")
print("--------------------------------")

print(
    f"Model Accuracy: {accuracy * 100:.2f}%"
)


# Save trained model
joblib.dump(
    model,
    "ml/fraud_model.pkl",
)


# Save encoder
joblib.dump(
    encoder,
    "ml/transaction_type_encoder.pkl",
)


print("--------------------------------")
print("Model saved successfully!")


