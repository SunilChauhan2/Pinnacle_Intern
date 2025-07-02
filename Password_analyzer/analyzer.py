import re
import math
from difflib import get_close_matches
import random
import string

COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "letmein", "admin",
    "welcome", "sunil123", "abc123", "iloveyou", "111111",
    "123123", "password1", "monkey", "dragon", "football"
]

KEYBOARD_PATTERNS = ["qwerty", "asdf", "zxcvbn", "123456", "qazwsx"]

def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/]", password): charset += 32
    return round(len(password) * math.log2(charset), 2) if charset > 0 else 0

def detect_weaknesses(password):
    weaknesses = []
    lower_pwd = password.lower()

    # 1. Common password
    if lower_pwd in COMMON_PASSWORDS or get_close_matches(lower_pwd, COMMON_PASSWORDS):
        weaknesses.append("Uses a common or easily guessable password.")

    # 2. Keyboard pattern
    for pattern in KEYBOARD_PATTERNS:
        if pattern in lower_pwd:
            weaknesses.append(f"Contains a predictable keyboard pattern: '{pattern}'.")

    # 3. Repeated characters
    if re.fullmatch(r'(.)\1{2,}', lower_pwd):  # e.g. "aaaaaa", "111111"
        weaknesses.append("Contains repeated characters.")

    # 4. Sequential characters
    if re.search(r"(0123|1234|2345|3456|4567|5678|6789|7890|abcd|bcde|cdef|defg|efgh)", lower_pwd):
        weaknesses.append("Contains sequential characters.")

    # 5. Short length
    if len(password) < 8:
        weaknesses.append("Password is too short. Use at least 12 characters.")

    return weaknesses

def analyze_password(password):
    results = {}
    results['length'] = len(password)
    results['entropy'] = calculate_entropy(password)
    results['has_upper'] = bool(re.search(r"[A-Z]", password))
    results['has_lower'] = bool(re.search(r"[a-z]", password))
    results['has_digit'] = bool(re.search(r"[0-9]", password))
    results['has_symbol'] = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    results['weaknesses'] = detect_weaknesses(password)

    score = sum([results['has_upper'], results['has_lower'], results['has_digit'], results['has_symbol']])
    if results['length'] < 8:
        results['strength'] = "Weak"
    elif score == 4 and results['length'] >= 12 and not results['weaknesses']:
        results['strength'] = "Very Strong"
    elif score >= 3 and not results['weaknesses']:
        results['strength'] = "Strong"
    else:
        results['strength'] = "Moderate"

    return results

def recommend(password):
    suggestions = []

    if len(password) < 12:
        suggestions.append("- Increase password length to at least 12 characters.")
    if not re.search(r"[A-Z]", password):
        suggestions.append("- Add uppercase letters.")
    if not re.search(r"[a-z]", password):
        suggestions.append("- Add lowercase letters.")
    if not re.search(r"[0-9]", password):
        suggestions.append("- Add digits.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        suggestions.append("- Add special characters.")
    
    # Weakness-specific recommendations
    weaknesses = detect_weaknesses(password)
    for issue in weaknesses:
        if "keyboard" in issue:
            suggestions.append("- Avoid keyboard patterns like 'qwerty' or 'asdf'.")
        if "repeated" in issue:
            suggestions.append("- Avoid using repeated characters.")
        if "sequential" in issue:
            suggestions.append("- Avoid predictable sequences like '1234', 'abcd'.")
        if "common" in issue:
            suggestions.append("- Don’t use common or leaked passwords.")

    if not suggestions:
        suggestions.append("✅ Your password is strong. Good job!")

    return suggestions

def generate_strong_password(length=14):
    if length < 12:
        length = 12  # Enforce secure minimum length

    all_chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choice(all_chars) for _ in range(length))

        # Ensure at least one char from each category
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

