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
  
  def growth(self, matrix):
    for i in range(len(matrix)):
       for j in range(len(matrix[i])):
        if matrix[i][j][0] != 'sea':
          matrix[i][j][1] += const.growth_speed
          if matrix[i][j][1] < const.grass_food:
            matrix[i][j][0] = 'terrain'
          elif matrix[i][j][1] < const.forest_food:
            matrix[i][j][0] = 'grass'
          elif matrix[i][j][1] > const.forest_food:
            matrix[i][j][0] = 'forest'
            if matrix[i][j][1] > const.max_food:
              matrix[i][j][1] = const.max_food
    return matrix
    
  def zoom(self, matrix, zoom_level, map_pos):
    if zoom_level == 0:
      return matrix

    map_init_corner = ( min((len(matrix) - 2 * zoom_level - 1) ,max(0, int(map_pos[0] - len(matrix)/(4*zoom_level)))), min((len(matrix[0]) - 2 * zoom_level - 1), max(0, int(map_pos[1] - len(matrix[0])/(4*zoom_level)))) )

    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[None] * cols for _ in range(rows)]

    print('map_init_corner: ', map_init_corner)
    print('matrix dimensions: ', rows, cols)
    
    for i in range(int(rows / (2 * zoom_level))):
        for j in range(int(cols / (2 * zoom_level))):
            for k in range(2 * zoom_level):
                for l in range(2 * zoom_level):
                    print('row: ', map_init_corner[0] + i * 2 * zoom_level + k)
                    print('col: ', map_init_corner[1] + j * 2 * zoom_level + l)
                    new_matrix[map_init_corner[0] + i * 2 * zoom_level + k][map_init_corner[1] + j * 2 * zoom_level + l] = matrix[map_init_corner[0] + i][map_init_corner[1] + j]

    return new_matrix   


