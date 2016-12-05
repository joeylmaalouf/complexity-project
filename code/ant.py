class Ant():
  def __init__(self, home, pos, pheromoneStrength=1):
    self.home = home;
    self.pos = pos;
    self.foundFood = False;
    self.pheromoneStrength = pheromoneStrength;
    self.totalDistance = 0;
    self.visited = [];
    self.visited.append(home);

  '''
    Get current pheromone strength. Pheromones get weaker as the ant walk 
    further up until it finds food.

    return -> Float: pheromone strength
  '''
  def getPheromones(self):
    return self.pheromoneStrength / (self.totalDistance * 2);

  def visit(self, dest):
    self.pos = dest;
    self.visited.append(dest);