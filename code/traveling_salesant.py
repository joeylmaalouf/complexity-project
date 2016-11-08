from math import sqrt
import matplotlib.pyplot as plt
import networkx as nx


class TSA(object):
  def __init__(self, cities):
    self.cities = cities
    self.graph = nx.Graph()
    self.graph.add_nodes_from(cities.keys())
    for city1 in self.graph:
      for city2 in self.graph:
        if city1 != city2:
          self.graph.add_edge(city1, city2, length = distance(self.cities[city1], self.cities[city2]))

  def draw(self):
    nx.draw_networkx_nodes(self.graph, self.cities, alpha = 0.7)
    nx.draw_networkx_edges(self.graph, self.cities, alpha = 0.3)
    nx.draw_networkx_labels(self.graph, self.cities, alpha = 1.0)
    plt.show()


def distance(p1, p2):
  return sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)


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
  t = TSA(cities)
  t.draw()
