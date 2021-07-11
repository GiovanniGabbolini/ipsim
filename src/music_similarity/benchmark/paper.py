"""
Created on Sun Apr 04 2021

@author Giovanni Gabbolini
"""

from src.music_similarity.benchmark.similar_items import *
from src.music_similarity.benchmark.recommendation import *
from src.music_similarity.benchmark.metrics import *
from src.music_similarity.algorithms.segue_based_similarity import *
from scipy.stats import wilcoxon
import pandas as pd
from collections import OrderedDict
from src.utils.experiments import trunc
import numpy as np
import logging
import matplotlib.pyplot as plt
import random
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
from src.interestingness.interestingness_GB import interestingness
from src.knowledge_graph.walk_graph import find_segues
from src.knowledge_graph.segues_filtering import nodes_types_to_filter_loose
from src.music_similarity.dataset import load_dataset
from src.canned_texts.segue_canned_texts import segue_canned_texts
from src.utils.musicbrainz_setup import musicbrainzngs_setup
plt.style.use('science')

"""This file replicates the tables to be found in the paper.
"""


def fix_names(df):
    """Does changes to row and column names.

    It assumes the df has 4 rows with four algorithms in this order:
    1) random;
    2) count-segues;
    3) LDSD;
    4) ipsim;

    It assumes to have 4 columns with four metrics:
    - ndcg @5;
    - ndcg @10;
    - precision @5;
    0 precision @10;

    Args:
        df (Pandas df)

    Returns:
        [Pandas df]: same df, but with:
                     - columns arranged in a fixed way (['ndcg @5', 'ndcg @10', 'precision @5', 'precision @10', ]);
                     - columns names with all the needed upper case letters: ndcg -> nDCG, precision -> Pr;
                     - algorithms names  with all the needed upper case letters.
    """
    assert len(df) == 4
    df = df[sorted(df.columns, key=lambda x: len(x))]
    assert list(df.columns.values) == ['ndcg @5', 'ndcg @10', 'precision @5', 'precision @10', ]
    df = df.rename({'ndcg @10': r'\textit{nDCG@10}', 'ndcg @5': r'\textit{nDCG@5}',
                    'precision @10': r'\textit{Pr@10}', 'precision @5': r'\textit{Pr@5}'}, axis=1)
    df.index = [r'\random{}', r'\countsegues{}', r'\ldsd{}', r'\ipsim{}']
    return df


def significance_test(local_metrics):
    """Do statistical significance test.

    It compares LDSD and IPSim.

    It assumes:
    - to have a key LDSD;
    - that the last key on the ordered dict is IPSim;
    - to have four metrics.

    Args:
        local_metrics (Ordered dict)

    Returns:
        p-values on ['ndcg @5', 'ndcg @10', 'precision @5', 'precision @10', ]
    """
    metrics = ['ndcg @5', 'ndcg @10', 'precision @5', 'precision @10', ]
    pvalues = []

    LDSD = local_metrics['LDSD']
    key_ipsim = list(local_metrics.keys())[-1]
    assert 'ipsim_best_params' in key_ipsim
    ipsim = local_metrics[key_ipsim]

    for metric in metrics:
        score_LDSD = [l[metric] for l in LDSD]
        score_ipsim = [l[metric] for l in ipsim]
        w, p = wilcoxon(score_LDSD, score_ipsim)
        pvalues.append(p)

    return pvalues


def table_performance(algorithm):
    digits = 3
    local_metrics = algorithm(cutoff_list=[5, 10])
    assert local_metrics.__class__ == OrderedDict
    global_metrics = {k: aggregate_metrics(local_metrics[k]) for k in local_metrics.keys()}
    df = pd.DataFrame(global_metrics).T
    df = fix_names(df)
    p = significance_test(local_metrics)
    for j in range(len(df.columns)):
        argmax_value = np.argmax(df.iloc[:, j].values)
        for i in range(len(df)):
            if i == argmax_value:

                significance_suffix = ''
                if p[j] <= 0.05 and p[j] > 0.01:
                    significance_suffix = '*'
                elif p[j] <= 0.01 and p[j] > 0.001:
                    significance_suffix = '**'
                elif p[j] <= 0.001:
                    significance_suffix = '***'

                df.iloc[i, j] = r'\textbf{' + trunc(df.iloc[i, j], digits) + r'}' + r'$^{' + significance_suffix + r'}$'
            else:
                df.iloc[i, j] = trunc(df.iloc[i, j], digits)

    s = "\\begin{table} \n"
    s += df.to_latex(column_format=f'|l{"|l"*df.shape[1]}|', escape=False)
    s += "\\caption{} \n \\label{} \n \\end{table}"
    s = s.replace(r'\midrule', '').replace(r'\bottomrule', '').replace(r'\toprule', r'\hline')
    s = s.replace(r'\\', r'\\ \hline')
    print(s)


