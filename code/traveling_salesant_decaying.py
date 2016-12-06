from traveling_salesant import *

class DecayingGraph(TravelGraph):
  def step(self, decay_amount = 0.1):
    for city1, city2 in self.edges():
      self[city1][city2]["pheromones"] -= min(self[city1][city2]["pheromones"], decay_amount)


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
  best = None
  generations = 1000
  population = 1000
  dg = DecayingGraph(cities)
  for _ in range(generations):
    dg.step(population/1000.0)
    ants = [Ant(dg, "BOSTON") for _ in range(population)]
    for ant in ants:
      ant.travel()
      if best is None or ant.traveled < best.traveled:
        best = ant
  print(best.visited)
  print(best.traveled)
  dg.draw(best.visited, draw_edges=False)

'''
Current best with this code:
['BOSTON', 'MIAMI', 'ATLANTA', 'HOUSTON', 'PHOENIX', 'LAS VEGAS', 'SAN DIEGO', 'LOS ANGELES', 'SAN FRANCISCO', 'SEATTLE', 'SALT LAKE CITY', 'ALBUQUERQUE', 'OKLAHOMA CITY', 'INDIANAPOLIS', 'NEW YORK', 'BOSTON']
139.053186595
'''
