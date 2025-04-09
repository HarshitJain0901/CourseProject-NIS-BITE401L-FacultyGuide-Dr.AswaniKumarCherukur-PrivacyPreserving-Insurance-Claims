import tenseal as ts
import numpy as np
import joblib
import os
from aes_utils import load_key, decrypt_file, encrypt_file
from blockchain_utils import BlockchainClient
import hashlib

class HEServer:
    def __init__(self):
        self.coefficients = np.load("src/model_coefficients.npy").flatten()
        self.intercept = float(np.load("src/model_intercept.npy"))

    def compute_prediction(self, encrypted_data, context):
        encrypted_vector = ts.ckks_vector_from(context, encrypted_data)

        # Compute "importance" dot product (Random Forest feature_importances_ used here)
        encrypted_dot_product = encrypted_vector.dot(self.coefficients)
        encrypted_dot_product += self.intercept

        # Approximate sigmoid (0.5 + 0.197x)
        encrypted_result = encrypted_dot_product * 0.197
        encrypted_result += 0.5

        return encrypted_result.serialize()

def server_process():
    print("\n=== SERVER PROCESSING ===")
    
    try:
        # 1. Define all file paths
        input_encrypted = "src/encrypted_data.bin.aes"  # Changed from encrypted_result
        temp_decrypted = "src/temp_decrypted.bin"
        output_encrypted = "src/encrypted_result.bin.aes"
        
        # 2. Check if input file exists
        if not os.path.exists(input_encrypted):
            raise FileNotFoundError(f"Input file {input_encrypted} not found")

        # 3. Decrypt input
        key = load_key("src/aes.key")
        decrypt_file(input_encrypted, temp_decrypted, key)

        # 4. Load context and data
        with open("src/public_context.bin", "rb") as f:
            context = ts.context_from(f.read())

        with open(temp_decrypted, "rb") as f:
            encrypted_data = f.read()

        # 5. Compute prediction
        server = HEServer()
        encrypted_result = server.compute_prediction(encrypted_data, context)

        # 6. Save result to temporary file
        temp_result = "src/temp_result.bin"
        with open(temp_result, "wb") as f:
            f.write(encrypted_result)
        
        # 7. Encrypt result and clean up
        encrypt_file(temp_result, output_encrypted, key)
        
        # 8. Blockchain integration
        with open(temp_decrypted, "rb") as f:
            data_hash = hashlib.sha256(f.read()).hexdigest()
        with open(temp_result, "rb") as f:
            result_hash = hashlib.sha256(f.read()).hexdigest()
            
        blockchain = BlockchainClient()
        tx_receipt = blockchain.log_computation(data_hash, result_hash)
        print(f"\n🔗 Blockchain TX Hash: {tx_receipt.hex()}")

        # 9. Clean up temporary files
        os.remove(temp_decrypted)
        os.remove(temp_result)

        print("\n✅ Computation complete. Encrypted result saved to", output_encrypted)

    except Exception as e:
        print(f"\n❌ Server processing failed: {str(e)}")
        # Clean up any partial files
        for f in [temp_decrypted, temp_result]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    server_process()
