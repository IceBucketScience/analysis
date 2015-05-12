import os
from py2neo import Graph
import pandas as pd
from datetime import datetime

graph = Graph(os.environ['DB_URI'])

class Node():
    def __init__(self, db_node):
        self.id = db_node._id
        self.name = db_node['name']
        self.is_volunteer = 'isIndexed' in db_node.properties
        self.time_nominated = datetime.utcfromtimestamp(db_node['timeNominated']) if 'timeNominated' in db_node.properties else None
        self.time_completed = datetime.utcfromtimestamp(db_node['timeCompleted']) if 'timeCompleted' in db_node.properties else None
        self.time_donated = datetime.utcfromtimestamp(db_node['donationDate']) if 'donationDate' in db_node.properties else None
        self.is_first_donation = db_node['isFirstDonation']

        self.friends = {}

        self.nominated_by = {}
        self.nominated = {}

    def add_friend(self, friend):
        self.friends[friend.id] = friend

    def add_nominated_by(self, nominator):
        self.nominated_by[nominator.id] = nominator

    def add_nominated(self, nominee):
        self.nominated[nominee.id] = nominee

    def was_nominated(self):
        return not self.time_nominated is None

    def completed_challenge(self):
        return not self.time_completed is None

    def did_donate(self):
        return not self.time_donated is None

    def get_friends(self):
        return pd.Series(self.friends)

    def is_friends_with(self, node):
        return node.id in self.friends

class Graph():
    def __init__(self):
        self.graph = graph

        self.nodes = pd.Series({node._id: Node(node) for node in self.__get_nodes_from_db()})

        self.friendships = self.__get_relationships_from_db('FRIENDS')
        self.nominations = self.__get_relationships_from_db('NOMINATED')

        self.__add_friendships_to_nodes()
        self.__add_nominations_to_nodes()

        print 'GRAPH RETRIEVED'

    def __get_nodes_from_db(self):
        return self.graph.find('Person')

    def __get_relationships_from_db(self, rel_name):
        raw_rels = self.graph.cypher.execute('MATCH (p1)-[:' + rel_name + ']->(p2) RETURN Id(p1) AS p1, Id(p2) AS p2')
        
        return pd.DataFrame([{'source': rel.p1, 'target': rel.p2} for rel in raw_rels])

    def __add_friendships_to_nodes(self):
        for index, friendship in self.friendships.iterrows():
            p1, p2 = self.nodes[friendship['source']], self.nodes[friendship['target']]
            p1.add_friend(p2)
            p2.add_friend(p1)

    def __add_nominations_to_nodes(self):
        for index, nomination in self.nominations.iterrows():
            nominator, nominee = self.nodes[nomination['source']], self.nodes[nomination['target']]
            nominator.add_nominated(nominee)
            nominee.add_nominated_by(nominator)

    def get_challenge_participants(self):
        return pd.Series([node for node in self.nodes if node.was_nominated()])

    def get_donors(self):
        return pd.Series([node for node in self.nodes if node.did_donate()])

    def get_nominations(self):
        return self.nominations.applymap(lambda p: self.nodes[p])
