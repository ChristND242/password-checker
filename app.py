import streamlit as st
import hashlib
import requests
import re
import random

# Define translations for French and English
translations = {
    'fr': {
        'title': "Analyseur de la force du mot de passe avec détection de violation by C.ND",
        'enter_password': "Entrez votre mot de passe :",
        'show_password': "Afficher le mot de passe",
        'password_strength': "Force du mot de passe :",
        'password_entropy': "Entropie du mot de passe :",
        'feedback': "Retour d'information :",
        'safe_password': "Votre mot de passe est sûr et n'a pas été trouvé dans des violations de données.",
        'breached_password': "Votre mot de passe a été trouvé dans une violation de données !",
        'expiry_suggestion': "Suggestion de changement de mot de passe :",
        'generate_password': "Générer un mot de passe plus fort",
        'select_length': "Sélectionnez la longueur du mot de passe :",
        'generated_password': "Mot de passe généré :",
        'security_tip': "Conseil de sécurité du jour :",
        'password_expiry_12_months': "Suggéré de changer tous les 12 mois.",
        'password_expiry_6_months': "Suggéré de changer tous les 6 mois.",
        'password_expiry_3_months': "Suggéré de changer tous les 3 mois.",
        'security_tips': [
            "Utilisez un gestionnaire de mots de passe pour stocker vos mots de passe en toute sécurité.",
            "Activez l'authentification à deux facteurs (2FA) pour plus de sécurité.",
            "Évitez d'utiliser le même mot de passe pour plusieurs comptes.",
            "Vérifiez régulièrement si vos mots de passe ont été impliqués dans des violations.",
            "Utilisez des mots de passe longs et complexes avec un mélange de caractères, de chiffres et de symboles."
        ]
    },
    'en': {
        'title': "Password Strength Analyzer with Breach Detection by C.ND",
        'enter_password': "Enter your password:",
        'show_password': "Show password",
        'password_strength': "Password strength:",
        'password_entropy': "Password entropy:",
        'feedback': "Feedback:",
        'safe_password': "Your password is safe and has not been found in any data breaches.",
        'breached_password': "Your password has been found in a data breach!",
        'expiry_suggestion': "Password expiry suggestion:",
        'generate_password': "Generate a stronger password",
        'select_length': "Select password length:",
        'generated_password': "Generated password:",
        'security_tip': "Security Tip of the Day:",
        'password_expiry_12_months': "Suggested to change every 12 months.",
        'password_expiry_6_months': "Suggested to change every 6 months.",
        'password_expiry_3_months': "Suggested to change every 3 months.",
        'security_tips': [
            "Use a password manager to store your passwords securely.",
            "Enable two-factor authentication (2FA) for extra security.",
            "Avoid using the same password for multiple accounts.",
            "Regularly check if your passwords have been involved in breaches.",
            "Use long, complex passwords with a mix of characters, numbers, and symbols."
        ]
    }
}

# Function to select the language
def get_translation(lang_code, key):
    return translations[lang_code][key]

# Set default language as French
selected_language = st.sidebar.selectbox("Select Language / Sélectionnez la langue", ['fr', 'en'], index=0)

# Helper functions
def check_password_strength(password, lang_code):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Le mot de passe doit comporter au moins 12 caractères." if lang_code == 'fr' else "Password should be at least 12 characters long.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Le mot de passe doit inclure au moins une lettre majuscule." if lang_code == 'fr' else "Password should include at least one uppercase letter.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Le mot de passe doit inclure au moins une lettre minuscule." if lang_code == 'fr' else "Password should include at least one lowercase letter.")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Le mot de passe doit inclure au moins un chiffre." if lang_code == 'fr' else "Password should include at least one number.")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Le mot de passe doit inclure au moins un caractère spécial." if lang_code == 'fr' else "Password should include at least one special character.")

    common_passwords = ['password', '12345', 'qwerty']
    if any(common in password.lower() for common in common_passwords):
        feedback.append("Évitez d'utiliser des mots ou des motifs courants comme 'mot de passe' ou '12345'." if lang_code == 'fr' else "Avoid using common words or patterns like 'password' or '12345'.")

    return score, feedback

def check_breach(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if suffix in response.text:
        return True  # Breached
    return False  # Safe

def calculate_entropy(password):
    charset_size = len(set(password))
    entropy = len(password) * (charset_size).bit_length()
    return entropy

def password_expiry(score, lang_code):
    if score >= 4:
        return get_translation(lang_code, 'password_expiry_12_months')
    elif score == 3:
        return get_translation(lang_code, 'password_expiry_6_months')
    else:
        return get_translation(lang_code, 'password_expiry_3_months')

def generate_password(length=16):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()?"
    return ''.join(random.choice(characters) for _ in range(length))

# Streamlit UI
lang_code = selected_language

st.title(get_translation(lang_code, 'title'))

password = st.text_input(get_translation(lang_code, 'enter_password'), type="password")
show_password = st.checkbox(get_translation(lang_code, 'show_password'))

if show_password:
    st.text(password)

if password:
    score, feedback = check_password_strength(password, lang_code)
    breached = check_breach(password)
    entropy = calculate_entropy(password)
    expiry_suggestion = password_expiry(score, lang_code)

    st.write(f"{get_translation(lang_code, 'password_strength')} {score}/5")
    st.write(f"{get_translation(lang_code, 'password_entropy')} {entropy} bits")

    if feedback:
        st.write(f"{get_translation(lang_code, 'feedback')}")
        for msg in feedback:
            st.write(f"- {msg}")
    
    if breached:
        st.error(get_translation(lang_code, 'breached_password'))
    else:
        st.success(get_translation(lang_code, 'safe_password'))
    
    st.write(f"{get_translation(lang_code, 'expiry_suggestion')} {expiry_suggestion}")

    # Password generation tool
    st.write(get_translation(lang_code, 'generate_password'))
    password_length = st.slider(get_translation(lang_code, 'select_length'), min_value=8, max_value=32, value=16)
    generated_password = generate_password(password_length)
    st.text(f"{get_translation(lang_code, 'generated_password')} {generated_password}")

    # Security Tip of the Day
    security_tips = get_translation(lang_code, 'security_tips')
    st.write(f"{get_translation(lang_code, 'security_tip')} {random.choice(security_tips)}")
