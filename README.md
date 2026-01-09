# 📚 Books to Scrape – Projet de Web Scraping

## 📖 Description

Ce projet permet d'extraire automatiquement les données des livres du site
https://books.toscrape.com.
Le script parcourt toutes les catégories et toutes les pages associées.

Les données collectées incluent :
* les informations détaillées de chaque livre
* les images de couverture 

## ⚙️ Prérequis

* Python 3.x
* Git

## 🛠️ Installation

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/fotsoaristide/books_scrape.git

cd books_scrape
```

### 2️⃣ Créer un environnement virtuel
```bash
python -m venv venv
```

### 3️⃣ Activer l’environnement virtuel
Windows
```bash
venv\Scripts\activate
```
Linux / macOS
```bash
source venv/bin/activate
```

### 4️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### ▶️ Exécution du script
```bash
python script.py
```

## 📦 Résultats générés après l’exécution :

* Les fichiers CSV sont générés par catégorie
* Les images des livres sont téléchargées et classées par catégorie
* Les données sont stockées localement dans le dossier `data/`

⚠️ Les données et images extraites ne sont pas incluses dans le repository GitHub, mais fournies séparément dans une archive ZIP.

## 📄 Dépendances (requirements.txt)

* requests
* beautifulsoup4
* pandas

## 👤 Auteur
Aristide Fotso


