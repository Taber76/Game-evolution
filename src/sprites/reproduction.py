import random
from data import const
from sprites.person import Person
from data import const

def reproduction(people, world_matrix):
  try:
    if len(people) < 20: # no posible reproduction
      return people
    
    shorted_people = sorted(people, key=lambda person: person.score, reverse=True)        
    best_parents = shorted_people[:int(len(people) * const.agents_top_reproduction)]
    max_childs = int(len(people) * const.agents_max_generation_size) 

    childs = []
    number_of_childs = 0

    const.score_max_of_generation = best_parents[0].score
 
    for i in range(len(best_parents) - 2): # best parent cross over all, second best parent next, ex...
      for j in range(i + 2, len(best_parents)):
        if number_of_childs >= max_childs:
          break
        parent1 = best_parents[i]
        parent2 = best_parents[j]
        if parent1.food > 15 and parent2.food > 15:
          parent1.food -= const.agents_food / 2
          parent2.food -= const.agents_food / 2
          child_brain = parent1.brain.crossover(parent2.brain).mutate(const.agents_mutation_rate)
          while True:
            col = random.randint(0, len(world_matrix[0]) - 1)
            row = random.randint(0, len(world_matrix) - 1)
            if world_matrix[row][col][0] != 'sea':
              break
          childs.append(Person(row, col, const.black, 'Black', child_brain))   # cross over
          childs.append(Person(row, col, const.black, 'Black', parent1.brain)) # copy of parent
          number_of_childs += 2

    for child in childs:
      people.add(child)

    return people

  except Exception as e:
    print('Error en reproducción: ', e)
    exit()