# geo-docker-demo

Petit projet pour illustrer les principes de base de Docker appliqués à
la géomatique : un script Python (GeoPandas) qui charge des polygones,
les reprojette et calcule leur superficie, le tout exécuté dans un
conteneur, sans rien installer sur la machine hôte.

## Contenu du dépôt

```
geo-docker-demo/
├── Dockerfile          ← définit l'image (Python + GDAL + GeoPandas)
├── .dockerignore        ← fichiers exclus du build
├── requirements.txt     ← dépendances Python
├── main.py               ← script d'exemple
├── data/
│   └── secteurs.geojson  ← données simplifiées, à but pédagogique
└── README.md
```

## Prérequis

Docker installé sur votre poste (Docker Desktop sur Windows/macOS,
Docker Engine sur Linux). Vérifiez avec :

```bash
docker --version
```

## Installer Docker en local

### Windows

Docker Desktop utilise généralement WSL 2 pour exécuter Docker sous
Windows.

La commande `wsl` est disponible nativement sur Windows 10 version 2004
(build 19041) ou ultérieure et sur Windows 11. Utilisez `winver` dans le
menu Démarrer pour vérifier votre version de Windows. Si la commande
`wsl` n'est pas reconnue, mettez Windows à jour avant de poursuivre.

1. Ouvrez **PowerShell en tant qu'administrateur** et vérifiez d'abord
   si WSL 2 est déjà installé :

  ```powershell
  wsl --status
  wsl --version
  wsl --list --verbose
  ```

  Une distribution Linux doit afficher `VERSION 2`. Si la commande
  `wsl` est reconnue mais que WSL ou une distribution Linux n'est pas
  installé, exécutez :

  ```powershell
  wsl --install
  ```

  Si aucune distribution n'est installée, vous pouvez installer Ubuntu
  avec `wsl --install -d Ubuntu`. Redémarrez l'ordinateur si Windows le
  demande.

  Si `wsl` n'est pas reconnu, cette commande ne peut pas encore être
  utilisée. Vérifiez votre version avec `winver`, installez les mises à
  jour Windows, puis ouvrez à nouveau PowerShell en tant qu'administrateur
  et reprenez cette étape. Pour une installation manuelle, consultez le
  [guide Microsoft consacré à WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install-manual).
