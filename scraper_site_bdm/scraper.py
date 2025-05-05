import requests # import pour les requêtes HTTP
from bs4 import BeautifulSoup # import pour le parsing HTML
from datetime import datetime

def scrape_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    # Titre
    title_tag = soup.find('h1', class_='entry-title')
    data['title'] = title_tag.get_text(strip=True) if title_tag else None

    # Image principale
    main_img = soup.find('img', class_='wp-post-image')
    data['thumbnail'] = main_img['src'] if main_img and main_img.has_attr('src') else None

    # Catégorie principale
    category_link = soup.find('a', class_='t-def')
    data['category'] = category_link.get_text(strip=True) if category_link else None
    # Catégorie : lien avec href contenant une catégorie principale
    categories = ['web', 'marketing', 'social', 'tech', 'tools']
    category_link = None
    for cat in categories:
        link = soup.find('a', href=f"https://www.blogdumoderateur.com/{cat}/", class_='t-def')
        if link:
            category_link = link
            break
    data['category'] = category_link.get_text(strip=True) if category_link else None

    #    # Sous-catégories (tags)
    tags_list = soup.find('ul', class_='tags-list')
    if tags_list:
        first_tag = tags_list.find('a', class_='post-tags')
        data['subcategories'] = [first_tag.get_text(strip=True)] if first_tag else []
        print(f"[DEBUG] Première sous-catégorie trouvée : {data['subcategories'][0] if data['subcategories'] else 'Aucune'}")
    else:
        data['subcategories'] = []
        print("[DEBUG] Aucune liste de tags trouvée")

    print(f"[DEBUG] tags_list trouvé : {bool(tags_list)}")
    print(f"[DEBUG] sous-catégorie : {data['subcategories']}")

    # Résumé (chapô)
    excerpt = soup.find('div', class_='entry-content').find('p')
    data['summary'] = excerpt.get_text(strip=True) if excerpt else None

    # Date de publication
    time_tag = soup.find('time', class_='entry-date')
    if time_tag and time_tag.has_attr('datetime'):
        date_raw = time_tag['datetime']
        data['date'] = date_raw[:10]  # Garde uniquement AAAA-MM-JJ
    else:
        data['date'] = None

    # Auteur
    author_tag = soup.select_one('.byline a')
    data['author'] = author_tag.get_text(strip=True) if author_tag else None

    # Images dans le contenu avec alt ou figcaption
    content = soup.find('div', class_='entry-content')
    images = content.find_all('img') if content else []
    image_list = []
    for img in images:
        url = img.get('src') or img.get('data-lazy-src')
        alt = img.get('alt')
        image_list.append({
            'url': url,
            'caption': alt
        })
    data['content_images'] = image_list

    return data


# TEST
article_url = 'https://www.blogdumoderateur.com/instagram-ajoute-nouvelles-fonctionnalites-edits-polices-ecriture-effets-vocaux/'
result = scrape_article(article_url)

# Affichage
for key, value in result.items():
    print(f"{key.upper()} :\n{value}\n")


