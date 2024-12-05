# README - Trouver le Flag02 à partir du .pcap

## Étapes suivies pour trouver le Flag02

### 1. fichier level02.pcap

l'extension pcap veut dire packet capture donc pour l'analyser il faut utiliser WireShark par exemple.

Utilisez la commande `scp` pour télécharger le fichier `level02.pcap` sur votre machine locale :
```bash
scp -P 4242 level02@localhost:/home/user/level02/level02.pcap .
```

### 2. Analyse du fichier pcap avec Wireshark

J'ai ouvert le fichier level02.pcap dans Wireshark pour analyser les paquets et rechercher des informations pertinentes :

### 3. Recherche de la chaîne Password:

En analysant les paquets, j'ai trouvé une donnée intéressante qui commence par la chaîne Password:.
J'ai examiné les données suivantes et trouvé ce qui semblait être une partie du flag.

### 4. Extraction du flag

Dans les données extraites, j'ai trouvé la chaîne suivante :

`ft_wandr...NDRel.L0L`

Les caractères . sont en réalité des valeurs ASCII de 7f (DEL), indiquant que ces caractères doivent être interprétés comme des suppressions. En remplaçant les . par des caractères valides, le flag complet devient :

`ft_waNDReL0L`

```bash
level02@SnowCrash:~$ su flag02
Password: ft_waNDReL0L
Don't forget to launch getflag !
flag02@SnowCrash:~$ getflag
Check flag.Here is your token : kooda2puivaav1idi4f57q8iq
flag02@SnowCrash:~$ su level03
Password: kooda2puivaav1idi4f57q8iq
level03@SnowCrash:~$
```