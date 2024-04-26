import pygame
import pickle
import random

from controllers.world import World
from sprites.person import Person
from data import const

def handle_menu_events(event, screen, active_screen, world_matrix, people):
  try:
    run = True # no exit from menu
    if active_screen == 'main':     
        #Start Game
        if event.pos[0] < 200:

            #Create People
            for _ in range(const.agents_count):
                while True:
                    col = random.randint(0, len(world_matrix[0]) - 1)
                    row = random.randint(0, len(world_matrix) - 1)
                    if world_matrix[row][col][0] != 'sea':
                        break
                try:
                    people.add(Person(row, col, const.black))
                except Exception as e:
                    print('Error al crear persona: ', e)
                    pass
              
        #Load Map
        elif event.pos[0] < 400:
            with open('./src/data/map.dat', 'rb') as file:
                world_matrix = pickle.load(file)
            world = World(const.width, const.height)
            world.draw_matrix(world_matrix, screen)
            main_menu(screen)
        
        #New Map
        elif event.pos[0] < 600:
            world = World(const.width, const.height)
            world_matrix = world.generate_terrain(screen)
            map_menu(screen)
            active_screen = 'map'
        
        #Exit
        elif event.pos[0] < 800:
            print('exit')
            run = False
            
    elif active_screen == 'map':
        #Use Map
        if event.pos[0] < 200:
            with open('./src/data/map.dat', 'wb') as file:
                pickle.dump(world_matrix, file)
            main_menu(screen)
            active_screen = 'main'
        
        #Generate Map
        elif event.pos[0] < 400:
            world = World(const.width, const.height)
            world_matrix = world.generate_terrain(screen)
            map_menu(screen)
        
        #Main Menu
        elif event.pos[0] < 600:
            main_menu(screen)
            active_screen = 'main'
   
    return run, active_screen, world_matrix, people

  except Exception as e:
    print('Error on handle_menu_events', e, event.pos)
    pass

def main_menu(screen):
    menu = pygame.Surface((const.width, 40))
    menu.fill(const.black)
    font = pygame.font.Font(None, 36)
    text_start = font.render("Start Game", True, const.white)
    text_load = font.render("Load Map", True, const.white)
    text_new = font.render("New Map", True, const.white)
    text_exit = font.render("Exit", True, const.white)
    text_year = font.render("Year: " + str(const.year), True, const.white)
    menu.blit(text_start, (10, 5))
    menu.blit(text_load, (200, 5))
    menu.blit(text_new, (400, 5))
    menu.blit(text_exit, (600, 5))
    menu.blit(text_year, (1000, 5))
    screen.blit(menu, (0, 0))
    pygame.display.update()

def map_menu(screen):
    menu = pygame.Surface((const.width, 40))
    menu.fill(const.black)
    font = pygame.font.Font(None, 36)
    text_load = font.render("Use Map", True, const.white)
    text_new = font.render("New Map", True, const.white)
    text_exit = font.render("Exit", True, const.white)
    menu.blit(text_load, (10, 5))
    menu.blit(text_new, (200, 5))
    menu.blit(text_exit, (400, 5))
    screen.blit(menu, (0, 0))
    pygame.display.update()


def update_year_population(screen, year, population):
    font = pygame.font.Font(None, 36)
    text_year = font.render("Year: " + str(year), True, const.white)
    text_population = font.render("Population: " + str(population), True, const.white)
    screen.blit(text_year, (1000, 5))
    screen.blit(text_population, (1400, 5))
    pygame.display.update(pygame.Rect(1000, 5, const.width, 40))