def figure(algorithms, titles):
    params = {'legend.fontsize': 8,
              "font.family": "serif",
              "font.serif": ["Times"], }
    mpl.rcParams.update(params)
    cutoffs = [1]+list(range(5, 100, 5))+[100]
    algs = [r"\textsc{IPSim}", r"\textsc{LDSD}", r"\textsc{Count}", r"\textsc{Rnd}"]
    style_lines = [{'color': 'dimgray', 'linestyle': 'solid'}, {'color': 'darkgray', 'linestyle': 'solid'},
                   {'color': 'dimgray', 'linestyle': 'dashed'}, {'color': 'darkgray', 'linestyle': 'dashed'}, ]
    fig, axes = plt.subplots(1, len(algorithms), figsize=(8, 3))
    for j in range(len(algorithms)):
        ax = axes[j]
        local_metrics = algorithms[j](cutoff_list=cutoffs)
        global_metrics = {k: aggregate_metrics(local_metrics[k]) for k in local_metrics.keys()}
        for i, k in enumerate(list(global_metrics.keys())[::-1]):
            y = [global_metrics[k][f'precision @{c}'] for c in cutoffs]
            x = [c for c in cutoffs]
            ax.plot(x, y, label=algs[i], **style_lines[i])
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
        ax.set_xlabel(r"\textit{N}")
        ax.set_xticks([0, 20, 40, 60, 80, 100])
        ax.set_title(titles[j], fontdict={'fontsize': 10})

    axes[0].set_ylabel(r"\textit{Pr@N}")
    axes[-1].legend()
    plt.tight_layout()
    plt.savefig('plot', dpi=600)


def case_study():
    musicbrainzngs_setup()
    dataset = 'mirex'
    random.seed(22)

    similar_items_ground_truth = load_dataset(dataset, f'similar_items_ground_truth_validation')
    graph = load_dataset(dataset, 'graph')

    S = list(similar_items_ground_truth.keys())
    I = [item['id'] for item in load_dataset(dataset, 'items')]

    algorithm = SegueBasedSimilarity(**{'dataset': dataset, 'aggregation_strategy': best_params_mirex_similarity})
    matrix = algorithm.similarity_matrix(S, I)

    seed = random.choice(range(len(S)))
    most_similar = np.argmax(matrix[seed, :])

    segues = find_segues(graph.nodes()[S[seed]]['graph'], graph.nodes()[I[most_similar]]['graph'],
                         pre_filtering=None, post_filtering=None, nodes_types_to_filter=nodes_types_to_filter_loose)
    segues = [segue for segue in segues if len(segue_type(segue)) <= 15]
    scores = interestingness(segues, 0.3, 0.1, 0.6)
    segues = sorted(segues, key=lambda segue: -scores[segues.index(segue)])
    texts = [segue_canned_texts(segue, 'short') for segue in segues]
    scores = interestingness(segues, 0.3, 0.1, 0.6)

    s = r"\begin{table}[t] \begin{tabular}{ | l|l|} \multicolumn{2}{c}{George Jones is most similar Tammy Wynette.} \\ \hline Explanation & Int \\ \hline"
    for text, score in zip(texts, scores):
        s += f"\n {text} & {trunc(score, 2)}" + r" \\ \hline"
    s += r"\end{tabular} \caption{} \end{table}"
    print(s)


