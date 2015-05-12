from graph import Graph
import pandas as pd
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

g = Graph()

def calc_mutual_friends_index(p1, p2):
    all_friends = pd.concat([p1.get_friends(), p2.get_friends()])
    print all_friends.shape
    mutual_friend_count = 0

    for friend in all_friends:
        if friend.is_friends_with(p1) and friend.is_friends_with(p2):
            mutual_friend_count += 1

    print p1.name, p2.name, mutual_friend_count

    return mutual_friend_count/float(len(all_friends))

def calc_mutual_friends_indexes(g):
    nominations = g.get_nominations()
    
    raw_coord_pairs = []

    for index, nomination in nominations.iterrows():
        coord_pair = {'mutual_friends_index': calc_mutual_friends_index(nomination['source'], nomination['target']), 'completed': 1 if nomination['target'].completed_challenge() else 0}
        raw_coord_pairs.append(coord_pair)

    return pd.DataFrame(raw_coord_pairs)

mutual_friends_indexes = calc_mutual_friends_indexes(g)

print mutual_friends_indexes.describe()

logit = sm.Logit(mutual_friends_indexes['completed'], mutual_friends_indexes['mutual_friends_index'])
result = logit.fit()
print result.summary()

mutual_friends_indexes.plot(x='mutual_friends_index', y='completed', kind='scatter')
plt.show()
