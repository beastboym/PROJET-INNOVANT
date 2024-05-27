import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from collections import defaultdict
from flask import Flask, render_template

app = Flask(__name__)

reserved_words = ["User", "Talk", "Special", "Help", "File", "Wikipedia", "Template", "Category",
                  "Portal", "Draft", "TimedText", "Module", "Gadget", "MediaWiki"]

keywords = ["France", "French", "Paris", "Français", "Française"]


def is_relevant(url, keywords):
    return any(keyword.lower() in url.lower() for keyword in keywords)


def scrape_links_recursive(url, max_links=1000, depth=2, pages=None, parent=None):
    if pages is None:
        pages = {}
    if url in pages:
        return pages
    if len(pages) >= max_links:
        return pages

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        links = [urljoin(url, link) for link in links if link]
        links = [urldefrag(link)[0]
                 for link in links if link]  # Ignorer les ancres
        links = [link for link in links if link.startswith(
            "https://en.wikipedia.org/wiki")]  # Filtrer les liens
        links = [link for link in links if not any(
            word in link for word in reserved_words)]  # Filtrer les mots réservés
        links = [link for link in links if is_relevant(
            link, keywords)]  # Filtrer par pertinence

        links = list(set(links))  # Supprimer les doublons
    except Exception as e:
        print(f"Erreur lors de l'accès à {url}: {e}")
        links = []

    pages[url] = links[:10] if parent else links[:500]

    if depth == 0:
        return pages

    for link in pages[url][:10]:
        if len(pages) < max_links:
            scrape_links_recursive(link, max_links, depth-1, pages, parent=url)
        else:
            break

    return pages


def calculate_pagerank(pages, damping_factor=0.85, max_iterations=100, tol=1.0e-6):
    num_pages = len(pages)
    pagerank = dict.fromkeys(pages, 1.0 / num_pages)
    new_pr = dict.fromkeys(pages, 0)
    outlinks_count = defaultdict(int)

    for page in pages:
        for link in pages[page]:
            outlinks_count[link] += 1
    for _ in range(max_iterations):
        for page in pages:
            new_pr[page] = (1 - damping_factor) / num_pages
            for other_page in pages:
                if page in pages[other_page]:
                    new_pr[page] += damping_factor * \
                        (pagerank[other_page] / len(pages[other_page]))
        if all(abs(new_pr[page] - pagerank[page]) < tol for page in pages):
            break
        pagerank, new_pr = new_pr, pagerank
    return pagerank, outlinks_count


def display_pagerank(pagerank, outlinks_count):
    ranked_pages = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
    for page, rank in ranked_pages:
        count = outlinks_count[page]
        print(f"{page}: {rank:.4f} (Occurences: {count})")


@app.route('/')
def index():
    url = "https://en.wikipedia.org/wiki/France"
    pages = scrape_links_recursive(url)
    pagerank, outlinks_count = calculate_pagerank(pages)
    ranked_pages = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
    return render_template('index.html', ranked_pages=ranked_pages, outlinks_count=outlinks_count)


if __name__ == "__main__":
    app.run(debug=True)
    print(scrape_links_recursive(url))
