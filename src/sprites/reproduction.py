from data import const
from sprites.person import Person
from data import const

def reproduction(people):
  try:
    new_people = []
    for i in range(len(people) - 1):
      parent1 = people.sprites()[i]
      parent2 = people.sprites()[i + 1]
      child_brain = parent1.brain.crossover(parent2.brain).mutate(const.agents_mutation_rate)
      new_people.append(Person(parent1.row, parent1.col, const.black, child_brain))
      new_people.append(Person(parent1.row, parent1.col, const.black, parent1.brain))
    for person in new_people:
      people.add(person)

    return people

  except Exception as e:
    print('Error en reproducción: ', e)
    exit()