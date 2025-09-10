# Lire le token depuis le fichier
with open("token", "rb") as f:
    token = f.read()

# Fonction pour décoder le token
def decode_token(token):
    decoded = ""
    for i, byte in enumerate(token[:25]):
        # Soustraire l'index i et appliquer modulo 256 pour éviter les valeurs négatives
        decoded_value = (byte - i) % 256
        decoded_char = chr(decoded_value)
        decoded += decoded_char
    return decoded

# Décoder et afficher le résultat
decoded_token = decode_token(token)
print("Token décodé :", decoded_token)