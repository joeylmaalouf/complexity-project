from math import sqrt
from ant import Ant
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def dist(p1, p2):
  """ Calculate the distance between two points. """
  return sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

'''
  Create a graph containing 3 types of nodes:
    empty: plain old node
    food: node with infinite supply of food
    ant hill: starting point of ants, when an ant finds a food node, they travel back to their hill
  all nodes have a spatial position.
  Every hill node is connected to every empty node.
  Every empty node is connected to every food node.
  Every empty node is connected to every other empty node.

  Edges between nodes have additional fields:
    length: length between nodes
    pheromones: amount of pheromones placed upon edge by ants

  Params:
    emptyNodes -> Map<String, Tuple(Int, Int): empty nodes mapped by id to pos
    foodSources -> Map<String, Tuple(Int, Int): food sources mapped by id to pos
    antHills -> Map<String, Tuple(Int, Int): ant hills mapped by id to pos
    baseEdgeWeight -> Int: base weight of each edge before additional weighting by pheromones. Lower = stronger pheromones
'''
class FoodTravelGraph(nx.Graph):
  def __init__(self, emptyNodes, foodSources, antHills, baseEdgeWeight=1):
    super(FoodTravelGraph, self).__init__();
    self.ants = [];
    self.frames = [];
    self.baseEdgeWeight = baseEdgeWeight;
    self.emptyNodes = emptyNodes;
    self.foodSources = foodSources;
    self.antHills = antHills;

    for node in emptyNodes:
      self.add_node(node, pos=emptyNodes[node], isFood=False);

    for node in foodSources:
      self.add_node(node, pos=foodSources[node], isFood=True);

    for node in antHills:
      self.add_node(node, pos=antHills[node]["pos"], ants=antHills[node]["ants"], isFood=False);
      for ant in range(antHills[node]["ants"]):
        self.ants.append(Ant(home=node, pos=node)); # create ant

    for hill in antHills:
      for node in emptyNodes:
        # add edge between this ant hill and this empty node
        self.add_edge(hill, node, pheromones=0, length=dist(antHills[hill]["pos"], emptyNodes[node]));

        # add edges between this empty node and all food nodes
        for food in foodSources:
          self.add_edge(node, food, pheromones=0, length=dist(foodSources[food], emptyNodes[node]));

        # add edges between this empty node and all other empty nodes
        for node2 in emptyNodes:
          self.add_edge(node, node2, pheromones=0, length=dist(emptyNodes[node2], emptyNodes[node]));

  ''' 
    Every ant traverses to another node. 
    ToDo: this should factor in distance somehow.
  '''
  def step(self):
    self.decayPheromones();
    for ant in self.ants:
      if (ant.foundFood):
        # if the ant is at home, drop the food
        if (ant.pos == ant.home):
          ant.foundFood = False;
          ant.totalDistance = 0;
        # walking home
        else:
          dest = ant.visited[len(ant.visited) - 2]; # get previous node
          self.edge[ant.pos][dest]["pheromones"] += ant.getPheromones(); # add pheromones to edge as we walk back

          ant.pos = dest;
          del ant.visited[-1];
      else:
        dest, dist = self.choose(currNode=ant.pos, visited=ant.visited);
        ant.totalDistance += dist;
        ant.visit(dest);
        if (self.node[dest]["isFood"]):
          ant.foundFood = True;

    self.saveFrame();

  '''
    Reduce amount of pheromones on each edge by fixed amount
  '''
  def decayPheromones(self):
    for a, b in self.edges():
      if self.edge[a][b]["pheromones"] > 0:
        self.edge[a][b]["pheromones"] -= .01;

  '''
    Choose the next unvisited node to visit from the neighbors of currNode.

    currNode -> String: name of node which ant is on
    visited -> List[String]: list of nodes which ant has visited

    return -> String: name of node to visit,
              Int: Distance between current node and destination
  '''
  def choose(self, currNode, visited):
    unvisitedNodes = {};
    for node, edge in self[currNode].items():
      if node not in visited:
        unvisitedNodes[node] = edge;

    normalizedWeights = [self.baseEdgeWeight + edge["pheromones"] for _, edge in unvisitedNodes.items()];
    total = sum(normalizedWeights);
    normalizedWeights = [x / total for x in normalizedWeights];

    choice = np.random.choice(a = [node for node in unvisitedNodes], p = normalizedWeights);

    # if one of the nodes in unvisitedNodes has a string name and the others have numerical names, 
    # then if a numerical name is chosen it will be returned as a string
    # so we have to check for that and turn it back into a <class 'int'>
    try:
      choice = int(choice);
    except ValueError:
      pass;

    return choice, self.edge[currNode][choice]["length"];

  ''' Save pheromone levels of graph. '''
  def saveFrame(self):
    self.frames.append([self.edge[edge[0]][edge[1]]["pheromones"] for edge in self.edges()]);

  def draw(self):
    fig, ax = plt.subplots();

    for edge in self.edges():
      x1, x2 = self.node[edge[0]]["pos"][0], self.node[edge[1]]["pos"][0];
      y1, y2 = self.node[edge[0]]["pos"][1], self.node[edge[1]]["pos"][1];

      p = self.edge[edge[0]][edge[1]]["pheromones"];
      color = (0, 0, 0);
      ax.add_artist(plt.Line2D([x1, x2], [y1, y2], color=color, label='foo'));
      ax.annotate(int(p), xy=(x1 + (x2 - x1)/2, y1 + (y2 - y1)/2));

    for node in self.antHills:
      ax.add_artist(plt.Circle(self.antHills[node]["pos"], 0.1, color='red'));
      
    for node in self.emptyNodes:
      ax.add_artist(plt.Circle(self.emptyNodes[node], 0.1, color='black'));

    for node in self.foodSources:
      ax.add_artist(plt.Circle(self.foodSources[node], 0.1, color='blue'));

    plt.axis([-2, 7, -1, 6]);
    plt.show();

if __name__ == "__main__":
  emptyNodes = {
    1: (0, 0),
    2: (2, 3),
    3: (2, 5)
  };

  foodSources = {
    "food1": (4, 2)
  };

  antHills = {
    "hill1": {"pos": (-1, 3), "ants": 10}
  }

  graph = FoodTravelGraph(emptyNodes, foodSources, antHills);

  for i in range(1000):
    graph.step();

  graph.draw();

  # print("NODES");
  # print(graph.nodes(data=True));
  # print("EDGES");
  # for edge in graph.edges(data=True):
  #   print(edge)