2. Téléchargez et installez [Docker Desktop](https://www.docker.com/products/docker-desktop/).
  Pendant l'installation, activez l'option **Use WSL 2 instead of Hyper-V**
  si elle est proposée.
3. Dans Docker Desktop, vérifiez que **Use the WSL 2 based engine** est
  activé dans les paramètres généraux.
4. Ouvrez PowerShell ou un terminal WSL et vérifiez l'installation :

  ```powershell
  docker --version
  docker run hello-world
  ```

Pour plus de détails, consultez le [guide Docker Desktop pour WSL 2](https://docs.docker.com/desktop/features/wsl/).

### macOS

1. Téléchargez et installez [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Lancez Docker Desktop et attendez que le moteur Docker soit démarré.
3. Ouvrez un terminal et vérifiez l'installation :

  ```bash
  docker --version
  docker run hello-world
  ```

Docker Desktop fournit Docker Engine, Docker CLI et les composants
nécessaires pour exécuter les conteneurs sur Windows et macOS.

### Linux

1. Consultez la [documentation officielle d'installation de Docker Engine](https://docs.docker.com/engine/install/)
  et sélectionnez votre distribution Linux.
2. Suivez les étapes indiquées pour installer Docker Engine et Docker
  Compose.
3. Vérifiez l'installation :

  ```bash
  docker --version
  sudo docker run hello-world
  ```

Sur Linux, l'utilisation de `sudo` peut être nécessaire. Pour exécuter
Docker sans `sudo`, ajoutez ensuite votre utilisateur au groupe `docker`
en suivant la [procédure post-installation officielle](https://docs.docker.com/engine/install/linux-postinstall/),
puis reconnectez-vous à votre session.

## Utiliser le projet dans GitHub Codespaces

GitHub Codespaces fournit un environnement de développement dans le
navigateur avec Docker déjà disponible. Pour lancer ce projet :

1. Sur GitHub, ouvrez la page du dépôt, cliquez sur **Code**, puis sur
  l'onglet **Codespaces**.
2. Cliquez sur **Create codespace on main** (ou choisissez la branche à
  utiliser). Attendez que le Codespace soit entièrement démarré.
3. Dans le terminal intégré de VS Code, vérifiez que Docker est
  disponible :

  ```bash
  docker --version
  ```

4. Construisez l'image depuis la racine du dépôt :

  ```bash
  docker build -t geo-docker-demo .
  ```

5. Exécutez l'exemple :

  ```bash
  docker run --rm geo-docker-demo
  ```

Les fichiers du dépôt sont directement accessibles dans le Codespace.
Les modifications sont conservées dans le Codespace et peuvent être
enregistrées avec Git puis envoyées sur GitHub avec `git add`, `git
commit` et `git push`. Pour éviter de consommer des ressources, arrêtez
ou supprimez le Codespace depuis **GitHub > Settings > Codespaces** quand
vous avez terminé (vous pouvez aussi visiter le lien suivant : https://github.com/codespaces, vous y verrez tous les environnements qui tournent.)

## Commandes de base

### 1. Construire l'image

```bash
docker build -t geo-docker-demo .
```

- `-t geo-docker-demo` donne un nom (tag) à l'image, pour la retrouver
  facilement ensuite
- Le `.` indique que le Dockerfile se trouve dans le dossier courant

### 2. Lancer un conteneur à partir de l'image

```bash
docker run --rm geo-docker-demo
```

- `--rm` supprime le conteneur automatiquement une fois l'exécution
  terminée (il n'a pas besoin de rester après coup)
- Le script `main.py` s'exécute et affiche les superficies calculées

### 3. Monter un dossier local (volume)

Pour que le conteneur utilise vos propres données, sans les copier
dans l'image :

```bash
docker run --rm -v "$(pwd)/data:/app/data" geo-docker-demo
```

- `-v hôte:conteneur` relie un dossier de votre machine à un dossier
  du conteneur — modifier `data/secteurs.geojson` localement change
  ce que le script lit, sans reconstruire l'image

### 4. Ouvrir un terminal dans le conteneur

Utile pour explorer l'environnement ou déboguer :

```bash
docker run --rm -it geo-docker-demo bash
```

- `-it` rend la session interactive (clavier + terminal)
- `bash` remplace la commande par défaut (`python main.py`) par un
  shell

### 5. Lister, inspecter, nettoyer

```bash
docker images              # images construites localement
docker ps                  # conteneurs en cours d'exécution
docker ps -a                # tous les conteneurs, y compris arrêtés
docker rmi geo-docker-demo  # supprimer l'image
docker system prune         # nettoyer les images/conteneurs inutilisés
```

## Modifier le projet

Après toute modification de `main.py` ou de `data/secteurs.geojson`,
il faut reconstruire l'image pour que le changement soit pris en
compte à l'intérieur du conteneur :

```bash
docker build -t geo-docker-demo .
docker run --rm geo-docker-demo
```

(Si vous utilisez un volume comme à l'étape 3, seules les
modifications du **code** nécessitent une reconstruction — les
données montées en volume sont toujours lues à jour.)

## Pourquoi Docker ici ?

`geopandas` dépend de GDAL, une bibliothèque système parfois délicate
à installer (versions incompatibles, dépendances manquantes selon le
système d'exploitation). Le `Dockerfile` fixe cet environnement une
fois pour toutes : le projet tourne à l'identique sur n'importe quel
poste ayant Docker installé, sans étape d'installation manuelle.
