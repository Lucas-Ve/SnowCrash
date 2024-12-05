# README - Trouver le Flag01 à partir du hash dans /etc/passwd

## Étapes suivies pour trouver le Flag01

### 1. Recherche du hash dans le fichier `/etc/passwd`

J'ai affiché le contenu du fichier `/etc/passwd` avec la commande suivante :

```bash
cat /etc/passwd
```

J'ai trouvé un hash pour l'utilisateur `flag01` :

```sh
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

Le hash associé à flag01 est `42hDRfypTqqnw`.

### 2. Utilisation de John the Ripper pour déchiffrer le hash

J'ai créé un fichier contenant le hash avec la commande suivante :

```bash
echo "42hDRfypTqqnw" > hashfile
```

Puis, j'ai utilisé John the Ripper pour cracker le hash :

```bash
john hashfile
```

### 3. Résultat du déchiffrement

John the Ripper a trouvé le mot de passe associé au hash :

`abcdefg`

```bash
level01@SnowCrash:~$ su flag01
Password: `abcdefg`
Don't forget to launch getflag !
flag01@SnowCrash:~$ getflag
Check flag.Here is your token : `f2av5il02puano7naaf6adaaf`
flag01@SnowCrash:~$ su level02
Password: `f2av5il02puano7naaf6adaaf`
level02@SnowCrash:~$ 
```