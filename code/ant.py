class Ant():
  def __init__(self, home, pos, pheromoneStrength=1):
    self.home = home;
    self.pos = pos;
    self.foundFood = False;
    self.pheromoneStrength = pheromoneStrength;
    self.visited = [];
    self.visited.append(home);

  def visit(self, dest):
    self.pos = dest;
    self.visited.append(dest);