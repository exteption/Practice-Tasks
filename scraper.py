# scraper.py — сбор данных с GitHub Trending
import requests
import time
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from config import BASE_URL, HEADERS, REQUEST_DELAY, TIMEOUT, CSV_FIELDS


def fetch_page(url: str) -> BeautifulSoup | None:

    try:
        print(f'[→] GET {url}')
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        print(f'[✓] HTTP {response.status_code}, размер: {len(response.text)} символов')
        time.sleep(REQUEST_DELAY)
        return BeautifulSoup(response.text, 'lxml')
    except requests.exceptions.HTTPError as e:
        print(f'[✗] HTTP ошибка: {e}')
    except requests.exceptions.ConnectionError:
        print(f'[✗] Нет соединения с {url}')
    except requests.exceptions.Timeout:
        print(f'[✗] Таймаут запроса ({TIMEOUT}с)')
    return None


def parse_items(soup: BeautifulSoup) -> list[dict]:
    """
    Извлечь данные репозиториев из HTML-дерева GitHub Trending.

    Args:
        soup (BeautifulSoup): Разобранный HTML документ.

    Returns:
        list[dict]: Список словарей с данными репозиториев.
    """
    items = []
    scraped_at = datetime.now().strftime('%Y-%m-%d %H:%M')

    articles = soup.find_all('article', class_='Box-row')
    print(f'[i] Найдено элементов: {len(articles)}')

    for art in articles:
        try:
            # Название репо и владелец
            h2 = art.find('h2')
            full_name = h2.get_text(strip=True).replace('\n', '').replace(' ', '') if h2 else ''
            parts = full_name.split('/')
            owner = parts[0].strip() if len(parts) > 1 else ''
            repo  = parts[1].strip() if len(parts) > 1 else full_name

            # Язык программирования
            lang_tag = art.find('span', itemprop='programmingLanguage')
            language = lang_tag.get_text(strip=True) if lang_tag else 'Unknown'

            # Звёзды и форки
            links = art.find_all('a', class_='Link--muted')
            stars_text = links[0].get_text(strip=True).replace(',', '') if links else '0'
            forks_text = links[1].get_text(strip=True).replace(',', '') if len(links) > 1 else '0'
            stars = int(stars_text) if stars_text.isdigit() else 0
            forks = int(forks_text) if forks_text.isdigit() else 0

            # Описание
            desc_tag = art.find('p')
            description = desc_tag.get_text(strip=True) if desc_tag else ''

            items.append({
                'repo':        repo,
                'owner':       owner,
                'language':    language,
                'stars':       stars,
                'forks':       forks,
                'description': description[:150],
                'scraped_at':  scraped_at,
            })
        except Exception as e:
            print(f'[!] Ошибка при парсинге элемента: {e}')
            continue

    return items


def save_to_csv(items: list[dict], filepath: str) -> None:
    """
    Сохранить список словарей в CSV-файл.

    Args:
        items (list[dict]): Список данных для сохранения.
        filepath (str): Путь к выходному CSV-файлу.
    """
    if not items:
        print('[!] Нет данных для сохранения')
        return
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(items)
    print(f'[✓] Сохранено {len(items)} записей → {filepath}')


def run_scraper(url: str, output_path: str) -> list[dict]:
    """
    Главная функция: скрапить страницу и сохранить результат в CSV.

    Args:
        url (str): URL страницы для скрапинга.
        output_path (str): Путь к выходному CSV-файлу.

    Returns:
        list[dict]: Список собранных данных.
    """
    soup = fetch_page(url)
    if soup is None:
        return []
    items = parse_items(soup)
    save_to_csv(items, output_path)
    return items


if __name__ == '__main__':
    from config import SNAPSHOT_1
    data = run_scraper(BASE_URL, SNAPSHOT_1)
    print(f'\nИтого собрано: {len(data)} элементов')
    for row in data[:3]:
        print(row)
