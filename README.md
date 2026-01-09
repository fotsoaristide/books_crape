📚 Books to Scrape – Web Scraping Project

📖 Description:

Ce projet permet d'extraire automatiquement les données des livres du site
https://books.toscrape.com, y compris :les informations détaillées de chaque livre; les images de couverture; Le script parcourt toutes les catégories et toutes les pages associées.

⚙️ Prérequis

Python 3.x

Git

🛠️ Installation
1️⃣ Cloner le dépôt
git clone https://github.com/fotsoaristide/books_crape.git

cd books_scrape

2️⃣ Créer un environnement virtuel

python -m venv venv

3️⃣ Activer l’environnement virtuel
Windows
venv\Scripts\activate

Linux / macOS
source venv/bin/activate

4️⃣ Installer les dépendances

pip install -r requirements.txt

▶️ Exécution du script

python script.py

📦 Résultats générés
Après l’exécution :

Les fichiers CSV sont générés par catégorie

Les images des livres sont téléchargées et classées par catégorie

Les données sont stockées localement dans le dossier data/

⚠️ Les données et images extraites ne sont pas incluses dans le repository GitHub, mais fournies séparément dans une archive ZIP.

📄 Dépendances (requirements.txt)

requests

beautifulsoup4

pandas

👤 Auteur
Aristide Fotso




