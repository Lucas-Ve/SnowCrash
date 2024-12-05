# README - level00

## Étapes suivies pour trouver le Flag

### 1. Recherche des fichiers appartenant à `flag00`

La première étape a été de trouver les fichiers appartenant à l'utilisateur **`flag00`**. Pour cela, j'ai utilisé la commande `find` :

```bash
find / -user flag00 2> /dev/null
```

Cette commande recherche tous les fichiers dans le système qui appartiennent à `flag00` et redirige les erreurs vers `/dev/null`. Le résultat de cette commande était :

```bash
/usr/sbin/john
/rofs/usr/sbin/john
```

### 2. Exploration des fichiers john

Ensuite, j'ai ouvert ces fichiers pour en examiner le contenu. En utilisant les commandes suivantes :

```bash
cat /usr/sbin/john
cat /rofs/usr/sbin/john
```

J'ai trouvé la même chaîne dans les deux fichiers : `cdiiddwpgswtgt`. Cette chaîne semblait être chiffrée ou encodée d'une manière particulière.

### 3. Décodage de la chaîne cdiiddwpgswtgt

Pour déchiffrer cette chaîne, j'ai utilisé un outil en ligne de déchiffrement dcode.fr. Après avoir testé différentes méthodes de décryptage, l'outil a révélé que la chaîne `cdiiddwpgswtgt` correspondait à la phrase en clair :

`nottoohardhere`

```bash
level00@SnowCrash:~$ su flag00
Password: `nottoohardhere`

level00@SnowCrash:~$ getflag
Check flag.Here is your token : x24ti5gi3x0ol2eh4esiuxias

flag00@SnowCrash:~$ su level01
Password: `x24ti5gi3x0ol2eh4esiuxias`
level01@SnowCrash:~$ 
```
