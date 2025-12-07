import hashlib
import re
import requests
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Password Security & Breach Checker", page_icon="🔐")

st.title("🔐 Password Security & Breach Checker")

st.markdown("""
Check how strong your password is and whether it has ever appeared in a known **data breach**.

This app:
- Rates your password strength (length & character variety)
- Checks if your password appears in the **Have I Been Pwned** password database
- Explains **why** a password is considered weak or risky

> ⚠️ Your full password is **never sent** over the network.
> Only the first 5 characters of its **SHA-1 hash** are sent, using the HIBP k-anonymity API.
""")


# ---------------- PASSWORD STRENGTH LOGIC ----------------
def evaluate_password_strength(password: str) -> dict:
    """
    Return a dict with:
      - score (0-100)
      - rating (Weak / Fair / Strong / Very Strong)
      - issues (list of strings)
    """
    issues = []

    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^\w]", password))

    variety_count = sum([has_lower, has_upper, has_digit, has_symbol])

    # Base score from length
    if length == 0:
        score = 0
    elif length < 8:
        score = 20
        issues.append("Password is **short**. Aim for at least 12–14 characters.")
    elif 8 <= length < 12:
        score = 50
        issues.append("Consider using **12+ characters** for stronger security.")
    elif 12 <= length < 16:
        score = 75
    else:
        score = 90  # 16+ chars

    # Adjust score based on character variety
    if variety_count == 1:
        score -= 10
        issues.append("Add **upper, lower, digits, and symbols** for better complexity.")
    elif variety_count == 2:
        issues.append("Add more character types (upper/lower/digits/symbols).")
    elif variety_count >= 3:
        score += 5

    # Clamp score between 0 and 100
    score = max(0, min(score, 100))

    # Determine rating
    if score == 0:
        rating = "No password entered"
    elif score < 40:
        rating = "Weak"
    elif score < 70:
        rating = "Fair"
    elif score < 90:
        rating = "Strong"
    else:
        rating = "Very Strong"

    # Additional hints
    if "password" in password.lower():
        issues.append("Avoid using the word **'password'** or obvious phrases.")
        score = min(score, 40)
        rating = "Weak"

    if re.search(r"(1234|1111|0000|qwerty)", password.lower()):
        issues.append("Avoid common patterns like **1234**, **1111**, or **qwerty**.")
        score = min(score, 40)
        rating = "Weak"

    return {
        "score": score,
        "rating": rating,
        "issues": issues,
        "length": length,
        "variety_count": variety_count,
    }


# ---------------- HIBP BREACH CHECK LOGIC ----------------
def check_pwned(password: str) -> int:
    """
    Check the password against the HaveIBeenPwned password API using k-anonymity.

    Returns:
      - number of times the password has been seen in breaches (0 means not found)
    """
    if not password:
        return 0

    # SHA-1 hash of the password (uppercase hex)
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        # If API fails, we return -1 to indicate an error
        return -1

    # Response is a list of "HASH_SUFFIX:COUNT" lines
    for line in response.text.splitlines():
        hash_suffix, count_str = line.split(":")
        if hash_suffix == suffix:
            return int(count_str)

    return 0


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("How to use")
    st.markdown("""
    1. Enter a password in the field below
    2. Click **Analyze password**
    3. Review **strength**, **breach status**, and **security tips**

    > Use this for **learning and demo purposes** —
    > Don't paste super-sensitive production passwords.
    """)


# ---------------- MAIN INPUT ----------------
password = st.text_input(
    "Enter a password to analyze",
    type="password",
    help="For demo/learning. Avoid using real production passwords.",
)

analyze_clicked = st.button("Analyze password")

if analyze_clicked:
    if not password:
        st.warning("Please enter a password first.")
    else:
        # Evaluate strength
        strength = evaluate_password_strength(password)

        # Show strength summary
        st.subheader("🧱 Password Strength")
        st.metric(
            label="Strength score (0–100)",
            value=strength["score"],
            help="Calculated based on length and character variety.",
        )
        st.write(f"**Rating:** {strength['rating']}")
        st.write(f"**Length:** {strength['length']} characters")
        st.write(f"**Character types used:** {strength['variety_count']} / 4")

        if strength["issues"]:
            st.write("### ⚠️ Improvement Suggestions")
            for issue in strength["issues"]:
                st.write(f"- {issue}")
        else:
            st.success("Nice! This password looks strong from a **complexity** standpoint.")

        st.markdown("---")

        # Check breach status
        st.subheader("🕵️ Breach Exposure Check")

        with st.spinner("Checking Have I Been Pwned (HIBP) database..."):
            breach_count = check_pwned(password)

        if breach_count == -1:
            st.warning(
                "Could not contact the Have I Been Pwned API. "
                "Try again later, or check your internet connection."
            )
        elif breach_count == 0:
            st.success("✅ This password **was not found** in the HIBP database.")
            st.write(
                "That doesn't guarantee it's perfectly safe, but it hasn't appeared "
                "in known public password dumps."
            )
        else:
            st.error(
                f"🚨 This password has appeared in **{breach_count:,}** known data breaches!"
            )
            st.write("""
            You should **never** use this password again.
            Attackers actively use breached passwords in credential stuffing attacks.
            """)

        # Explanation section
        st.markdown("---")
        st.subheader("ℹ️ What this tool teaches")

        st.markdown("""
        - **K-anonymity:** Only the first 5 characters of the SHA-1 hash are sent to HIBP.
          The full password or full hash is never exposed.
        - **Hashing vs Encryption:** Hashing (like SHA-1) is one-way; encryption is reversible with a key.
        - **Credential stuffing:** Attackers reuse breached passwords on other websites to take over accounts.
        - **Best practice:** Use a password manager + unique long passwords per site, plus **MFA** whenever possible.
        """)

# Footer
st.markdown("---")
st.caption(
    "Built by **Your Name** · GitHub: https://github.com/your-username/password-security-checker"
)
