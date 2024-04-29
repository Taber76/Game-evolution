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
        new_network = NeuralNetwork(9, 2, [5, 5], 1)
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
  def __init__(self, row, col, color, brain=None):
    try:
      super().__init__()
      self.image = pygame.Surface((const.box_size, const.box_size))
      self.image.fill(color)
      self.rect = self.image.get_rect()
      self.rect.x = int(col * const.box_size)
      self.rect.y = int(row * const.box_size)
      self.row = row
      self.col = col
      self.food = const.agents_food
      self.live = const.agents_live
      self.score = 0
      self.previous_move = 4 # no move
      if brain is None:
        self.brain = NeuralNetwork(9, 2, [5, 5], 1)
      else:
        self.brain = brain
    except Exception as e:
      print('Error al crear persona en la clase: ', e)
      pass

  def move(self, world_matrix):
      try:

        # Old death
        self.live -= 1
        if self.live < 1:
          self.kill()
          return world_matrix
        
        # Eating food
        self.food -= 1
        if self.food < 1:
          self.kill()
          return world_matrix
         
        # Next terrain vector
        try:
          terrain_vector = np.zeros(9)
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
        except Exception as e:
          print('Error in terrain vector: ', e, 'wordl_matrix: ', world_matrix)
          pass

        # Brain response
        next_move = self.brain.forward(terrain_vector)

        # Move despite having food in its place
        if world_matrix[self.row][self.col][1] > 0:
          self.score -= 5

        # Move to place without food
        if terrain_vector[next_move] == 0: 
           self.score -= 5

        # Move to sea
        if terrain_vector[next_move] == -1:
           row = 1
           col = 1 
           self.score -= 20
        else:
           row = next_move // 3
           col = next_move % 3

        self.row += row - 1
        self.col += col - 1
        self.rect.x = int(self.col * const.box_size)
        self.rect.y = int(self.row * const.box_size)
        self.score += terrain_vector[next_move]

        # Update food
        if world_matrix[self.row][self.col][1] > 0:
          world_matrix[self.row][self.col][1] -= 1
          self.food += 2
          self.score += 5
          if world_matrix[self.row][self.col][1] == 0 and (world_matrix[self.row][self.col][0] == 'forest' or world_matrix[self.row][self.col][0] == 'grass'):
            world_matrix[self.row][self.col][0] = 'terrain'

        return world_matrix
      except Exception as e:
        print('Error in move: ', e)
      pass

