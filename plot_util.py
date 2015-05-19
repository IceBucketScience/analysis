import pandas as pd
import numpy as np
from math import floor
from matplotlib.ticker import FuncFormatter

def add_binary_jitter(data, x_col, y_col, amount=0.05):
    x_vals = data.loc[:, x_col]
    y_vals = data.loc[:, y_col].apply(lambda p: np.random.normal(p, amount))
    return pd.concat([x_vals, y_vals], axis=1)

def get_binary_distribution(data, x_col, y_col, event_name, no_event_name, num_buckets=10):
    largest_x = data.loc[:, x_col].max()
    #add the constant to make sure that rounding down from this division doesn't allow for more than the number of buckets provided
    bucket_size = (largest_x + 0.0000000000001)/float(num_buckets)

    raw_vals = pd.DataFrame({x_col: np.arange(0, largest_x, bucket_size), event_name: np.zeros(num_buckets), no_event_name: np.zeros(num_buckets)})
    
    def accumulate_pair(pair):
        event_or_not = event_name if pair[y_col] == 1 else no_event_name
        raw_vals.loc[int(floor(pair[x_col]/bucket_size)), event_or_not] += 1

    data.apply(accumulate_pair, axis=1)

    def get_bucket_distribution(bucket):
        total_people = float(bucket[event_name] + bucket[no_event_name])
        return pd.Series({x_col: bucket[x_col], no_event_name: bucket[no_event_name]/total_people, event_name: bucket[event_name]/total_people, 'total_people': total_people})

    return raw_vals.apply(get_bucket_distribution, axis=1)

def plot_binary_distribution(data, x_col, x_label, y_label):
    ax = data.drop('total_people', axis=1).plot(x=x_col, kind='bar', stacked=True)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(loc=1)

    def format_label(l, pos):
        return '(' + str(int(data.loc[l, 'total_people'])) + ') ' + str(round(data.loc[l, x_col], 5))

    ax.xaxis.set_major_formatter(FuncFormatter(format_label))

def plot_normal_distributions(d1, d2, d1_name, d2_name, x_label, y_label):
    ax = d1.plot(kind='hist', alpha=0.5, bins=20, label=d1_name)
    d2.plot(ax=ax, kind='hist', alpha=0.5, bins=20, label=d2_name)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(loc=0)