from util.graph import Graph
import pandas as pd
import statsmodels.api as sm
import numpy as np
from util.significance import test_significance
from util.plot import add_binary_jitter, get_binary_distribution, plot_binary_distribution, plot_normal_distributions
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

g = Graph()

def compute_exposure_pcts(g):
    participants = g.get_challenge_participants()
    participants_w_min_friends = [participant for participant in participants if len(participant.get_friends()) >= 50]

    raw_coord_pairs = []

    for participant in participants_w_min_friends:
        coord_pair = {'exposure_pct': participant.get_exposure_pct(), 'participated': 1 if participant.completed_challenge() else 0}
        raw_coord_pairs.append(coord_pair)

    return pd.DataFrame(raw_coord_pairs)

exposure_pcts = compute_exposure_pcts(g)

binary_distribution = get_binary_distribution(exposure_pcts, 'exposure_pct', 'participated', 'completed', 'didnt_complete', 15)
print binary_distribution
#plot_binary_distribution(binary_distribution, 'exposure_pct', 'exposure_pct', 'pct_completed')

ax = add_binary_jitter(exposure_pcts, 'exposure_pct', 'participated').plot(x='exposure_pct', y='participated', kind='scatter', alpha=0.3)

# logit = sm.Logit(exposure_pcts['exposure_pct'], exposure_pcts['participated'])
# reg_result = logit.fit()
# print reg_result.summary()

# x_vals = np.linspace(exposure_pcts['exposure_pct'].min(), exposure_pcts['exposure_pct'].max(), 20)
# pd.DataFrame({'x': x_vals, 'y': logit.cdf(x_vals)}).plot(x='x', y='y', ax=ax)

didnt_participate = exposure_pcts[exposure_pcts['participated'] == 0].loc[:, 'exposure_pct']
participated = exposure_pcts[exposure_pcts['participated'] == 1].loc[:, 'exposure_pct']

#plot_normal_distributions(participated, didnt_participate, 'participated', 'didnt_participate', 'exposure_pct', 'frequency')

test_significance(didnt_participate, participated)

plt.show()