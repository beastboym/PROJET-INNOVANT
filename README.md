TPM&

# PageRank Web Application

Cette application web calcule et affiche le PageRank des pages liées à un article Wikipédia donné. Le projet utilise Flask pour le backend et HTML/CSS pour le frontend.

Python pour l'algorithme

## Prérequis

Avant de pouvoir exécuter l'application, assurez-vous d'avoir les éléments suivants installés sur votre système :

- Python 3.12.2
- pip3 (gestionnaire de paquets Python)

## Installation

Suivez ces étapes pour configurer et exécuter l'application :

### 1. Clonez le dépôt

Clonez ce dépôt sur votre machine locale à l'aide de la commande suivante :

```bash
git clone https://github.com/beastboym/pagerank_app.git
cd pagerank_app
```

### 2. Créez un environnement virtuel

Il est recommandé de créer un environnement virtuel pour isoler les dépendances du projet. Utilisez les commandes suivantes pour créer et activer un environnement virtuel :

(Optionnel)

```bash
python3 -m venv venv
source venv/bin/activate   # Pour macOS/Linux
venv\Scripts\activate      # Pour Windows
```

### 3. Installez les dépendances

Installez les dépendances nécessaires en utilisant pip :

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contenient les lignes suivantes :

```
Flask
requests
beautifulsoup4
```

### 4. Exécutez l'application

Lancez l'application Flask avec la commande suivante :

```bash
python pagerank.py
```

### 5. Accédez à l'application

Ouvrez votre navigateur et accédez à l'URL suivante pour voir l'application en action :

```
http://127.0.0.1:5000/
```

si ce lien ne fonctionne pas, il est possible que cet adresse (Port 5000) soit déja occupé.
Je vous recommande de kill ce qui est en cours sur le port, si ce n'est pas possible vous pouvez spécifier le port que vous souhaitez utilisé.

par exemple:

```
python pagerank.py 5001
```

## Structure du Projet

Voici la structure du projet :

```
pagerank_app/
│
├── pagerank.py                  # Fichier principal de l'application Flask
├── requirements.txt        # Liste des dépendances Python
├── templates/
│   └── index.html          # Template HTML pour l'affichage des résultats
└── static/
    ├── css/
    │   └── styles.css      # Fichier CSS pour les styles
    └── js/
        └── scripts.js      # Fichier JavaScript (actuellement vide)
```

## Fonctionnement

L'application effectue les étapes suivantes :

1. **Scraping des Liens** : Le script `pagerank.py` scrappe les liens de la page Wikipédia spécifiée (dans ce cas, la page sur la France) en suivant les liens pertinents.
2. **Calcul du PageRank** : Les liens sont utilisés pour calculer le PageRank de chaque page en utilisant un algorithme itératif.
3. **Affichage des Résultats** : Les résultats sont triés et affichés sur une page web, avec les scores de PageRank et le nombre de liens sortants pour chaque page.

## Personnalisation

Pour analyser une autre page Wikipédia, modifiez l'URL dans la fonction `index()` de `app.py` :

```python
@app.route('/')
def index():
    url = "https://en.wikipedia.org/wiki/France"  # Modifiez cette ligne avec l'URL souhaitée
    pages = scrape_links_recursive(url)
    pagerank, outlinks_count = calculate_pagerank(pages)
    ranked_pages = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
    return render_template('index.html', ranked_pages=ranked_pages, outlinks_count=outlinks_count)
```

Pour augmenter le nombre de résultat, modifiez `scrape_links_recursive` :

```python
    pages = scrape_links_recursive(url, max_links="NOMBRE MAX DE LIEN", depth="PROFONDEUR MAX DE LIEN")
```
