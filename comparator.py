# comparator.py — сравнение двух срезов данных GitHub Trending
import pandas as pd
import matplotlib.pyplot as plt
import os
from config import SNAPSHOT_1, SNAPSHOT_2, OUTPUT_DIR, SOURCE_NAME

COLORS = ['#0E7490', '#059669', '#0891B2', '#10B981',
          '#0284C7', '#22C55E', '#6366F1', '#8B5CF6']


def load_both(path1: str = SNAPSHOT_1, path2: str = SNAPSHOT_2):
    """
    Загрузить оба CSV-среза и добавить метку источника.

    Args:
        path1 (str): Путь к первому снимку данных.
        path2 (str): Путь к второму снимку данных.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Два датафрейма с метками.
    """
    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)
    df1['snapshot'] = 'Срез 1'
    df2['snapshot'] = 'Срез 2'
    print(f'[i] Срез 1: {len(df1)} строк  │  Срез 2: {len(df2)} строк')
    return df1, df2


def compare_top_categories(df1: pd.DataFrame, df2: pd.DataFrame,
                            cat_col: str = 'language', n: int = 5) -> dict:
    """
    Сравнить топ-N категорий между двумя срезами.

    Args:
        df1 (pd.DataFrame): Первый срез данных.
        df2 (pd.DataFrame): Второй срез данных.
        cat_col (str): Название столбца категорий.
        n (int): Количество топ-позиций.

    Returns:
        dict: Словарь с множествами stayed/new/dropped.
    """
    top1 = set(df1[cat_col].value_counts().head(n).index)
    top2 = set(df2[cat_col].value_counts().head(n).index)
    new_in_2 = top2 - top1
    dropped  = top1 - top2
    stayed   = top1 & top2
    print(f'\n=== Сравнение топ-{n} по «{cat_col}» ===')
    print(f'  Остались в топе:  {stayed}')
    print(f'  Вошли в топ:      {new_in_2}')
    print(f'  Выбыли из топа:   {dropped}')
    return {'stayed': stayed, 'new': new_in_2, 'dropped': dropped}


def compare_numeric(df1: pd.DataFrame, df2: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Сравнить описательную статистику числового поля между срезами.

    Args:
        df1 (pd.DataFrame): Первый срез данных.
        df2 (pd.DataFrame): Второй срез данных.
        col (str): Название числового столбца.

    Returns:
        pd.DataFrame: Таблица сравнения статистик.
    """
    stats = pd.DataFrame({
        'Срез 1': df1[col].describe().round(1),
        'Срез 2': df2[col].describe().round(1),
    })
    print(f'\n=== Сравнение «{col}» между срезами ===')
    print(stats.to_string())
    return stats


def plot_comparison_bar(df1: pd.DataFrame, df2: pd.DataFrame,
                        cat_col: str = 'language', n: int = 5) -> str:
    """
    Grouped bar chart: сравнение топ-N категорий между двумя срезами.

    Args:
        df1 (pd.DataFrame): Первый срез данных.
        df2 (pd.DataFrame): Второй срез данных.
        cat_col (str): Название столбца категорий.
        n (int): Количество топ-позиций.

    Returns:
        str: Путь к сохранённому файлу.
    """
    top_cats = (pd.concat([df1, df2])[cat_col]
                .value_counts().head(n).index.tolist())
    counts1 = [df1[df1[cat_col] == c].shape[0] for c in top_cats]
    counts2 = [df2[df2[cat_col] == c].shape[0] for c in top_cats]

    x = range(len(top_cats))
    w = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))
    b1 = ax.bar([i - w / 2 for i in x], counts1, w,
                label='Срез 1 (Общий тренд)', color='#0E7490', edgecolor='white')
    b2 = ax.bar([i + w / 2 for i in x], counts2, w,
                label='Срез 2 (Русскоязычный)', color='#059669', edgecolor='white')
    for bar in list(b1) + list(b2):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.1,
                str(int(h)), ha='center', va='bottom', fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(top_cats, rotation=15, ha='right')
    ax.set_ylabel('Количество')
    ax.set_title(f'Сравнение топ-{n} языков: общий тренд vs русскоязычный — {SOURCE_NAME}',
                 pad=15)
    ax.legend()
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'comparison.png')
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(f'[✓] Сохранён: {path}')
    return path


def run_comparison() -> tuple:
    """
    Запустить полное сравнение двух срезов данных.

    Returns:
        tuple: Словарь изменений категорий и таблица числовой статистики.
    """
    df1, df2 = load_both()
    diff      = compare_top_categories(df1, df2)
    num_stats = compare_numeric(df1, df2, 'stars')
    plot_comparison_bar(df1, df2)
    return diff, num_stats


if __name__ == '__main__':
    run_comparison()
