from graph import Graph
import pandas as pd
from scipy.stats import ttest_ind
from plot_util import add_binary_jitter, get_binary_distribution, plot_binary_distribution, plot_normal_distributions
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

g = Graph()

def compute_exposure_pcts(g):
    participants = g.get_challenge_participants()
    participants_w_min_friends = [participant for participant in participants if len(participant.get_friends()) > 50]

    raw_coord_pairs = []

    for participant in participants_w_min_friends:
        coord_pair = {'exposure_pct': participant.get_exposure_pct(), 'participated': 1 if participant.completed_challenge() else 0}
        raw_coord_pairs.append(coord_pair)

    return pd.DataFrame(raw_coord_pairs)

exposure_pcts = compute_exposure_pcts(g)

binary_distribution = get_binary_distribution(exposure_pcts, 'exposure_pct', 'participated', 'completed', 'didnt_complete', 15)
print binary_distribution
#plot_binary_distribution(binary_distribution, 'exposure_pct', 'exposure_pct', 'pct_completed')

#add_binary_jitter(exposure_pcts, 'exposure_pct', 'participated').plot(x='exposure_pct', y='participated', kind='scatter', alpha=0.3)

didnt_participate = exposure_pcts[exposure_pcts['participated'] == 0].loc[:, 'exposure_pct']
participated = exposure_pcts[exposure_pcts['participated'] == 1].loc[:, 'exposure_pct']

plot_normal_distributions(participated, didnt_participate, 'participated', 'didnt_participate', 'exposure_pct', 'frequency')

print (didnt_participate.size, didnt_participate.mean()), (participated.size, participated.mean())
print ttest_ind(didnt_participate.values, participated.values, equal_var=False)

plt.show()