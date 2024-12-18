# README - Exploitation du binaire level09

## Étapes suivies pour obtenir le Flag09

### 1. Identification des fichiers

Le répertoire contient deux fichiers principaux :

```bash
level09@SnowCrash:~$ ls -l
total 12
-rwsr-sr-x 1 flag09 level09 7640 Mar  5  2016 level09
----r--r-- 1 flag09 level09   26 Mar  5  2016 token
```

- **`level09`** : Un exécutable avec les permissions `setuid` et `setgid`, ce qui signifie qu'il s'exécute avec les privilèges de l'utilisateur `flag09`.
- **`token`** : Un fichier contenant un contenu transformé de manière indéchiffrable directement, mais qui peut être décrypté en comprenant la logique appliquée par `level09`.

### 2. Analyse du programme `level09`

En testant le programme avec différents arguments :

```bash
level09@SnowCrash:~$ ./level09 aaaa
abcd
level09@SnowCrash:~$ ./level09 eeee
efgh
level09@SnowCrash:~$ ./level09 ab
ac
```

Nous observons que chaque caractère de l'entrée est transformé en ajoutant un décalage basé sur sa position dans la chaîne (0 pour le premier caractère, +1 pour le deuxième, etc.).

**Règle de transformation probable** :
Pour chaque caractère `c` à la position `i` :

```plaintext
c_transformed = c + i
```

Cette transformation a également été appliquée au fichier `token`, qui contient les données chiffrées. Le but est d'inverser cette transformation pour récupérer le contenu original.

### 3. Exploitation de la vulnérabilité

La transformation ne sécurise pas réellement le contenu, car elle peut être inversée. En effet, pour chaque caractère transformé, il suffit de soustraire l'index de la position pour retrouver le caractère original.

### 4. Décryptage avec un script Python

Nous avons écrit un script Python pour automatiser cette opération et inverser la transformation appliquée sur le fichier `token`.

#### Script Python :

```python
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
```

#### Étape 1 : Exécuter le script

Place le script dans le même répertoire que le fichier `token` et exécute-le :

```bash
python3 decrypt.py
```

#### Étape 2 : Résultat

Le script affiche le contenu décrypté :

```bash
Contenu décrypté : f3iji1ju5yuevaus41q1afiuq
```

### 5. Passage à l'utilisateur suivant

Utilisez le flag récupéré pour passer à `flag09` :

```bash
level09@SnowCrash:~$ su flag09
Password: f3iji1ju5yuevaus41q1afiuq
Don't forget to launch getflag !
flag09@SnowCrash:~$ getflag
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
```

### 6. Accès à l'utilisateur suivant

Utilisez le token pour passer à `level10` :

```bash
flag09@SnowCrash:~$ su level10
Password: s5cAJpM8ev6XHw998pRWG728z
level10@SnowCrash:~$
```

### Vulnérabilité expliquée

Le programme `level09` applique une transformation simple et réversible au contenu de son argument ou du fichier `token`. Cette transformation est basée sur un décalage d'index, qui peut être inversé mathématiquement. En raison de l'absence de chiffrement réel ou de protection supplémentaire, le contenu peut être récupéré facilement à l'aide d'un script ou en analysant la logique interne du programme.
