from math import sqrt
import matplotlib.pyplot as plt
import networkx as nx
# import numpy as np


def distance(p1, p2):
  """ Calculate the distance between two points. """
  return sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

    
class TravelGraph(nx.Graph):
  def __init__(self, cities):
    """ Initialize the graph with some custom attributes (length, pheromones). """
    super(TravelGraph, self).__init__()
    self.cities = cities
    self.add_nodes_from(cities.keys())
    for city1 in self.nodes():
      for city2 in self.nodes():
        if city1 != city2:
          self.add_edge(city1, city2, length = distance(self.cities[city1], self.cities[city2]))
    nx.set_edge_attributes(self, "pheromones", 0)
    # for e in self.edges():
    #   print(e, self[e[0]][e[1]])

  def draw(self):
    """ Draw the graph. """
    nx.draw_networkx_nodes(self, self.cities, alpha = 0.7)
    nx.draw_networkx_edges(self, self.cities, alpha = 0.3)
    nx.draw_networkx_labels(self, self.cities, alpha = 1.0)
    plt.show()


class Ant(object):
  def __init__(self, graph, start):
    """ Initialize the ant agent on a graph to traverse. """
    self.graph = graph
    self.node = start
    self.visited = [self.node]
    self.traveled = 0
    self.alive = True

  def travel(self):
    """ Choose a node to travel to, weighted via distance and pheromone trail. """
    if ant.alive:
      if len(self.visited) < len(self.graph.cities):
        choice = min(
          (i for i in self.graph[self.node].items() if i[0] not in self.visited), # change to factor in pheromones
          key = lambda x: x[1]["length"]
        )
        self.visit(choice)
      else:
        self.finish()
        self.spray()
        self.alive = False

  def visit(self, node):
    """ Visit a given node. """
    self.node = node[0]
    self.visited.append(self.node)
    self.traveled += node[1]["length"]

  def finish(self):
    """ Finish the path, traveling back to the starting node. """
    start = self.visited[0]
    self.traveled += self.graph[self.node][start]["length"]
    self.visited.append(start)
    self.node = start

  def spray(self):
    """ Leave a pheromone trail of strength inversely proportional to distance traveled. """
    for i in range(len(self.visited) - 1):
      self.graph[self.visited[i]][self.visited[i + 1]]["pheromones"] += 1.0 / self.traveled


if __name__ == "__main__":
  cities = {
    "SEATTLE":        (-122.3321, 47.6062),
    "SAN FRANCISCO":  (-122.4194, 37.7749),
    "LOS ANGELES":    (-118.2437, 34.0522),
    "SAN DIEGO":      (-117.1611, 32.7157),
    "LAS VEGAS":      (-115.1398, 36.1699),
    "PHOENIX":        (-112.0740, 33.4484),
    "SALT LAKE CITY": (-111.8910, 40.7608),
    "ALBUQUERQUE":    (-106.6056, 35.0853),
    "OKLAHOMA CITY":  (-097.5164, 35.4676),
    "HOUSTON":        (-095.3698, 29.7604),
    "INDIANAPOLIS":   (-086.1581, 39.7684),
    "ATLANTA":        (-084.3880, 33.7490),
    "MIAMI":          (-080.1918, 25.7617),
    "NEW YORK":       (-074.0059, 40.7128),
    "BOSTON":         (-071.0589, 42.3601)
  }
  num_ants = 1
  num_iterations = 20
  tg = TravelGraph(cities)
  # tg.draw()
  ants = [Ant(tg, "BOSTON") for _ in range(num_ants)]
  for _ in range(num_iterations):
    for ant in ants:
      ant.travel()
  print(ants[0].visited)
  print(ants[0].traveled)
