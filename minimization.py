"""

Author = Abdellah TOUNSI
This module contains Pools class that is adapted to trigger the
evolution of number of populations(Pools) with a specific 
genom type.

"""
from typing import Callable, List, Tuple
from random import random
from copy import deepcopy
from math import sqrt
import numpy as np

class Pools:
    """
    This class minimizes a function of specific number of parameters
    Pools re different populations governed by genetic evolution 
    and natural selection.
    
    Attributes:
        fun: Callable: function to be minimized.
        bounds: List[Tuple]: bounds of adjustable function's arguments.
        n_pools: int: number of populations.
        pools: List[List]: list of the generation of populations.
            
    """
    def __init__(self, fun, n_pools, bounds):
        self.fun = fun
        self.bounds = bounds
        self.n_pools = n_pools
        self.pools = []
    
    def generate(self, pool_size):
        """
        generates initial random popolations(pools).
        """
        widths = []
        for bound in self.bounds:
            widths.append(bound[1] - bound[0])
        for n in range(self.n_pools):
            pool = []
            for i in range(pool_size):
                genom = []
                for width, bound in zip(widths, self.bounds):
                    genom.append(random() * width + bound[0])  
                pool.append(genom)
                
            self.pools.append(pool)
            
    def evolve(self, n_gen, mutation_rate):
        """
        triggers evolution of all current populations over n_gen generations.
        """
        for i, pool in enumerate(self.pools):
            self.pools[i] = genetic(self.fun, self.bounds, pool,
                           mutation_rate,
                           n_gen)
    def pick_elites(self):
        """
        returns the elite list of best genoms from each population.
        """
        elites = []
        for pool in self.pools:
            elites.append(pool[0])
        return elites
        
def generate_elite(population, elite_size):
    """
        Finds the first 'elite_size' elements of population by their scores and
        returns them.
    """
    elite = []
    pop = deepcopy(population)
    for i in range(elite_size):
        index = 0
        best_element = pop[index]
        for i, element in enumerate(pop):
            if element[1] < best_element[1]:
                index, best_element = i, element
        elite.append(best_element)
        del pop[index]
    return elite

def cross(genom1, genom2, mutation_rate, widths, bounds):
    """
         Generates a child_genom by breeding 2 parent_genoms with
         a mutation chance = mutation rate = [0, 1].
    """
    child_genom = []
    for i in range(len(genom1)):
        if widths[i] == 0:
            child_genom.append(genom1[i])
            continue
        if random() < mutation_rate:
            #   Mutation
            child_genom.append(random() * widths[i] + bounds[i][0])
        else:
            #   Breeding
            rand = round(random())
            child_genom.append(rand * genom1[i] + (1-rand) * genom2[i])
    return child_genom

def genetic(fun, bounds, pool,
            mutation_rate,
            n_gen):
    """
    triggers evolution of one population (pool) over n_gen generations.
    """
    pool_size = len(pool)
    widths = []
    for bound in bounds:
        widths.append(bound[1] - bound[0])
    elite = []
    for genom in pool:
        elite.append([genom, fun(genom)])

    for gen in range(n_gen):
        
        last_pop = deepcopy(elite)
        for i in range(pool_size):
            for j in range(pool_size):
                if j == i:
                    continue
                # Breed and mutate
                child_genom = cross(elite[i][0], elite[j][0],
                              mutation_rate, widths,
                              bounds)
                
                last_pop.append([child_genom, fun(child_genom)])

        elite = generate_elite(last_pop, pool_size)
    pool = []
    for element in elite:
        pool.append(element[0])
    return pool
    
