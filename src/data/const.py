#SIZES
height = 0      #deprecated
width = 0       #deprecated
box_size = 6    #pixel box

#COLORS
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 128, 0)         #grass
dark_green = (0, 50, 0)     #forest
blue = (0, 0, 255)          #sea
brown = (150, 75, 0)        #terrain

# WORLD GENERATION PROBABILITY - PERCENT
terrain_prob = 0.6  # on sea 0.6
grass_prob = 0.4    # on terrain
forest_prob = 0.2   # on grass
snow_prob = 0.1

#TERRAIN SEED
terrain_seed = 70

#GROW SHIFTS 
terrain_grow = 40
grass_grow = 8
forest_grow = 3
snow_grow = 5

#TERRAIN TYPE FOOD
grass_food = 10
forest_food = 30
snow_food = 1
growth_speed = 0.01 #recovery speed
max_food = 50

#AGENTS
agents_count = 1000         # agents at start
agents_food = 5             # food on birth
agents_max_food = 50
agents_live = 100           # years of life
agents_reproduction_years = 25
agents_mutation_rate = 0.02
agents_top_reproduction = 0.5   # Percent of top to reproduce
agents_max_generation_size = 0.5  # Percent of population new generation
agents_disease_rate = 0.05

#SCORE
score_move_if_not_food_in_own_place = 5
score_move_if_food_in_own_place = 0
score_move_if_not_food_in_the_new_place = -2
score_move_from_food_to_non_food = -10
score_move_if_not_enough_energy = -2
score_move_to_sea = -10
score_if_found_food = 2
score_max_of_generation = 0  #variable

#WORLD DATA
speed = 10
generation = 0
year = 0
dead_for_disease = 0
dead_for_age = 0
dead_for_food = 0
dead_for_drowning = 0