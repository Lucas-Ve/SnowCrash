# README - Exploitation du binaire level13

## Étapes suivies pour obtenir le Flag13

### 1. Identification des fichiers

Le répertoire contient un fichier principal :

```bash
level13@SnowCrash:~$ ls -l
total 12
-rwsr-sr-x 1 flag13 level13 8672 Mar  5  2016 level13
```

- **`level13`** : Un binaire ELF 32-bit exécutable avec permissions `setuid` et `setgid`, s'exécutant avec les privilèges de l'utilisateur `flag13`.

### 2. Analyse du binaire `level13`

Charge le binaire dans `gdb` et désassemble `main` :

```
(gdb) disas main
Dump of assembler code for function main:
   0x0804858c <+0>:	push   %ebp
   0x0804858d <+1>:	mov    %esp,%ebp
   0x0804858f <+3>:	and    $0xfffffff0,%esp
   0x08048592 <+6>:	sub    $0x10,%esp
   0x08048595 <+9>:	call   0x8048380 <getuid@plt>
   0x0804859a <+14>:	cmp    $0x1092,%eax
   0x0804859f <+19>:	je     0x80485cb <main+63>
   0x080485a1 <+21>:	call   0x8048380 <getuid@plt>
   0x080485a6 <+26>:	mov    $0x80486c8,%edx
   0x080485ab <+31>:	movl   $0x1092,0x8(%esp)
   0x080485b3 <+39>:	mov    %eax,0x4(%esp)
   0x080485b7 <+43>:	mov    %edx,(%esp)
   0x080485ba <+46>:	call   0x8048360 <printf@plt>
   0x080485bf <+51>:	movl   $0x1,(%esp)
   0x080485c6 <+58>:	call   0x80483a0 <exit@plt>
   0x080485cb <+63>:	movl   $0x80486ef,(%esp)
   0x080485d2 <+70>:	call   0x8048474 <ft_des>
   0x080485d7 <+75>:	mov    $0x8048709,%edx
   0x080485dc <+80>:	mov    %eax,0x4(%esp)
   0x080485e0 <+84>:	mov    %edx,(%esp)
   0x080485e3 <+87>:	call   0x8048360 <printf@plt>
   0x080485e8 <+92>:	leave  
   0x080485e9 <+93>:	ret    
End of assembler dump.
```

- **Observation** : À `0x0804859a <+14>`, le programme compare l'UID (`%eax`) avec `0x1092` (4242 en décimal). Si l'UID ne correspond pas, il sort via `exit(1)`. Sinon, il appelle `ft_des` à `0x080485d2 <+70>`.

### 3. Exploitation de la vérification UID avec `gdb`

Place un breakpoint à la comparaison et ajuste l'UID :

```
(gdb) b *0x0804859a
Breakpoint 1 at 0x804859a
(gdb) run
Starting program: /home/user/level13/level13 

Breakpoint 1, 0x0804859a in main ()
(gdb) print $eax
$1 = 2013
(gdb) set $eax = 4242
(gdb) print $eax
$2 = 4242
(gdb) continue
Continuing.
your token is 2A31L79asukciNyi8uppkEuSx
[Inferior 1 (process 3314) exited with code 050]
(gdb) quit
```

- **Explication** : L'UID initial est `2013` (UID de `level13`). En le modifiant à `4242` avec `set $eax = 4242`, la condition `je 0x80485cb` est satisfaite, et le programme continue vers `ft_des`, affichant le token `2A31L79asukciNyi8uppkEuSx`.

### 4. Passage à l'utilisateur suivant

Utilise le token obtenu pour passer à `level14` :

```bash
level13@SnowCrash:~$ su level14
Password: 2A31L79asukciNyi8uppkEuSx
level14@SnowCrash:~$ 
```

### Vulnérabilité expliquée

Le binaire vérifie l'UID (`getuid() == 4242`). Si faux, il sort. La dépendance à un UID spécifique est une faiblesse, car elle peut être contournée en modifiant `%eax` dans `gdb`.