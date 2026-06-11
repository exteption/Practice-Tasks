# visualizer.py — визуализация данных GitHub Trending
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
from config import OUTPUT_DIR, SOURCE_NAME

plt.rcParams.update({
    'font.family':       'DejaVu Sans',
    'font.size':         11,
    'figure.dpi':        120,
    'axes.spines.top':   False,
    'axes.spines.right': False,
})

COLORS = ['#0E7490', '#06B6D4', '#22D3EE', '#67E8F9', '#A5F3FC',
          '#4338CA', '#6366F1', '#818CF8', '#A5B4FC', '#C7D2FE']


def plot_bar_top_languages(top_langs: pd.Series, title: str = None) -> str:
    """
    Горизонтальная столбчатая диаграмма: топ-5 языков по количеству репозиториев.

    Args:
        top_langs (pd.Series): Серия с топ языками.
        title (str): Заголовок графика.

    Returns:
        str: Путь к сохранённому файлу.
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(top_langs.index, top_langs.values,
                   color=COLORS[:len(top_langs)], edgecolor='white', height=0.6)
    for bar in bars:
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                f'{int(bar.get_width())}', va='center', ha='left', fontsize=10)
    ax.set_xlabel('Количество репозиториев')
    ax.set_title(title or f'Топ-5 языков по числу репо — {SOURCE_NAME}', pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'bar_chart.png')
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(f'[✓] Сохранён: {path}')
    return path


def plot_pie_languages(top_langs: pd.Series) -> str:
    """
    Круговая диаграмма долей языков программирования.

    Args:
        top_langs (pd.Series): Серия с топ языками.

    Returns:
        str: Путь к сохранённому файлу.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        top_langs.values,
        labels=top_langs.index,
        autopct='%1.1f%%',
        colors=COLORS[:len(top_langs)],
        startangle=140,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
        pctdistance=0.8,
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight('bold')
    ax.set_title(f'Доля языков среди трендовых репо — {SOURCE_NAME}', pad=20)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'pie_chart.png')
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(f'[✓] Сохранён: {path}')
    return path


def plot_bar_mean_stars(mean_stars: pd.Series, top_n: int = 8) -> str:
    """
    Горизонтальный bar chart: среднее количество звёзд по языку программирования.

    Args:
        mean_stars (pd.Series): Серия со средними значениями звёзд.
        top_n (int): Количество языков для отображения.

    Returns:
        str: Путь к сохранённому файлу.
    """
    data = mean_stars.head(top_n)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(data.index, data.values,
                   color=COLORS[:len(data)], edgecolor='white', height=0.6)
    for bar in bars:
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                f'{bar.get_width():,.0f}', va='center', ha='left', fontsize=9)
    ax.set_xlabel('Среднее количество звёзд')
    ax.set_title(f'Среднее звёзд по языку (топ-{top_n}) — {SOURCE_NAME}', pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'bar_mean_stars.png')
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(f'[✓] Сохранён: {path}')
    return path


def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str) -> str:
    """
    Scatter plot для исследования корреляции между двумя числовыми полями.

    Args:
        df (pd.DataFrame): Датафрейм с данными.
        x_col (str): Название столбца для оси X.
        y_col (str): Название столбца для оси Y.

    Returns:
        str: Путь к сохранённому файлу.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df[x_col], df[y_col], alpha=0.6, color=COLORS[0],
               edgecolors='white', linewidth=0.5, s=60)
    ax.set_xlabel(x_col.capitalize())
    ax.set_ylabel(y_col.capitalize())
    ax.set_title(f'Корреляция: {x_col} ↔ {y_col}', pad=15)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, f'scatter_{x_col}_{y_col}.png')
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(f'[✓] Сохранён: {path}')
    return path
