from data import const
import pygame
import random

class World:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.num_rows = height // const.box_size
    self.num_cols = width // const.box_size

  # Methods  
  def get_neighbors(self, row, col):
    neighbors = []
    if row > 0:
      neighbors.append((row - 1, col))
    if row < self.num_rows - 1:
      neighbors.append((row + 1, col))
    if col > 0:
      neighbors.append((row, col - 1))
    if col < self.num_cols - 1:
      neighbors.append((row, col + 1))
    return neighbors

  def seed_terrain(self):
    seeds_list = []
    for _ in range(const.terrain_seed):
      row = random.randint(0, self.num_rows - 1)
      col = random.randint(0, self.num_cols - 1)
      seeds_list.append((row, col))
    return seeds_list
  
  def other_seed(self, terrain_list, seed_percentage): #grass, forest...
    sample = int(len(terrain_list) * seed_percentage)
    return random.sample(terrain_list, sample)
  
  def grow_seed(self, seeds_list, screen, seed_type):
    aux_seeds_list = seeds_list.copy()
    if seed_type == 'terrain':
      color = const.brown
      prob = const.terrain_prob
      grown = const.terrain_grow
    elif seed_type == 'grass':
      color = const.green
      prob = const.grass_prob
      grown = const.grass_grow
    elif seed_type == 'forest':
      color = const.dark_green
      prob = const.forest_prob
      grown = const.forest_grow
    else:
      color = const.blue
      prob = 0
      grown = 0

    for i in range(grown):
      for seed in aux_seeds_list:
        pygame.draw.rect(screen, color, (seed[1] * const.box_size, seed[0] * const.box_size, const.box_size, const.box_size))
        aux_seeds_list.remove(seed)
        grow_prob = random.random()
        if grow_prob < prob:
          neighbors = self.get_neighbors(seed[0], seed[1])
          for neighbor in neighbors:
            if neighbor not in seeds_list:
              seeds_list.append(neighbor)
              aux_seeds_list.append(neighbor)
              if i < grown - 1:
                pygame.draw.rect(screen, const.white, (neighbor[1] * const.box_size, neighbor[0] * const.box_size, const.box_size, const.box_size))
      pygame.time.wait(10)
      pygame.display.update()
    return seeds_list
  
  def assign_matrix(self, matrix, list, type):
    for coord in list:
      matrix[coord[0]][coord[1]] = [type[0], type[1]]
    return matrix
  
  def draw_matrix(self, matrix, screen):
    if matrix is None:
      return
    for row in range(self.num_rows):
      for col in range(self.num_cols):
        if matrix[row][col][0] == 'grass':
          color = const.green
        elif matrix[row][col][0] == 'forest':
          color = const.dark_green
        elif matrix[row][col][0] == 'terrain':
          color = const.brown
        else:
          color = const.blue
        pygame.draw.rect(screen, color, (col * const.box_size, row * const.box_size, const.box_size, const.box_size))
    pygame.display.update(pygame.Rect(0, 40, const.width, const.height))

  def generate_terrain(self, screen):
    screen.fill(const.blue)
    pygame.display.update()
    matrix = [[['sea', -1] for _ in range(self.num_cols)] for _ in range(self.num_rows)]
    seeds_grass_list = self.seed_terrain()
    terrain_list = self.grow_seed(seeds_grass_list, screen, 'terrain')
    grass_list = self.grow_seed(self.other_seed(terrain_list, const.terrain_prob), screen, 'grass')
    forest_list = self.grow_seed(self.other_seed(grass_list, const.grass_prob), screen, 'forest')
    matrix = self.assign_matrix(matrix, terrain_list, ['terrain', 0])
    matrix = self.assign_matrix(matrix, grass_list, ['grass', const.grass_food])
    matrix = self.assign_matrix(matrix, forest_list, ['forest', const.forest_food])
    self.draw_matrix(matrix, screen)
    
    return matrix

