# Blockchain-Based Privacy-Preserving Medical Insurance Claim Processing using Homomorphic Encryption

Course Title: Network and Information Security

Course Code: BITE401L

Institution: VIT Vellore

Department: SCORE

Faculty Guide: Dr. Aswani Kumar Cherukuri

---
## 🧠 Project Overview

This project implements a **Blockchain-integrated privacy-preserving medical insurance claim verification system** using **Homomorphic Encryption**. It allows secure verification of encrypted medical data for insurance claims without compromising patient privacy.

### 🔐 Core Technologies:
- **Blockchain (Ethereum, Truffle, Ganache)** for integrity and tamper-proof storage.
- **Homomorphic Encryption (CKKS via TenSEAL)** for privacy-preserving computation.
- **SHA-256 Hashing** for integrity verification.
- **AES Encryption** for secure off-chain file encryption.

---

## 🛠️ Features

- ✅ End-to-end encryption of patient data using CKKS scheme.
- ✅ Blockchain-based verification of data integrity and timestamp.
- ✅ Model inference on encrypted data for insurance approval/denial.
- ✅ Off-chain storage with tamper detection using stored hash comparison.
- ✅ CLI interface for data submission and result decryption.

---

## 📊 Workflow

1. User inputs medical details through the CLI.
2. Data is encrypted using CKKS and AES and then hashed (SHA-256).
3. The SHA-256 hash and metadata are stored on the blockchain.
4. Encrypted files are stored off-chain (e.g., local/IPFS/S3).
5. On retrieval, AES decrypts the file, and hash is recomputed.
6. If the hash matches, integrity is verified. Otherwise, tampering is detected.

🚀 Getting Started

🔧 Prerequisites

Python 3.8+

Ganache

Node.js & Truffle

TenSEAL

OpenFHE (if experimenting with BGV/BFV)

⚙️ Setup
# Clone the repository
git clone https://github.com/HarshitJain0901/BITE401L-Privacy-Preserving-Insurance-Claims.git

cd BITE401L-Privacy-Preserving-Insurance-Claims

# Install dependencies
npm install
pip install -r requirements.txt

# Start local Ethereum node
ganache-cli

# Deploy smart contract
truffle migrate --network development

# Run the client
python src/client.py
