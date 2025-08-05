# 🔒 Privacy-Preserving Medical Insurance Claim Processing

![Blockchain](https://img.shields.io/badge/Blockchain-Ethereum-blue)
![Homomorphic Encryption](https://img.shields.io/badge/Homomorphic%20Encryption-CKKS-green)
![Python](https://img.shields.io/badge/Python-Backend-yellow)
![Solidity](https://img.shields.io/badge/Smart%20Contracts-Solidity-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

A **decentralized, privacy-preserving medical insurance claim processing system** that leverages:

- **Homomorphic Encryption (HE)** to perform computations directly on encrypted patient data.  
- **Blockchain (Ethereum)** to maintain **immutable claim logs** and **audit trails**.  
- **Smart Contracts** to **automate claim verification** and **prevent fraud**.

This system ensures **end-to-end confidentiality, integrity, and transparency** for all stakeholders — patients, hospitals, and insurers.

---

## 📌 Key Features

- 🔹 **End-to-End Data Privacy**: Claims are processed **without ever decrypting patient data** using **CKKS homomorphic encryption**.  
- 🔹 **Decentralized & Tamper-Proof**: Uses **Ethereum blockchain** to store **data and result hashes** for verifiable integrity.  
- 🔹 **Smart Contract Automation**: Eliminates manual verification delays and **prevents fraudulent claims**.  
- 🔹 **Immutable Audit Trail**: All claim transactions are **traceable and auditable**.  
- 🔹 **Privacy + Transparency**: Combines **AES for transport security** and **homomorphic encryption** for computation.  

---

## 🏗 System Architecture

The system integrates **clients, hospitals, insurers, and blockchain nodes** into a **secure claim processing pipeline**:

<img width="503" height="363" alt="image" src="https://github.com/user-attachments/assets/1a5b373a-be56-4548-adda-1af20e6fb923" />


**Workflow Overview:**

1. **Patient/Hospital** encrypts medical records using **CKKS + AES**.  
2. **Smart Contract** logs the data hash to blockchain.  
3. **Server** computes claim decision on **encrypted data**.  
4. **Blockchain** immutably stores result hash for verification.  
5. **Client** decrypts final decision and verifies hash integrity.  

---

## 🛠 Technology Stack

| Component                   | Technology Used                    |
|-----------------------------|------------------------------------|
| **Blockchain Platform**      | Ethereum (Ganache + Truffle)       |
| **Smart Contracts**          | Solidity                           |
| **Backend / Encryption**     | Python + TenSEAL (CKKS)            |
| **Data Transmission**        | AES (Advanced Encryption Standard) |
| **Verification & Audit**     | SHA-256 Hashing + Blockchain       |

---

## ⚡ End-to-End Workflow

The end-to-end claim workflow:

1. **Blockchain & Smart Contract Setup**
   - Deploy smart contract for **hash logging & verification**.  
2. **Client-Side Data Encryption**
   - Encrypt medical records with **CKKS + AES**.  
3. **Blockchain Logging**
   - Log **data hash** to blockchain.  
4. **Server-Side Homomorphic Evaluation**
   - Compute claim decision on **encrypted data**.  
5. **Result Hashing & Logging**
   - Store **result hash** on blockchain for verification.  
6. **Client Verification**
   - Decrypt results and verify **integrity using hashes**.


<img width="522" height="962" alt="image" src="https://github.com/user-attachments/assets/c5c36248-6e67-4a04-a591-41f5688d40b0" />


---

## 📊 Performance Metrics

| Metric                         | Value               |
|--------------------------------|--------------------|
| **Data Encryption Time**        | ~0.35 sec/record   |
| **Encrypted Claim Processing**  | ~2.4 sec/claim     |
| **Result Decryption Time**      | ~0.22 sec/result   |
| **Smart Contract Execution**    | ~1.1 sec           |
| **Blockchain Throughput**       | ~25–30 tx/sec      |
| **Storage Overhead**            | ~2.3x plaintext    |

---

## 📈 Privacy Guarantees

| Scenario                         | Privacy Outcome                     |
|----------------------------------|-------------------------------------|
| **Encrypted Data Transmission**  | Fully secure (AES)                  |
| **Server-Side Computation**      | Fully secure (Homomorphic Encryption)|
| **Blockchain Logging**           | Stores **hashes only**, no PHI       |

---

---

## 🎥 Demo Workflow

1. **Blockchain Server Initialization and Smart Contract Deployment**
   <img width="503" height="390" alt="image" src="https://github.com/user-attachments/assets/b67e8b15-06fa-477c-a22a-1e11d828c1d7" />

2. **Client-Side Medical Data Encryption and Transmission**
   <img width="503" height="192" alt="image" src="https://github.com/user-attachments/assets/97be71bd-0c62-4c29-95bc-8472fbb91b4a" />

3. **Hash Logging on the Blockchain Server**
   
   <img width="503" height="294" alt="image" src="https://github.com/user-attachments/assets/383ef905-b7bd-49f9-bb9e-4cdbd531e55e" />

5. **Secure Server-Side Homomorphic Processing**
   <img width="503" height="60" alt="image" src="https://github.com/user-attachments/assets/895c0c3c-8edc-4c81-acda-004131ec88c5" />

6. **Result Hashing and Update on Blockchain**
    <img width="503" height="90" alt="image" src="https://github.com/user-attachments/assets/116b02d0-092c-4ed5-ad01-73970af4b440" />

7. **Client-Side Result Retrieval and Integrity Verification**
    <img width="503" height="96" alt="image" src="https://github.com/user-attachments/assets/2e063f6d-316a-47ea-ba74-ea8ac959d268" />

---

## 🚀 Future Enhancements

- ✅ Public blockchain integration for **cross-institutional trust**  
- ✅ Integration with **secure federated learning** for model updates  
- ✅ Deployment of **vibration alerts or push notifications** for claim events


