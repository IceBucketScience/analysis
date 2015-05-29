from util.graph import Graph
import pandas as pd
from util.significance import test_significance
from util.plot import add_binary_jitter, get_binary_distribution, plot_binary_distribution, plot_normal_distributions
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

g = Graph()

def calc_network_overlaps(g):
    nominations = g.get_nominations()
    
    raw_coord_pairs = []

    for index, nomination in nominations.iterrows():
        if nomination['target'].completed_challenge() and ((not nomination['source'].is_volunteer and not nomination['target'].is_volunteer) or (nomination['target'].is_volunteer and nomination['source'].is_volunteer)):
            coord_pair = {'network_overlap': nomination['source'].get_network_overlap_with(nomination['target']), 'donated': 1 if nomination['target'].did_donate() else 0}
            raw_coord_pairs.append(coord_pair)

    return pd.DataFrame(raw_coord_pairs)

network_overlaps = calc_network_overlaps(g)

binary_distribution = get_binary_distribution(network_overlaps, 'network_overlap', 'donated', 'donated', 'didnt_donate', 15)
print binary_distribution
#plot_binary_distribution(binary_distribution, 'network_overlap', 'network_overlap', 'pct_donated')
network_overlaps.plot(x='network_overlap', y='donated', kind='scatter')
#add_binary_jitter(network_overlaps, 'network_overlap', 'donated').plot(x='network_overlap', y='donated', kind='scatter', alpha=0.2)

didnt_donate = network_overlaps[network_overlaps['donated'] == 0].loc[:, 'network_overlap']
donated = network_overlaps[network_overlaps['donated'] == 1].loc[:, 'network_overlap']

#plot_normal_distributions(didnt_donate, donated, 'didnt_donate', 'donated', 'network_overlap', 'frequency')

test_significance(didnt_donate, donated)

plt.show()
