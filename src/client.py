import tenseal as ts
import numpy as np
import pandas as pd
import joblib
import os
import hashlib
from aes_utils import generate_key, load_key, encrypt_file, decrypt_file
from blockchain_utils import BlockchainClient

def get_user_input():
    print("\nEnter the following details:")
    return pd.DataFrame({
        'age': [int(input("Age: "))],
        'sex': [int(input("Sex (0 = female, 1 = male): "))],
        'bmi': [float(input("BMI: "))],
        'children': [int(input("Number of children: "))],
        'smoker': [int(input("Smoker (0 = no, 1 = yes): "))],
        'region': [int(input("Region (0 = southwest, 1 = southeast, 2 = northwest, 3 = northeast): "))],
        'charges': [float(input("Recent medical charges: "))]
    })

class HEClient:
    def __init__(self):
        self.context = None
        self.public_context = None

    def generate_keys(self):
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        context.global_scale = 2**40
        context.generate_galois_keys()
        self.context = context
        self.public_context = context.copy()
        self.public_context.make_context_public()

    def encrypt_data(self, data):
        vector = np.array(data).flatten()
        encrypted = ts.ckks_vector(self.context, vector)
        return encrypted.serialize()

def encrypt_mode():
    print("\n=== ENCRYPTION MODE ===")
    client = HEClient()
    client.generate_keys()

    # Setup AES encryption
    key_path = "src/aes.key"
    if not os.path.exists(key_path):
        generate_key(key_path)
    key = load_key(key_path)

    # Save TenSEAL contexts
    with open("src/private_context.bin", "wb") as f:
        f.write(client.context.serialize(save_secret_key=True))
    with open("src/public_context.bin", "wb") as f:
        f.write(client.public_context.serialize())

    # Process user input
    sample = get_user_input()
    preprocessor = joblib.load("src/preprocessor.joblib")
    processed = preprocessor.transform(sample)

    # Encrypt and save data (changed from encrypted_result to encrypted_data)
    encrypted_data = client.encrypt_data(processed)
    with open("src/encrypted_data.bin", "wb") as f:  # Changed filename
        f.write(encrypted_data)
    encrypt_file("src/encrypted_data.bin", "src/encrypted_data.bin.aes", key)  # Changed filename

    # Blockchain integration
    try:
        blockchain = BlockchainClient()
        with open("src/encrypted_data.bin", "rb") as f:  # Changed filename
            data_hash = hashlib.sha256(f.read()).hexdigest()
        
        tx_receipt = blockchain.log_computation(
            data_hash=data_hash,
            result_hash="0"*64  # Placeholder for pending result
        )
        print(f"\n🔗 Blockchain TX Hash: {tx_receipt.hex()}")
    except Exception as e:
        print(f"\n⚠️ Blockchain error: {str(e)}")

    print("\nEncryption complete. Files saved:")
    print("- private_context.bin")
    print("- public_context.bin")
    print("- encrypted_result.bin.aes")
    print("- aes.key")

def verify_integrity():
    """Full end-to-end integrity check"""
    try:
        # 1. Load current result hash
        with open("src/encrypted_result.bin", "rb") as f:
            current_result_hash = hashlib.sha256(f.read()).hexdigest()
        
        # 2. Get original data hash from blockchain
        blockchain = BlockchainClient()
        original_data_hash = blockchain.get_original_data_hash(current_result_hash)
        if not original_data_hash:
            raise ValueError("No matching computation record found")
        
        # 3. Recompute data hash from original file
        with open("src/encrypted_data.bin", "rb") as f:
            recomputed_data_hash = hashlib.sha256(f.read()).hexdigest()
        
        # 4. Verify all conditions
        hash_match = (recomputed_data_hash == original_data_hash)
        blockchain_valid = blockchain.verify_computation(original_data_hash, current_result_hash)
        
        return hash_match and blockchain_valid
        
    except Exception as e:
        print(f"Integrity verification failed: {str(e)}")
        return False    

def decrypt_mode():
    print("\n=== DECRYPTION MODE ===")
    try:
        key = load_key("src/aes.key")
        decrypt_file("src/encrypted_result.bin.aes", "src/encrypted_result.bin", key)

        with open("src/private_context.bin", "rb") as f:
            context = ts.context_from(f.read())

        with open("src/encrypted_result.bin", "rb") as f:
            encrypted_result = ts.ckks_vector_from(context, f.read())

        prediction = max(0.0, min(1.0, encrypted_result.decrypt()[0]))
        print(f"\n🔍 Model output (probability): {prediction:.4f}")
        print("✅ Claim Approved" if prediction >= 0.5 else "❌ Claim Denied")

        # Verify on blockchain
        try:
            blockchain = BlockchainClient()
            # Get original data hash from blockchain
            with open("src/encrypted_data.bin", "rb") as f:
                data_hash = hashlib.sha256(f.read()).hexdigest()
            # Get result hash
            with open("src/encrypted_result.bin", "rb") as f:
                result_hash = hashlib.sha256(f.read()).hexdigest()
            
            is_valid = blockchain.verify_computation(data_hash, result_hash)
            print(f"\n🔗 Blockchain Verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
        except Exception as e:
            print(f"\n⚠️ Blockchain verification failed: {str(e)}")

    except Exception as e:
        print(f"\n❌ Decryption failed: {str(e)}")
    finally:
        if os.path.exists("src/encrypted_result.bin"):
            os.remove("src/encrypted_result.bin")

if __name__ == '__main__':
    print("1. Encrypt data")
    print("2. Decrypt result")
    choice = input("Enter choice (1/2): ")
    
    if choice == '1':
        encrypt_mode()
    elif choice == '2':
        decrypt_mode()
    else:
        print("Invalid choice.")