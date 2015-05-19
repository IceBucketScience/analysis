from graph import Graph
import pandas as pd
from scipy.stats import ttest_ind
from plot_util import add_binary_jitter, get_binary_distribution, plot_binary_distribution, plot_normal_distributions
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

g = Graph()

def compute_donation_exposure_pcts(g):
    participants = g.get_challenge_participants()
    participants_w_min_friends = [participant for participant in participants if len(participant.get_friends()) > 50]

    raw_coord_pairs = []

    for participant in participants_w_min_friends:
        coord_pair = {'donation_exposure_pct': participant.get_donation_exposure_pct(), 'donated': 1 if participant.did_donate() else 0}
        raw_coord_pairs.append(coord_pair)

    return pd.DataFrame(raw_coord_pairs)

exposure_pcts = compute_donation_exposure_pcts(g)

binary_distribution = get_binary_distribution(exposure_pcts, 'donation_exposure_pct', 'donated', 'donated', 'didnt_donate', 15)
print binary_distribution
#plot_binary_distribution(binary_distribution, 'donation_exposure_pct', 'donation_exposure_pct', 'pct_donated')

#add_binary_jitter(exposure_pcts, 'donation_exposure_pct', 'donated').plot(x='donation_exposure_pct', y='donated', kind='scatter', alpha=0.2)

didnt_donate = exposure_pcts[exposure_pcts['donated'] == 0].loc[:, 'donation_exposure_pct']
donated = exposure_pcts[exposure_pcts['donated'] == 1].loc[:, 'donation_exposure_pct']

plot_normal_distributions(didnt_donate, donated, 'didnt_donate', 'donated', 'donation_exposure_pct', 'frequency')

print (didnt_donate.size, didnt_donate.mean()), (donated.size, donated.mean())
print ttest_ind(didnt_donate.values, donated.values, equal_var=False)

plt.show()