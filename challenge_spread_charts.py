import os
from py2neo import Graph
import numpy as np
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
from tablib import Dataset

mpl.interactive(False)

graph = Graph(os.environ['DB_URI'])

def get_challenge_nominated():
    return [node_data.p for node_data in graph.cypher.execute('MATCH (p:Person) WHERE has(p.timeNominated) RETURN p')]

def get_challenge_completed():
    return [node_data.p for node_data in graph.cypher.execute('MATCH (p:Person) WHERE has(p.timeCompleted) RETURN p')]

def get_challenge_donated():
    return [node_data.p for node_data in graph.cypher.execute('MATCH (p:Person) WHERE has(p.donationDate) RETURN p')]

def generate_graph_vals(participants, time_val_name):
    sorted_participants = np.array(sorted(participants, key=lambda p: p[time_val_name]))
    coord_pairs = np.array([])

    for participant in sorted_participants:
        time = datetime.utcfromtimestamp(participant[time_val_name])

        if coord_pairs.ndim < 2:
            coord_pairs = np.array([[time, 0]])
        elif coord_pairs[-1, 0] != time:
            new_coord_pair = np.array([time, coord_pairs[-1, 1]])
            coord_pairs = np.append(coord_pairs, np.array([new_coord_pair]), axis=0)

        coord_pairs[-1, 1] += 1

    x_vals = coord_pairs[ : , 0]
    y_vals = coord_pairs[ : , 1]

    return x_vals, y_vals

def get_graph_values():
    nom_x_vals, nom_y_vals = generate_graph_vals(get_challenge_nominated(), 'timeNominated')
    comp_x_vals, comp_y_vals = generate_graph_vals(get_challenge_completed(), 'timeCompleted')
    don_x_vals, don_y_vals = generate_graph_vals(get_challenge_donated(), 'donationDate')

    return {
        'nominated': (nom_x_vals, nom_y_vals),
        'completed': (comp_x_vals, comp_y_vals),
        'donated': (don_x_vals, don_y_vals)
    }

def render_graph(nominated_vals, completed_vals, donated_vals):
    plt.xlabel('Date')
    plt.ylabel('Total People')

    plt.gca().xaxis_date()
    plt.gcf().autofmt_xdate()

    nominated, = plt.plot(nominated_vals[0], nominated_vals[1], 'r-', label='nominated')
    completed, = plt.plot(completed_vals[0], completed_vals[1], 'b-', label='completed')
    donated, = plt.plot(donated_vals[0], donated_vals[1], 'g-', label='donated')

    plt.legend([nominated, completed, donated], ['Nominated', 'Completed', 'Donated'], loc=2)
    
    plt.show()

def export_to_csv(vals, filename):
    data = Dataset()

    data.append_col(vals[0], header='Date')
    data.append_col(vals[1], header='Total People')

    file = open(filename, 'w')
    file.write(data.csv)
    file.close()

graph_vals = get_graph_values()

#export_to_csv(graph_vals['nominated'], 'nominated_graph.csv')

render_graph(graph_vals['nominated'], graph_vals['completed'], graph_vals['donated'])