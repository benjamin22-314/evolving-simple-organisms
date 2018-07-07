
import numpy as np
import datetime

# import our files.
import plotting
from organism import Organism
from food import Food
from simulate import simulate
from evolve import evolve
import nn_maths_functions
import make_gif

# --- CONSTANTS --------------------------------------------------------+

settings = {}

# EVOLUTION SETTINGS
settings['pop_size'] = 10       # number of organisms
settings['food_num'] = 10      # number of food particles
settings['gens'] = 6           # number of generations
settings['elitism'] = 0.20      # elitism (selection bias)
settings['mutate'] = 0.10       # mutation rate

# SIMULATION SETTINGS
settings['seed'] = 33           # for reproducibility
settings['time_steps'] = 100    # time steps in a generation

settings['x_min'] = -2.0        # arena western border
settings['x_max'] = 2.0        # arena eastern border
settings['y_min'] = -2.0        # arena southern border
settings['y_max'] = 2.0        # arena northern border

# GIF
settings['plot'] = True                         # plot final generation?
settings['plot_generations'] = [0, 3]           # plot these generations as well as the final gen
settings['gif_name'] = 'the coolest gif'        # gif name will include generation
settings['gif_fps'] = 12                        # frames per second
settings['datetime'] = datetime.datetime.now().strftime(' %Y-%m-%d %H-%M-%S')

# ORGANISM NEURAL NET SETTINGS
settings['velocity_decay_factor'] = 0.2     # velocity decay factor, so the fish has momentum
settings['inodes'] = 4                      # number of input nodes
settings['hnodes'] = 5                      # number of hidden nodes
settings['onodes'] = 2                      # number of output nodes


def run(settings):

    # --- SET RANDOM SEED ----
    np.random.seed(settings['seed'])

    # --- POPULATE THE ENVIRONMENT WITH FOOD ---------------+
    foods = []
    for i in range(0, settings['food_num']):
        foods.append(Food(settings))

    # --- POPULATE THE ENVIRONMENT WITH ORGANISMS ----------+
    organisms = []
    for i in range(0, settings['pop_size']):
        wih_init = np.random.uniform(-1, 1, (settings['hnodes'], settings['inodes']))     # mlp weights (input -> hidden)
        who_init = np.random.uniform(-1, 1, (settings['onodes'], settings['hnodes']))     # mlp weights (hidden -> output)

        organisms.append(Organism(settings, wih_init, who_init, name='gen[x]-org['+str(i)+']'))

    # --- CYCLE THROUGH EACH GENERATION --------------------+
    for gen in range(0, settings['gens']):

        # SIMULATE
        organisms = simulate(settings, organisms, foods, gen)

        # make gif with the plotted images

        # EVOLVE
        organisms, stats = evolve(settings, organisms, gen)
        print('> GEN:', gen, 'BEST:', stats['BEST'], 'AVG:', stats['AVG'], 'WORST:', stats['WORST'])


if __name__ == '__main__':
    run(settings)
