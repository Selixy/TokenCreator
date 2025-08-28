# TokenCreator

Éditeur d’images 2D adapté au traitement de gros volumes de fichiers **PNG / JPEG / SVG**.  
Permet un workflow en chaîne : on indique un répertoire de traitement, et toutes les images qu’il contient (y compris dans les sous-dossiers) sont incluses automatiquement.  
L’outil est conçu pour préparer rapidement des tokens utiles en jeu de rôle.


## Prérequis
- Windows 10/11
- Python 3.11

## Installation (développement)
```bat
.vscode\script\setup_venv.bat
```
> Crée/actualise `.venv`, met `pip` à jour et installe les dépendances (définies dans `pyproject.toml`).

## Lancer l’application
- Via VS Code : **Terminal → Run Task → Lancer**
- ou en direct :
```bat
.vscode\script\run.bat
```
- ou encore, si le venv est actif :
```bat
python -m tokencreator
```

## Build (packaging Windows)
```bat
.vscode\script\release.bat
```
**Sortie finale :** `build/TokenCreator/`  
Ce dossier contient `TokenCreator.exe` **et** ses dépendances (/_internal, DLL Qt, etc.).  


## Arborescence (après build)
```
TokenCreator/
├─ .vscode/
│  └─ script/
│     ├─ build.ps1
│     ├─ build.py
│     └─ run.ps1
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ logic/
│  │  └─ ...
│  ├─ ui/
│  │  └─ ...
│  └─ styles/
│     └─ ...
├─ icons/
│  └─ app.ico
├─ build/
│  └─ TokenCreator/
│     ├─ TokenCreator.exe
│     └─ _internal/
└─ pyproject.toml
```

## Tests
```bat
python -m unittest discover -s tests -p "test_*.py"
```

## Gitignore
À ne pas versionner :
```
/.venv/
/build/
/__pycache__/
/*.spec
/app/*.egg-info/
```

## Licence
MIT
