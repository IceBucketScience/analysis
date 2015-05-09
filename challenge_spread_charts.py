import os
from py2neo import Graph
import numpy as np
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

graph = Graph(os.environ['DB_URI'])

def get_challenge_nominated():
    return [node_data.p for node_data in graph.cypher.execute('MATCH (p:Person) WHERE has(p.timeNominated) RETURN p')]

def get_challenge_completed():
    return [node_data.p for node_data in graph.cypher.execute('MATCH (p:Person) WHERE has(p.timeCompleted) RETURN p')]

def get_challenge_donated():
    return [node_data.p for node_data in graph.cypher.execute('MATCH (p:Person) WHERE has(p.donationDate) RETURN p')]

def generate_graph_vals(participants, time_val_name):
    sorted_participants = np.sort(sorted(participants, key=lambda p: p[time_val_name], reverse=True))
    coord_pairs = np.array([])

    for participant in sorted_participants:
        time = datetime.utcfromtimestamp(participant[time_val_name])

        if coord_pairs.ndim < 2:
            coord_pairs = np.array([[time, 0]])
        elif coord_pairs[-1, 0] != time:
            new_coord_pair = np.array([time, coord_pairs[-1, 1]])
            coord_pairs = np.append(coord_pairs, np.array([new_coord_pair]), axis=0)

        coord_pairs[-1, 1] += 1

    x_vals = np.sort(coord_pairs[ : , 0])
    y_vals = np.sort(coord_pairs[ : , 1])

    return x_vals, y_vals

def get_timestamp(dt):
    return time.mktime(dt.timetuple())

def get_logistic_regression_for(x_vals, y_vals):
    return sm.Logit(y_vals, np.array([get_timestamp(val) for val in x_vals]))

def render_graph():
    nom_x_vals, nom_y_vals = generate_graph_vals(get_challenge_nominated(), 'timeNominated')
    # comp_x_vals, comp_y_vals = generate_graph_vals(get_challenge_completed(), 'timeCompleted')
    # don_x_vals, don_y_vals = generate_graph_vals(get_challenge_donated(), 'donationDate')

    plt.gca().xaxis_date()
    plt.gcf().autofmt_xdate()

    plt.plot(nom_x_vals, nom_y_vals, 'r-')
    #plt.plot(nom_x_vals, nom_y_vals, 'r-', comp_x_vals, comp_y_vals, 'b-', don_x_vals, don_y_vals, 'g-')
    
    plt.xlabel('Date')
    plt.ylabel('Num Challenged')
    plt.show()

render_graph()