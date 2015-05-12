from graph import Graph
import pandas as pd
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

g = Graph()

def compute_donation_exposure_pct(node):
    friends = node.get_friends()
    num_participants_at_completion = 0
    num_donors_at_completion = 0

    for friend in friends:
        if friend.completed_challenge() and friend.time_completed < node.time_nominated:
            num_participants_at_completion += 1
        if friend.did_donate() and friend.time_donated < node.time_nominated:
            num_donors_at_completion += 1

    return num_donors_at_completion/float(num_participants_at_completion) if num_participants_at_completion > 0 else 0

def compute_donation_exposure_pcts(g):
    participants = g.get_challenge_participants()
    participants_w_min_friends = [participant for participant in participants if len(participant.get_friends()) > 50]

    raw_coord_pairs = []

    for participant in participants_w_min_friends:
        coord_pair = {'donation_exposure_pct': compute_donation_exposure_pct(participant), 'donated': 1 if participant.did_donate() else 0}
        raw_coord_pairs.append(coord_pair)

    return pd.DataFrame(raw_coord_pairs)

exposure_pcts = compute_donation_exposure_pcts(g)

print exposure_pcts.describe()

logit = sm.Logit(exposure_pcts['donated'], exposure_pcts['donation_exposure_pct'])
result = logit.fit()
print result.summary()

exposure_pcts.plot(x='donation_exposure_pct', y='donated', kind='scatter')
plt.show()