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
people = pygame.sprite.Group()
world = World(const.width, const.height)
generation = 0


while run:
  try: 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
      
        # clicked on menu
        if event.pos[1] < 40:
          run, active_screen, world_matrix, people = screen_menu.handle_menu_events(event, screen, active_screen, world_matrix, people)

    #move people
    for person in people:
      new_matrix = person.move(world_matrix)
      if new_matrix is not None:
        world_matrix = new_matrix

    if len(people) > 0:
      const.year += 1
 
    if const.year > 0 and const.year % const.agents_reproduction_years == 0:
      people = reproduction(people)
      generation += 1
 
  
    #update screen
    world_matrix = world.growth(world_matrix)
    world.draw_matrix(world_matrix, screen)
    people.draw(screen)
    pygame.display.update(pygame.Rect(0, 40, const.width, const.height))
    screen_menu.update_year_population(screen, const.year, len(people), generation)
    pygame.time.wait(const.speed)

  except Exception as e:
    print('Error in main: ', e)