import requests
from bs4 import BeautifulSoup
from scraper import scrape_article  
import time


def get_article_urls_from_category(category_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(category_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article', class_='post')
    urls = []

    for article in articles:
        link = article.find('a')
        if link and link.has_attr('href'):
            urls.append(link['href'])

    return urls


def scrape_category(category_url):
    article_urls = get_article_urls_from_category(category_url)
    print(f"[INFO] {len(article_urls)} articles trouvés.")

    all_data = []
    for url in article_urls:
        print(f"[SCRAPING] {url}")
        try:
            data = scrape_article(url)
            all_data.append(data)
            time.sleep(1)  # pour éviter d’être bloqué
        except Exception as e:
            print(f"[ERROR] Erreur avec l’article {url} : {e}")

    return all_data





# test avec url catégorie et dossier (ex. 'https://www.blogdumoderateur.com/dossier/instagram/') => fonctionnel
if __name__ == '__main__':
    cat_url = 'https://www.blogdumoderateur.com/social/'
    #cat_url = 'https://www.blogdumoderateur.com/dossier/instagram/'
    articles = scrape_category(cat_url)

    for article in articles:
        print("TITRE :", article['title'])
        print("SOUS-CATÉGORIE :", article['subcategories'])
        print("DATE :", article['date'])
        print("---")    