def mirex_similarity(cutoff_list):
    split = 'test'
    dataset = 'mirex'
    local_metrics = similar_items([
        (Random, {'dataset': dataset}),
        (SegueBasedSimilarity, {'dataset': dataset, 'aggregation_strategy': count_segues}),
        (LDSD, {'dataset': dataset}),
        (SegueBasedSimilarity, {'dataset': dataset, 'aggregation_strategy': best_params_mirex_similarity}),
    ], dataset=dataset, cutoff=cutoff_list, split=split)
    return local_metrics


def lastfm_similarity(cutoff_list):
    split = 'test'
    dataset = 'lastfmapi'
    local_metrics = similar_items([
        (Random, {'dataset': dataset}),
        (SegueBasedSimilarity, {'dataset': dataset, 'aggregation_strategy': count_segues}),
        (LDSD, {'dataset': dataset}),
        (SegueBasedSimilarity, {'dataset': dataset, 'aggregation_strategy': best_params_lastfm_similarity}),
    ], dataset=dataset, cutoff=cutoff_list, split=split)
    return local_metrics


def lastfm_recommendation(cutoff_list):
    split = 'test'
    dataset = 'lastfmrecommender'
    metrics = ['accuracy']
    local_metrics = OrderedDict()

    algorithm = Random(dataset)
    similarity_matrix = retrieve_similarity_matrix(algorithm, dataset)
    local_metrics[algorithm.name()] = recommendation(similarity_matrix, dataset, split=split, metrics=metrics, top_k=5, cutoff=cutoff_list)

    algorithm = SegueBasedSimilarity(**{'dataset': dataset, 'aggregation_strategy': count_segues})
    similarity_matrix = retrieve_similarity_matrix(algorithm, dataset)
    local_metrics[algorithm.name()] = recommendation(similarity_matrix, dataset, split=split, metrics=metrics, top_k=10, cutoff=cutoff_list)

    algorithm = LDSD(dataset)
    similarity_matrix = retrieve_similarity_matrix(algorithm, dataset)
    local_metrics[algorithm.name()] = recommendation(similarity_matrix, dataset, split=split, metrics=metrics, top_k=40, cutoff=cutoff_list)

    algorithm = SegueBasedSimilarity(**{'dataset': dataset, 'aggregation_strategy': best_params_lastfm_recommender})
    similarity_matrix = retrieve_similarity_matrix(algorithm, dataset)
    local_metrics[algorithm.name()] = recommendation(similarity_matrix, dataset, split=split, metrics=metrics, top_k=40, cutoff=cutoff_list)

    return local_metrics


def facebook_recommendation(cutoff_list):
    split = 'test'
    dataset = 'facebookrecommender'
    metrics = ['accuracy']
    local_metrics = OrderedDict()

    algorithm = Random(dataset)
    similarity_matrix = retrieve_similarity_matrix(algorithm, dataset)
    local_metrics[algorithm.name()] = recommendation(similarity_matrix, dataset, split=split, metrics=metrics, top_k=1, cutoff=cutoff_list)

    algorithm = SegueBasedSimilarity(**{'dataset': dataset, 'aggregation_strategy': count_segues})
    similarity_matrix = retrieve_similarity_matrix(algorithm, dataset)
    local_metrics[algorithm.name()] = recommendation(similarity_matrix, dataset, split=split, metrics=metrics, top_k=1, cutoff=cutoff_list)

    algorithm = LDSD(dataset)
    similarity_matrix = retrieve_similarity_matrix(algorithm, dataset)
    local_metrics[algorithm.name()] = recommendation(similarity_matrix, dataset, split=split, metrics=metrics, top_k=7, cutoff=cutoff_list)

    algorithm = SegueBasedSimilarity(**{'dataset': dataset, 'aggregation_strategy': best_params_facebook_recommender})
    similarity_matrix = retrieve_similarity_matrix(algorithm, dataset)
    local_metrics[algorithm.name()] = recommendation(similarity_matrix, dataset, split=split, metrics=metrics, top_k=None, cutoff=cutoff_list)

    return local_metrics


if __name__ == '__main__':
    # figure([lastfm_recommendation, facebook_recommendation], [r'(a) \textit{LastFM-h}', r'(b) \textit{Facebook}', ])
    table_performance(mirex_similarity)
