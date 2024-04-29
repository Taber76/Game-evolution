from data import const
from sprites.person import Person
from data import const

def reproduction(people):
  try:
    shorted_people = sorted(people, key=lambda person: person.score, reverse=True)        
    if len(shorted_people) < const.agents_top_reproduction:
      best_parents = shorted_people
    else:
      best_parents = shorted_people[:const.agents_top_reproduction]

    childs = []

    print('best_parent: ', best_parents[0].score)

    for i in range(len(best_parents) - 2): # best parent cross over all, second best parent next, ex...
      for j in range(i + 2, len(best_parents)):
        parent1 = best_parents[i]
        parent2 = best_parents[j]
        child_brain = parent1.brain.crossover(parent2.brain).mutate(const.agents_mutation_rate)
        childs.append(Person(parent1.row, parent1.col, const.black, child_brain))   # cross over
        childs.append(Person(parent1.row, parent1.col, const.black, parent1.brain)) # copy of parent
    
    for child in childs:
      people.add(child)

    return people

  except Exception as e:
    print('Error en reproducción: ', e)
    exit()