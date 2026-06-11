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

