# Script pour décrypter le fichier token avec gestion des caractères non imprimables
def decrypt_token(file_path):
    try:
        # Ouvrir et lire le contenu du fichier token en mode binaire
        with open(file_path, "rb") as f:
            encrypted = f.read()  # Lire le contenu en tant qu'octets

        # DÉCRYPTAGE du contenu
        decrypted = ""
        for i, c in enumerate(encrypted):
            char = chr((c - i) % 256)  # Décaler et rester dans la plage [0, 255]
            # Ajouter uniquement les caractères imprimables (ASCII standard)
            if 32 <= ord(char) <= 126:  # Plage des caractères imprimables
                decrypted += char

        return decrypted

    except FileNotFoundError:
        return "Erreur : Le fichier token est introuvable."
    except PermissionError:
        return "Erreur : Permissions insuffisantes pour lire le fichier token."
    except Exception as e:
        return f"Erreur inattendue : {str(e)}"

# Spécifie le chemin du fichier token
file_path = "token"

# Appeler la fonction de décryptage
result = decrypt_token(file_path)
print(f"Contenu décrypté : {result}")
