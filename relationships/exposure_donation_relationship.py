from util.graph import Graph
import pandas as pd
from util.significance import test_significance
from util.plot import add_binary_jitter, get_binary_distribution, plot_binary_distribution, plot_normal_distributions
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

g = Graph()

def compute_exposure_pcts(g):
    participants = g.get_completed()
    participants_w_min_friends = [participant for participant in participants if len(participant.get_friends()) >= 50]

    raw_coord_pairs = []

    for participant in participants_w_min_friends:
        coord_pair = {'exposure_pct': participant.get_exposure_pct(), 'donated': 1 if participant.did_donate() else 0}
        raw_coord_pairs.append(coord_pair)

    return pd.DataFrame(raw_coord_pairs)

exposure_pcts = compute_exposure_pcts(g)

binary_distribution = get_binary_distribution(exposure_pcts, 'exposure_pct', 'donated', 'donated', 'didnt_donate', 10)
print binary_distribution
#plot_binary_distribution(binary_distribution, 'exposure_pct', 'exposure_pct', 'pct_donated')

#add_binary_jitter(exposure_pcts, 'exposure_pct', 'donated').plot(x='exposure_pct', y='donated', kind='scatter', alpha=0.2)

didnt_donate = exposure_pcts[exposure_pcts['donated'] == 0].loc[:, 'exposure_pct']
donated = exposure_pcts[exposure_pcts['donated'] == 1].loc[:, 'exposure_pct']

plot_normal_distributions(didnt_donate, donated, 'didnt_donate', 'donated', 'exposure_pct', 'frequency')

test_significance(didnt_donate, donated)

plt.show()