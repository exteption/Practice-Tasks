# analyzer.py — анализ данных GitHub Trending
import pandas as pd
from config import SNAPSHOT_1


def load_data(filepath: str) -> pd.DataFrame:
    """
    Загрузить CSV и выполнить базовую очистку данных.

    Args:
        filepath (str): Путь к CSV-файлу.

    Returns:
        pd.DataFrame: Очищенный датафрейм.
    """
    df = pd.read_csv(filepath)
    print(f'\n[i] Загружено {len(df)} строк, {len(df.columns)} колонок')
    print(f'[i] Колонки: {list(df.columns)}')
    print(f'[i] Пропущенные значения:\n{df.isnull().sum()}')

    df['language'] = df['language'].fillna('Unknown')
    df['stars'] = pd.to_numeric(df['stars'], errors='coerce').fillna(0).astype(int)
    df['forks'] = pd.to_numeric(df['forks'], errors='coerce').fillna(0).astype(int)
    return df


def top_by_category(df: pd.DataFrame, cat_col: str, n: int = 5) -> pd.Series:
    """
    Топ-N категорий по количеству записей.

    Args:
        df (pd.DataFrame): Датафрейм с данными.
        cat_col (str): Название столбца категорий.
        n (int): Количество топ-записей.

    Returns:
        pd.Series: Серия с топ-N категориями.
    """
    top = df[cat_col].value_counts().head(n)
    print(f'\n=== Топ-{n} по полю «{cat_col}» ===')
    print(top.to_string())
    return top


def mean_by_category(df: pd.DataFrame, cat_col: str, num_col: str) -> pd.Series:
    """
    Среднее числового поля в разбивке по категории.

    Args:
        df (pd.DataFrame): Датафрейм с данными.
        cat_col (str): Название столбца категорий.
        num_col (str): Название числового столбца.

    Returns:
        pd.Series: Серия со средними значениями.
    """
    means = df.groupby(cat_col)[num_col].mean().sort_values(ascending=False)
    print(f'\n=== Среднее «{num_col}» по «{cat_col}» ===')
    print(means.round(1).to_string())
    return means


def descriptive_stats(df: pd.DataFrame, num_col: str) -> pd.Series:
    """
    Описательная статистика числового поля.

    Args:
        df (pd.DataFrame): Датафрейм с данными.
        num_col (str): Название числового столбца.

    Returns:
        pd.Series: Серия с описательной статистикой.
    """
    stats = df[num_col].describe()
    print(f'\n=== Описательная статистика «{num_col}» ===')
    print(stats.round(1).to_string())
    return stats


def correlation_analysis(df: pd.DataFrame, col1: str, col2: str) -> float:
    """
    Коэффициент корреляции Пирсона между двумя числовыми полями.

    Args:
        df (pd.DataFrame): Датафрейм с данными.
        col1 (str): Первый числовой столбец.
        col2 (str): Второй числовой столбец.

    Returns:
        float: Коэффициент корреляции.
    """
    r = df[[col1, col2]].corr().iloc[0, 1]
    print(f'\n=== Корреляция {col1} ↔ {col2}: r = {r:.3f} ===')
    if abs(r) > 0.7:
        print('  → Сильная зависимость')
    elif abs(r) > 0.4:
        print('  → Умеренная зависимость')
    else:
        print('  → Слабая или отсутствует')
    return r


def top_n_records(df: pd.DataFrame, sort_col: str, n: int = 10) -> pd.DataFrame:
    """
    Топ-N записей по числовому полю.

    Args:
        df (pd.DataFrame): Датафрейм с данными.
        sort_col (str): Столбец для сортировки.
        n (int): Количество топ-записей.

    Returns:
        pd.DataFrame: Датафрейм с топ-N записями.
    """
    top = df.nlargest(n, sort_col)
    print(f'\n=== Топ-{n} по «{sort_col}» ===')
    print(top[['repo', 'language', sort_col]].to_string(index=False))
    return top


def run_analysis(filepath: str = SNAPSHOT_1) -> dict:
    """
    Запустить полный анализ данных.

    Args:
        filepath (str): Путь к CSV-файлу.

    Returns:
        dict: Словарь с результатами анализа.
    """
    df = load_data(filepath)
    top_langs   = top_by_category(df, 'language', n=5)
    mean_stars  = mean_by_category(df, 'language', 'stars')
    stars_stats = descriptive_stats(df, 'stars')
    corr_sf     = correlation_analysis(df, 'stars', 'forks')
    top_repos   = top_n_records(df, 'stars', n=10)

    return {
        'df':          df,
        'top_langs':   top_langs,
        'mean_stars':  mean_stars,
        'stars_stats': stars_stats,
        'corr_sf':     corr_sf,
        'top_repos':   top_repos,
    }


if __name__ == '__main__':
    results = run_analysis()
