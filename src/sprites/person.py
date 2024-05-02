import pygame
import numpy as np

from data import const

class NeuralNetwork:
    def __init__(self, input_size, hidden_layers, hidden_sizes, output_size):
        self.hidden_sizes = hidden_sizes
        self.weights = []
        prev_size = input_size
        for i in range(hidden_layers):
            if i == hidden_layers - 1:
                self.weights.append(np.random.uniform(-1, 1, (prev_size, output_size))) # last hidden layer
            else:
                self.weights.append(np.random.uniform(-1, 1, (prev_size, hidden_sizes[i]))) # hidden layer
            prev_size = hidden_sizes[i]
                
    def forward(self, X):
        try:
          activations = [X]
          for i in range(len(self.weights)):
              activations.append(self.sigmoid(np.dot(activations[-1], self.weights[i])))
          output = round(activations[-1][0] * 8)
          return output
        except Exception as e:
          print('Error al hacer forward en la clase: ', e)
          pass

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def crossover(self, other_network):
        new_network = NeuralNetwork(12, 2, [5, 5], 1)
        for i in range(len(self.weights)):
            crossover_point = np.random.randint(self.weights[i].shape[0])
            new_network.weights[i][:crossover_point] = self.weights[i][:crossover_point]
            new_network.weights[i][crossover_point:] = other_network.weights[i][crossover_point:]
        return new_network

    def mutate(self, mutation_rate):
        for i in range(len(self.weights)):
            mask = np.random.rand(*self.weights[i].shape) < mutation_rate
            mutation = np.random.uniform(-0.5, 0.5, self.weights[i].shape)
            self.weights[i] += mask * mutation
  


class Person(pygame.sprite.Sprite):
  def __init__(self, row, col, color, tribe, brain=None):
    try:
      super().__init__()
      self.image = pygame.Surface((const.box_size, const.box_size))
      self.image.fill(color)
      self.tribe = tribe
      self.rect = self.image.get_rect()
      self.rect.x = int(col * const.box_size)
      self.rect.y = int(row * const.box_size)
      self.row = row
      self.col = col
      self.food = const.agents_food
      self.live = const.agents_live
      self.score = 0
      self.stamina = 10    # 0 - 100  
      self.energy = 50     # 0 - 100
      self.previous_food = const.agents_food
      if brain is None:
        self.brain = NeuralNetwork(12, 2, [5, 5], 1)
      else:
        self.brain = brain
    except Exception as e:
      print('Error al crear persona en la clase: ', e)
      pass

  def move(self, world_matrix):
      try:

        # Old death
        self.live -= 1
        if self.live + self.stamina / 2 + self.energy / 2 < 1:
          self.kill()
          const.dead_for_age += 1
          return world_matrix
        
        # Eating food and death for hungry
        if self.food > 0:
          self.food -= .2
          self.energy = min(100, self.energy + 10)
        elif self.energy < 5:
          self.kill()
          const.dead_for_food += 1
          return world_matrix
        
        # Disease
        disease_prob_death = const.agents_disease_rate * ( 0.2 * (1 - self.stamina / 100) + 0.8 * (1 - self.energy / 100))
        if np.random.uniform(0, 1) < disease_prob_death:
          self.kill()
          const.dead_for_disease += 1
          return world_matrix

        # Next terrain vector and self food
        try:
          terrain_vector = np.zeros(12)
          ele = 0
          for i in range(-1, 2):
            for j in range(-1, 2):
              if self.row + i < 0 or self.row + i >= len(world_matrix) or self.col + j < 0 or self.col + j >= len(world_matrix[0]): # out of bounds
                terrain_vector[ele] = -1
              elif world_matrix[self.row + i][self.col + j][0] == 'sea':
                terrain_vector[ele] = -1
              else:
                terrain_vector[ele] = world_matrix[self.row + i][self.col + j][1]
              ele += 1

          # self entries for brain
          terrain_vector[9] = self.food
          terrain_vector[10] = self.stamina
          terrain_vector[11] = self.energy
        except Exception as e:
          print('Error in terrain vector: ', e)
          pass

        # Brain response
        next_move = self.brain.forward(terrain_vector)

        # Up stamina if move and down energy
        if next_move == 4:  # not move
          self.stamina = max(self.stamina - 2.5, 0)
          self.energy = max(self.energy - 2.5, 0)
        else:                # move
          self.stamina = min(self.stamina + 5, 100)   
          self.energy = max(self.energy - 5, 0)           
     

        # SCORES
        # Not move and not food in its place
        if world_matrix[self.row][self.col][1] < 1 and terrain_vector[next_move] != 4:
          self.score += const.score_move_if_not_food_in_own_place

        # Move despite having food in its place
        if world_matrix[self.row][self.col][1] > 1 and terrain_vector[next_move] != 4:
          self.score += const.score_move_if_food_in_own_place

        # Move from place with food to place without food
        if world_matrix[self.row][self.col][1] > 1 and terrain_vector[next_move] < 1:
          self.score += const.score_move_from_food_to_non_food

        # Move to place without food
        if terrain_vector[next_move] < 1: 
           self.score += const.score_move_if_not_food_in_the_new_place

        # Move
        if terrain_vector[next_move] == -1:                        # sea?
           const.dead_for_drowning += 1
           self.kill()
           return world_matrix
           #row = 1
           #col = 1 
           #self.score += const.score_move_to_sea
        elif terrain_vector[next_move] != 4 and self.energy < 5: # not move
           row = 1
           col = 1
           self.score += const.score_move_if_not_enough_energy
        else:                                                       # move
           row = next_move // 3
           col = next_move % 3

        self.row += row - 1
        self.col += col - 1
        self.rect.x = int(self.col * const.box_size)
        self.rect.y = int(self.row * const.box_size)
        self.score += terrain_vector[next_move]

        # Update food
        if world_matrix[self.row][self.col][1] > 1:
          if self.food < const.agents_max_food:
            world_matrix[self.row][self.col][1] -= 1
            self.food += 1
          self.score += const.score_if_found_food
          if world_matrix[self.row][self.col][1] == 0 and (world_matrix[self.row][self.col][0] == 'forest' or world_matrix[self.row][self.col][0] == 'grass'):
            world_matrix[self.row][self.col][0] = 'terrain'

        return world_matrix
      except Exception as e:
        print('Error in move: ', e)
      pass

