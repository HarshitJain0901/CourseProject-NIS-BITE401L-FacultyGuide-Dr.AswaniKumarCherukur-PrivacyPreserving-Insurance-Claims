import tenseal as ts
import numpy as np
import pandas as pd
import joblib
import os
from aes_utils import generate_key, load_key, encrypt_file, decrypt_file
from sklearn.metrics import accuracy_score, classification_report

# === CONFIGURATION ===
TEST_DATA_PATH = "data/Insurance.csv"
MODEL_PATH = "src/model_coefficients.npy"
INTERCEPT_PATH = "src/model_intercept.npy"
PREPROCESSOR_PATH = "src/preprocessor.joblib"
AES_KEY_PATH = "src/aes.key"

# === HELPER FUNCTIONS ===

def sigmoid_approx(x):
    """3rd degree polynomial sigmoid approximation."""
    return 0.5 + 0.197 * x - 0.004 * x ** 3

def simulate_client_encryption(data_row, context, preprocessor, key):
    processed = preprocessor.transform(data_row)
    vector = np.array(processed).flatten()
    encrypted = ts.ckks_vector(context, vector)

    with open("src/encrypted_data.bin", "wb") as f:
        f.write(encrypted.serialize())
    encrypt_file("src/encrypted_data.bin", "src/encrypted_data.bin.aes", key)
    os.remove("src/encrypted_data.bin")

def simulate_server_prediction(context, key, coefficients, intercept):
    decrypt_file("src/encrypted_data.bin.aes", "src/encrypted_data.bin", key)
    with open("src/encrypted_data.bin", "rb") as f:
        encrypted_data = f.read()
    os.remove("src/encrypted_data.bin")
    os.remove("src/encrypted_data.bin.aes")

    encrypted_vector = ts.ckks_vector_from(context, encrypted_data)
    encrypted_dot = encrypted_vector.dot(coefficients)
    encrypted_dot += intercept
    raw_output = encrypted_dot.decrypt()[0]
    return raw_output

# === MAIN EVALUATION FUNCTION ===

def evaluate_model_on_test_set():
    print("\n=== 🔐 HOMOMORPHIC ENCRYPTION EVALUATION ===")

    # Load data and model
    test_data = pd.read_csv(TEST_DATA_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    coefficients = np.load(MODEL_PATH).flatten()
    intercept = float(np.load(INTERCEPT_PATH))
    y_true = test_data["insuranceclaim"]
    X_test = test_data.drop(columns=["insuranceclaim"])

    # Create encryption context
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()

    # Save contexts for compatibility
    os.makedirs("src", exist_ok=True)
    with open("src/private_context.bin", "wb") as f:
        f.write(context.serialize(save_secret_key=True))
    public_context = context.copy()
    public_context.make_context_public()
    with open("src/public_context.bin", "wb") as f:
        f.write(public_context.serialize())

    if not os.path.exists(AES_KEY_PATH):
        generate_key(AES_KEY_PATH)
    key = load_key(AES_KEY_PATH)

    # Evaluation loop
    predictions = []
    for idx, row in X_test.iterrows():
        row_df = pd.DataFrame([row])

        simulate_client_encryption(row_df, context, preprocessor, key)
        raw_output = simulate_server_prediction(context, key, coefficients, intercept)
        probability = sigmoid_approx(raw_output)
        predicted_class = int(probability >= 0.5)
        predictions.append(predicted_class)

        print(f"\n🧪 Test #{idx + 1}")
        print(f"🔢 Raw output: {raw_output:.4f}")
        print(f"📈 Approximated probability: {probability:.4f}")
        print(f"🎯 Prediction: {'Claim Approved' if predicted_class else 'Claim Denied'}")
        print(f"✅ Actual: {'Claim Approved' if y_true.iloc[idx] else 'Claim Denied'}")

    # Evaluation report
    acc = accuracy_score(y_true, predictions)
    print(f"\n✅ Model Accuracy: {acc * 100:.2f}%")
    print("\n📋 Classification Report:")
    print(classification_report(y_true, predictions, target_names=["Denied", "Approved"]))

if __name__ == '__main__':
    evaluate_model_on_test_set()
