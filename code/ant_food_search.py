from math import sqrt
from ant import Ant
import networkx as nx
import numpy as np

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
  def __init__(self, emptyNodes, foodSources, antHills, baseEdgeWeight=5):
    super(FoodTravelGraph, self).__init__();
    self.ants = [];
    self.baseEdgeWeight = baseEdgeWeight;

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
    for ant in self.ants:
      if (ant.foundFood):
        # if the ant is at home, drop the food
        if (ant.pos == ant.home):
          ant.foundFood = False;
        # walking home
        else:
          dest = ant.visited[len(ant.visited) - 2]; # get previous node
          self.edge[ant.pos][dest]["pheromones"] += ant.pheromoneStrength; # add pheromones to edge as we walk back

          ant.pos = dest;
          del ant.visited[-1];
      else:
        dest = self.choose(currNode=ant.pos, visited=ant.visited);
        ant.visit(dest);
        if (self.node[dest]["isFood"]):
          ant.foundFood = True;

  '''
    Choose the next unvisited node to visit from the neighbors of currNode.

    currNode -> String: name of node which ant is on
    visited -> List[String]: list of nodes which ant has visited

    return -> String: name of node to visit
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

    return choice


if __name__ == "__main__":
  emptyNodes = {
    1: (0, 0),
    2: (3, 3),
    3: (2, 5)
  };

  foodSources = {
    "food1": (2, 2)
  };

  antHills = {
    "hill1": {"pos": (-1, -1), "ants": 10}
  }

  graph = FoodTravelGraph(emptyNodes, foodSources, antHills);

  for i in range(100):
    graph.step();

  print("NODES");
  print(graph.nodes(data=True));
  print("EDGES");
  for edge in graph.edges(data=True):
    print(edge)