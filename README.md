# PPC_projet

## Que faut il installer pour lancer le projet ?

```sh
pip install pygame os multiprocessing time signal threading random socket json datetime
```

ou bien

```sh
sudo apt-get install python3-pygame
```

(sachant que la plupart des packages sont déjà installé)

## Comment on lance le projet ?

On commence par lancé l'interface graphique :

```sh
~/PPC_projet$ cd frontend
```

```sh
~/PPC_projet/frontend$ python3 main.py
```

Puis on lance le code présent dans le "backend" :

```sh
~/PPC_projet$ cd backend
```

```sh
~/PPC_projet/backend$ python3 main.py
```

Il ne reste plus qu'à attendre (quelques secondes) que les premiers véhicules arrivent !

## Comment on arrête le projet ?

Il faut simplement faire la commande : `CTRL + C ` au sein du terminal concerné.
