from itertools import izip, product
from math import sqrt
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


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

  def draw(self, path = None, draw_nodes = True, draw_edges = True, draw_labels = True):
    """ Draw the graph, optionally highlighting a given path. """
    if draw_nodes:
      nx.draw_networkx_nodes(
        G = self,
        pos = self.cities,
        alpha = 0.5,
        node_color = "k"
      )
    if draw_edges:
      nx.draw_networkx_edges(
        G = self,
        pos = self.cities,
        alpha = 0.25,
        edge_color = "r"
      )
    if draw_labels:
      nx.draw_networkx_labels(
        G = self,
        pos = {city: (pos[0], pos[1] + 1.5) for city, pos in self.cities.items()},
        alpha = 1.0,
        font_color = "k"
      )
    if path:
      nx.draw_networkx_edges(
        G = self,
        pos = {city: self.cities[city] for city in path},
        edgelist = [(path[i], path[(i + 1) % len(path)]) for i in range(len(path))],
        alpha = 1.0,
        edge_color = "g"
      )
    plt.show()


class Ant(object):
  def __init__(self, graph, start, dist_weight = 5, pher_weight = 10, generation = 0):
    """ Initialize the ant agent on a graph to traverse. """
    self.graph = graph
    self.node = start
    self.visited = [self.node]
    self.traveled = 0
    self.dist_weight = float(dist_weight)
    self.pher_weight = float(pher_weight)
    self.generation = generation

  def travel(self):
    """ Travel between nodes until every one has been visited. """
    while len(self.visited) < len(self.graph.cities):
      choice = self.choose()
      self.visit(choice)
    self.finish()
    self.spray()

  def choose(self):
    """ Select a node to travel to, making decisions based on distance and pheromone trail. """
    choices = [c for c in self.graph[self.node].items() if c[0] not in self.visited]
    weights = [self.dist_weight / c[1]["length"] + c[1]["pheromones"] for c in choices]
    total = sum(weights)
    weights = [w * 1.0 / total for w in weights]
    choice = np.random.choice(a = [c[0] for c in choices], p = weights)
    return (choice, self.graph[self.node][choice])

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
      self.graph[self.visited[i]][self.visited[i + 1]]["pheromones"] += self.pher_weight / self.traveled


def evaluate(generations, population, dist_weight, pher_weight, decay = False, decay_amount = 0.025):
  """ Evaluate one instance of the algorithm. """
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
  best = None
  tg = TravelGraph(cities)
  for g in range(1, generations + 1):
    if decay:
      for city1, city2 in tg.edges():
        tg[city1][city2]["pheromones"] -= min(tg[city1][city2]["pheromones"], decay_amount)
    ants = [Ant(tg, "BOSTON", dist_weight, pher_weight, g) for _ in range(population)]
    for ant in ants:
      ant.travel()
      if best is None or (ant.visited != best.visited and ant.traveled < best.traveled):
        best = ant
  # print(best.generation)
  # print(best.traveled)
  # print(best.visited)
  # tg.draw(best.visited)
  return best


def grid_search(hyperparam_ranges):
  """ Find the best hyperparameter combination. """
  runs = {}
  for p in [dict(izip(hyperparam_ranges, r)) for r in product(*hyperparam_ranges.values())]:
    # print(p)
    runs[tuple(p.values())] = evaluate(**p)
  return runs

if __name__ == "__main__":
  # results = grid_search({
  #   "generations": [100, 500, 1000, 1500, 2000],
  #   "population": [100, 500, 1000, 1500, 2000],
  #   "dist_weight": [1, 5, 10],
  #   "pher_weight": [1, 5, 10]
  # })
  # results = sorted(results.items(), key = lambda x: (x[1].traveled, x[1].generation))
  # for r in results:
  #   print(r[0], r[1].generation, r[1].traveled, r[1].visited)
  ant = evaluate(2000, 2000, 5.0, 10.0)
  print(ant.generation)
  print(ant.traveled)
  print(ant.visited)
