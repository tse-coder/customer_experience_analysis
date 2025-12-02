"""Task 4 insights: generate drivers, pain-points, and visualizations.

Produces:
 - reports/figures/rating_distribution.png
 - reports/figures/sentiment_counts.png
 - reports/figures/top_keywords_{bank}.png (per bank)
 - reports/summary_task4.json (brief summary)

Run from repository root with PYTHONPATH=src so modules import correctly:
    PYTHONPATH=src venv/bin/python src/task4_insights.py
"""
import os
from pathlib import Path
import re
from collections import Counter, defaultdict

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
PROCESSED = DATA_DIR / 'processed'
SENTIMENT = DATA_DIR / 'sentiment_results'
OUT_DIR = ROOT / 'reports'
FIG_DIR = OUT_DIR / 'figures'
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

STOPWORDS = set([
    'the','a','and','is','it','to','i','in','for','of','this','that','with','be','on','not','my',
    'you','was','but','are','as','have','has','they','them','we','so','too','do','me','your','its'
])


def load_data():
    banks = ['CBE','BOA','DB']
    dfs = {}
    for b in banks:
        p = PROCESSED / f"{b}.csv"
        if p.exists():
            dfs[b] = pd.read_csv(p, parse_dates=['date'])
    # sentiment files
    sdfs = {}
    for b in banks:
        p = SENTIMENT / f"{b}_sentiment.csv"
        if p.exists():
            sdfs[b] = pd.read_csv(p)
    return dfs, sdfs


def plot_rating_distribution(dfs):
    out = FIG_DIR / 'rating_distribution.png'
    combined = []
    for bank, df in dfs.items():
        tmp = df[['rating']].copy()
        tmp['bank'] = bank
        combined.append(tmp)
    dfc = pd.concat(combined, ignore_index=True)

    plt.figure(figsize=(8,5))
    sns.countplot(data=dfc, x='rating', hue='bank')
    plt.title('Rating Distribution by Bank')
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    return out


def plot_sentiment_counts(sdfs):
    out = FIG_DIR / 'sentiment_counts.png'
    combined = []
    for bank, df in sdfs.items():
        # choose textblob sentiment label if present or vader
        label_col = 'tb_sentiment' if 'tb_sentiment' in df.columns else ('vader_sentiment' if 'vader_sentiment' in df.columns else None)
        if label_col is None:
            continue
        tmp = df[[label_col]].copy()
        tmp.columns = ['sentiment']
        tmp['bank'] = bank
        combined.append(tmp)
    dfc = pd.concat(combined, ignore_index=True)

    plt.figure(figsize=(8,5))
    sns.countplot(data=dfc, x='sentiment', hue='bank')
    plt.title('Sentiment Label Counts by Bank')
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    return out


def extract_keywords(text, n=20):
    # very basic tokenization
    if not isinstance(text, str):
        return []
    words = re.findall(r"\b[\w']{3,}\b", text.lower())
    words = [w for w in words if w not in STOPWORDS and not w.isdigit()]
    return words


def bank_keywords(df, topn=15):
    # count words across reviews and split by positive/negative
    # positive = rating >=4, negative = rating <=2
    pos_texts = df[df['rating'] >= 4]['review'].astype(str).tolist()
    neg_texts = df[df['rating'] <= 2]['review'].astype(str).tolist()

    pos_counts = Counter()
    neg_counts = Counter()
    for t in pos_texts:
        pos_counts.update(extract_keywords(t))
    for t in neg_texts:
        neg_counts.update(extract_keywords(t))

    return pos_counts.most_common(topn), neg_counts.most_common(topn)


def plot_top_keywords(bank, pos, neg):
    out = FIG_DIR / f'top_keywords_{bank.lower()}.png'
    # create a side-by-side bar chart for positive vs negative top keywords
    pos_df = pd.DataFrame(pos, columns=['word','count'])
    neg_df = pd.DataFrame(neg, columns=['word','count'])

    # focus on union of top words
    words = list(dict(pos).keys() | dict(neg).keys())[:15]

    pos_map = {k:v for k,v in pos}
    neg_map = {k:v for k,v in neg}

    data = []
    for w in words:
        data.append({'word': w, 'pos': pos_map.get(w, 0), 'neg': neg_map.get(w, 0)})

    df = pd.DataFrame(data).set_index('word')
    df = df.sort_values(by='pos', ascending=False)

    df.plot(kind='bar', figsize=(10,5))
    plt.title(f'Top keywords — positive vs negative ({bank})')
    plt.ylabel('count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def summarize(dfs, sdfs):
    # identify drivers and pain points per bank
    summary = {}
    for bank, df in dfs.items():
        pos, neg = bank_keywords(df, topn=20)
        # drivers: top positive words
        drivers = [w for w,c in pos[:10]]
        pain = [w for w,c in neg[:10]]
        avg_rating = float(df['rating'].mean())
        summary[bank] = {
            'drivers': drivers,
            'pain_points': pain,
            'avg_rating': avg_rating,
            'n_reviews': int(len(df))
        }

    # cross-bank comparisons
    comp = {
        'avg_ratings': {b: summary[b]['avg_rating'] for b in summary},
        'counts': {b: summary[b]['n_reviews'] for b in summary}
    }

    return summary, comp


def main():
    print('loading data…')
    dfs, sdfs = load_data()
    if not dfs:
        print('no processed CSVs found — ensure data/processed contains CBE.csv, BOA.csv, DB.csv')
        return

    print('generating rating distribution…')
    rdist = plot_rating_distribution(dfs)
    print('rating plot saved to', rdist)

    print('generating sentiment counts…')
    splot = plot_sentiment_counts(sdfs)
    print('sentiment plot saved to', splot)

    print('computing keywords and saving per-bank charts…')
    summary = {}
    for bank, df in dfs.items():
        pos, neg = bank_keywords(df)
        img = plot_top_keywords(bank, pos, neg)
        summary[bank] = {
            'top_positive': [p[0] for p in pos[:10]],
            'top_negative': [n[0] for n in neg[:10]],
            'keywords_img': str(img)
        }
        print(f'created keywords plot for {bank}: {img}')

    # overall summary
    bank_summary, comp = summarize(dfs, sdfs)
    out_summary = OUT_DIR / 'summary_task4.json'
    import json
    json.dump({'per_bank': summary, 'numeric_summary': bank_summary, 'comparison': comp}, open(out_summary, 'w'), indent=2)
    print('summary written to', out_summary)


if __name__ == '__main__':
    main()
