import pygame
from data import const
from controllers.world import World
from screen import screen_menu
from sprites.reproduction import reproduction

pygame.init()

# Start screen
screen_info = pygame.display.Info()
const.width = screen_info.current_w
const.height = screen_info.current_h
screen = pygame.display.set_mode((const.width, const.height), pygame.FULLSCREEN)
screen.fill(const.blue)
pygame.display.set_caption("LivePlay")
screen_menu.main_menu(screen)

run = True
active_screen = 'main'
clock = pygame.time.Clock()
world_matrix = None
view_matrix = None
zoom_level = 0
map_pos = (int(const.width / 2 / const.box_size), int(const.height / 2 / const.box_size))
people = pygame.sprite.Group()
world = World(const.width, const.height)
generation = 0


while run:
  try: 

    #User events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.MOUSEBUTTONDOWN: 
        # clicked on menu
        if event.pos[1] < 40:
          run, active_screen, world_matrix, people = screen_menu.handle_menu_events(event, screen, active_screen, world_matrix, people)
        # clicked on map
        elif event.button == 4: # zoom in, mouse wheel up
          if zoom_level < 5:
            zoom_level += 1
            map_pos = (int(event.pos[0] / const.box_size), int(event.pos[1] / const.box_size))
            #view_matrix = world.zoom(world_matrix, zoom_level, map_pos)
        elif event.button == 5: # zoom out, mouse wheel down
          if zoom_level > 0:
            zoom_level -= 1
            map_pos = (int(event.pos[0] / const.box_size), int(event.pos[1] / const.box_size))

    #Move people
    for person in people:
      new_matrix = person.move(world_matrix)
      if new_matrix is not None:
        world_matrix = new_matrix

    if people is not None:
      if len(people) > 0:
        const.year += 1
        #Update world growth
        world_matrix = world.growth(world_matrix)
 
    if const.year > 0 and const.year % const.agents_reproduction_years == 0:
      people = reproduction(people, world_matrix)
      generation += 1
      print('----------------------------------------------')
      print('Generation: ', generation)
      print('Population: ', len(people))
      print('Deaths for older:    ', const.dead_for_age, ' - ', int(const.dead_for_age / len(people) * 100), '%', sep='')
      print('Deaths for food:     ', const.dead_for_food, ' - ', int(const.dead_for_food / len(people) * 100), '%', sep='')
      print('Deaths for disease:  ', const.dead_for_disease, ' - ', int(const.dead_for_disease / len(people) * 100), '%', sep='')
      print('Deaths for drowning: ', const.dead_for_drowning, ' - ', int(const.dead_for_drowning / len(people) * 100), '%', sep='')
      const.dead_for_age = 0
      const.dead_for_food = 0
      const.dead_for_disease = 0
      const.dead_for_drowning = 0
    

    #Update zoom
    if view_matrix is None and world_matrix is not None:
      view_matrix = world_matrix.copy()
    else:
      view_matrix = world.zoom(view_matrix, zoom_level, map_pos)
    
    #Update screen
    world.draw_matrix(view_matrix, screen)
    people.draw(screen)
    pygame.display.update(pygame.Rect(0, 40, const.width, const.height))
    screen_menu.update_year_population(screen, const.year, len(people), generation)
    pygame.time.wait(const.speed)

  except Exception as e:
    print('Error in main: ', e)