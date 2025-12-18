📁 Project 2: Password Security Checker
🔐 Overview
The Password Security Checker evaluates user passwords against known breach data to help prevent credential reuse and account compromise. The project demonstrates an understanding of identity security, one of the most critical areas in modern security and governance.

🎯 Objectives
Detect compromised credentials


Educate users on password hygiene


Reduce credential-based attack risk


Apply real-world identity security concepts



🛠️ Technologies Used
Python


Have I Been Pwned API


SHA-1 Hashing


K-Anonymity


Streamlit



🔎 How It Works
Password is hashed locally (never sent in plain text)


Hash prefix is queried against breach database


Results indicate if the password has appeared in breaches


User receives actionable security guidance



🧠 Security Principles Applied
Zero-knowledge architecture


Credential hygiene


Privacy-first design


Defense against credential stuffing
🧩 Real-World Use Case
Identity security tools


IAM awareness training


Security awareness platforms


Governance identity controls



🚀 Future Enhancements
MFA recommendations


Password policy enforcement


Enterprise IAM integration


Audit logging for governance reporting



📌 Skills Demonstrated
Identity & access security


Secure API usage


Cryptographic hashing


Privacy-conscious design



























📂 Lab Steps

1. Firstly, I created a Python virtual environment (.src) to isolate dependencies and ensure reproducible development for a cloud security scanning application.











2. Defined and managed application dependencies using requirements.txt, including streamlit and requests, following Python packaging best practices.


















3. .Built a Streamlit-based web application to provide real-time password strength analysis with instant feedback for end users.










4. Implemented a password evaluation engine that analyzes length, character variety (upper, lower, digits, symbols), and assigns a numerical security score (0–100).




5. Integrated Have I Been Pwned (HIBP) breach detection using k-anonymity, hashing passwords with SHA-1, querying only hash prefixes via the HIBP API, and verifying exposure without ever transmitting plaintext credentials.




















6. Designed a secure, user-friendly Streamlit interface with masked password input, guided sidebar instructions, and explicit warnings to prevent users from submitting real production credentials, reinforcing secure handling of sensitive data.



