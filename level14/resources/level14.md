# README - Exploitation du binaire `/bin/getflag` (GDB Manipulation)

## Étapes suivies pour obtenir le Flag14

### 1. Analyse du binaire `/bin/getflag`

Charge le binaire dans `gdb` pour inspection :

```
level14@SnowCrash:~$ gdb /bin/getflag
```

- **Observation** : Le binaire `/bin/getflag` contient des symboles de débogage absents, mais reste exploitable via `gdb`.

### 2. Exploitation avec `gdb`

Place un breakpoint au début de la vérification `ptrace` :

```
(gdb) b *0x0804898e
Breakpoint 1 at 0x804898e
(gdb) run
Starting program: /bin/getflag 

Breakpoint 1, 0x0804898e in main ()
```

Vérifie et ajuste la valeur de retour de `ptrace` :

```
(gdb) print $eax
$1 = -1
(gdb) set $eax = 0
```

Place un breakpoint avant la vérification de l'UID et avance :

```
(gdb) b *0x08048b02
Breakpoint 2 at 0x8048b02
(gdb) step
Single stepping until exit from function main,
which has no line number information.

Breakpoint 2, 0x08048b02 in main ()
```

Vérifie et modifie l'UID avec celui de flag14 : 
```
level14@SnowCrash:~$ id flag14
uid=3014(flag14) gid=3014(flag14) groups=3014(flag14),1001(flag)
```

```
(gdb) print $eax
$2 = 2014
(gdb) print $esp
$3 = (void *) 0xbffff620
(gdb) set $eax = 3014
(gdb) print $eax
$4 = 3014
(gdb) continue
Continuing.
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
[Inferior 1 (process 3572) exited normally]
(gdb) quit
```


### Vulnérabilité expliquée

Le binaire `/bin/getflag` utilise `ptrace` pour détecter le débogage, mais cette vérification est contournée en modifiant `%eax` dans `gdb`. De plus, la comparaison de l'UID (`2014` vs `3014`) est vulnérable à une manipulation, permettant d'accéder au token. Une correction impliquerait une vérification plus robuste (ex. : hash de l'UID) et des protections contre le débogage (ex. : désactivation de `ptrace` dans `gdb`).
