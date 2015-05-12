from graph import Graph
import pandas as pd
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

g = Graph()

def compute_exposure_pct(node):
    friends = node.get_friends()
    num_participants_at_completion = 0

    for friend in friends:
        if friend.completed_challenge() and friend.time_completed < node.time_nominated:
            num_participants_at_completion += 1

    return num_participants_at_completion/float(len(friends))

def compute_exposure_pcts(g):
    participants = g.get_challenge_participants()
    participants_w_min_friends = [participant for participant in participants if len(participant.get_friends()) > 50]

    raw_coord_pairs = []

    for participant in participants_w_min_friends:
        coord_pair = {'exposure_pct': compute_exposure_pct(participant), 'donated': 1 if participant.did_donate() else 0}
        raw_coord_pairs.append(coord_pair)

    return pd.DataFrame(raw_coord_pairs)

exposure_pcts = compute_exposure_pcts(g)

print exposure_pcts.describe()

logit = sm.Logit(exposure_pcts['donated'], exposure_pcts['exposure_pct'])
result = logit.fit()
print result.summary()

exposure_pcts.plot(x='exposure_pct', y='donated', kind='scatter')
plt.show()