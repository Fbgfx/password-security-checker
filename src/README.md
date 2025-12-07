# 🔐 Password Security & Breach Checker

A Streamlit app that analyzes password strength and checks whether a password
has appeared in known **data breaches** using the [Have I Been Pwned](https://haveibeenpwned.com/)
password API (k-anonymity model).

## 🎯 What this project demonstrates

- Understanding of **password security fundamentals**
- Use of **hashing (SHA-1)** and **k-anonymity** for privacy-preserving lookups
- Awareness of real-world attack patterns like **credential stuffing**
- Practical use of a public security API from Python

## 🧱 Tech Stack

- Python
- Streamlit (UI)
- `requests` (HTTP calls)
- Have I Been Pwned "Pwned Passwords" API (no API key required for range endpoint)

## 🚀 Getting Started

```bash
git clone https://github.com/<your-username>/password-security-checker.git
cd password-security-checker
pip install -r requirements.txt
streamlit run src/app.py
