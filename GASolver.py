import numpy
import random
import math

class GASolver:
    # equation should be passed as a function
    # num_weights is fundamentally how many variables we need to consider
    # is_maximizing, boolean it's either True if maximizing or False if minimizing, by default maximizing
    def __init__(self, equation, num_weights, nonlincon = None, is_maximizing = True,  is_verbose = True):
        self.equation = equation
        self.num_weights = num_weights
        self.nonlincon = nonlincon
        self.is_maximizing = is_maximizing
        self.is_verbose = is_verbose
    
    # Bounds should be a vector bounds(0) is the lb, bounds(1) is ub, used for initialization, does not limit later
    # spp means solutions per population
    # max_num_generations is the num of iterations to perform GA for
    # num_mating_parents is the number of mating parents to produce
    # rep_cutoff is the number of times an answer should be expected to repeat before an early termination
    def solve(self, bounds, spp, num_mating_parents, rep_cutoff = 15, max_num_generations = math.inf):
        if num_mating_parents <= 1:
            print("Warning: need more than 1 mating parent for this to work")
            num_mating_parents = num_mating_parents + 1
        # TODO handle edge case spp = 2, num mating parents = 1
        if num_mating_parents >= spp:
            print("Warning: Selected num mating parents is greater than total number of population \n")
            print("Setting num_mating_parents to spp - 1 \n")
            print("Recommend restarting with num_mating_parents << spp \n")
            num_mating_parents = spp - 1
        

        population_size = (spp, self.num_weights)
        current_population = numpy.random.uniform(low = bounds[0], high= bounds[1], size = population_size)
        #print(current_population)

        current_generation = 0
        num_rep = 0
        prev_answer = 0
        while current_generation < max_num_generations:
            current_generation = current_generation + 1
            fitness_values = GASolver.calculate_population_fitness(self.equation, current_population, self.nonlincon, self.is_maximizing)

            extreme_value = GASolver.get_extreme_value(self.is_maximizing,current_generation,fitness_values, self.is_verbose)

            if current_generation == 0:
                prev_answer = extreme_value 
            else:
                if prev_answer == extreme_value:
                    num_rep = num_rep + 1
                else:
                    prev_answer = extreme_value
                    num_rep = 0
            if num_rep == rep_cutoff:
                print("----- Computation Exited: Exceeded " + str(rep_cutoff) + " repetitions ------")
                current_generation = current_generation - 1
                break;

            #print(fitness_values)
            mating_parents = GASolver.select_mating_parents(num_mating_parents, fitness_values, current_population, self.is_maximizing)
            # Assume replacement of existing population except selected parents
            offspring = GASolver.calculate_offspring(mating_parents, spp - num_mating_parents, self.num_weights)

            new_population = GASolver.consolidate_populations(mating_parents,offspring)
            current_population = new_population
        
        final_fitness_values = GASolver.calculate_population_fitness(self.equation, current_population, self.nonlincon, self.is_maximizing)
        ordered_indices = GASolver.order_items(final_fitness_values)
        
        optimum_solution = current_population[ordered_indices[0]]
        if self.is_maximizing:
            print("Final Output in Generation " + str(current_generation) + " : " + str(max(final_fitness_values)))
            print("Provided by solution: " + str(optimum_solution))
        else:
            optimum_solution = current_population[ordered_indices[len(ordered_indices)-1]]
            print("Final Output in Generation " + str(current_generation) + " : " + str(min(final_fitness_values)))
            print("Provided by solution: " + str(optimum_solution))
        return optimum_solution

    def get_extreme_value(is_maximizing, current_generation, fitness_values, is_verbose):
        extreme_value = 0
        if is_maximizing:
            if is_verbose:
                print("Maximum Value in Generation " + str(current_generation - 1) + " : " + str(max(fitness_values)))
            extreme_value = max(fitness_values)
        else:
            if is_verbose:
                print("Minimum Value in Generation " + str(current_generation - 1) + " : " + str(min(fitness_values)))
            extreme_value = min(fitness_values)
        return extreme_value

    def consolidate_populations(mating_parents, offspring):
        #print(mating_parents)
        #print(offspring)
        new_population = []
        for parent in mating_parents:
            new_population.append(parent)
        for child in offspring:
            new_population.append(child)
        #print(new_population)
        return new_population

    def calculate_offspring(parents, offspring_size, num_weights):
        crossover_offspring = GASolver.perform_crossover(parents,offspring_size, num_weights)
        calculated_offspring = GASolver.perform_mutation(crossover_offspring)
        return calculated_offspring

    # TODO change number of mutations to be flexible
    def perform_mutation (offspring):
        #print(offspring)
        for current_offspring in offspring:
            num_genes_to_alter = 1
            if (len(current_offspring) > 2):
                num_genes_to_alter = random.randint(1,len(current_offspring)-2)
            genes_altered = 0
            previously_altered = []
            while genes_altered < num_genes_to_alter:
                # TODO in small numbers this can take more time than I'd like try to optimize the gene selection method
                index_affected_gene = random.randint(0,len(current_offspring)-1)
                while index_affected_gene in previously_altered:
                    index_affected_gene = random.randint(0,len(current_offspring)-1)
                previously_altered.append(index_affected_gene)
                # Currently randomly adds in the order of -1 to 1, not good for big changes
                #considered just adding but too small, only multiplying will prevent switching signage, so use both
                current_offspring[index_affected_gene] = current_offspring[index_affected_gene]*(1+random.uniform(-0.1,0.1))
                # Add a modifier but only sometimes
                if round(current_offspring[index_affected_gene] * 10 ** 6) == 0 and random.randint(0,1) ==  1:
                    current_offspring[index_affected_gene] = current_offspring[index_affected_gene] + random.uniform(-0.01,0)
                genes_altered = genes_altered + 1
            
        #print(offspring)
        return offspring

    def perform_crossover(parents, offspring_size, num_weights):
        offspring = []
        # TODO Have the option to do more random selection for weights, easier to just divide by 2
        pivot = num_weights/2
        current_parent_index = 0
        while (len(offspring) < offspring_size):
            current_child = []
            
            # TODO This could be a time waster if there are too few elements, remove from list then look for index 
            p1_index =random.randint(0,len(parents)-1)
            p2_index = random.randint(0,len(parents)-1)
            while p2_index == p1_index:
                p2_index = random.randint(0,len(parents)-1)
            
            parent_1 = parents[p1_index]
            parent_2 = parents[p2_index]

            current_item_index = 0
            while current_item_index < pivot:
                current_child.append(parent_1[current_item_index])
                current_item_index = current_item_index + 1
            while current_item_index < len(parent_2):
                current_child.append(parent_2[current_item_index])
                current_item_index = current_item_index + 1
            
            offspring.append(current_child)
        
        #print(offspring)
        return offspring
    
    def calculate_population_fitness(fitness_function, population, nonlincon, is_maximizing):
        fitness_values = []
        for parent in population:
            fitness_score = fitness_function(parent)
            conditions_satisfied = True

            # Iterate over non-linear conditions
            if not nonlincon == None:
                for condition in nonlincon:
                    if condition(parent) > 0:
                        conditions_satisfied = False
            
            if not conditions_satisfied:
                # TODO adjust penalty to be dynamic or manually altered
                penalty = 1000
                if is_maximizing:
                    fitness_score = fitness_score - penalty
                else:
                    fitness_score = fitness_score + penalty

            fitness_values.append(fitness_score)
        return fitness_values

    # Return ordered list of indices (from index of largest to index of smallest)
    def order_items(fitness_values):
        ordered_indices = [0]
        current_index = 1
        while current_index < len(fitness_values):
            sub_index = 0
            while sub_index < len(ordered_indices) and fitness_values[current_index] < fitness_values[ordered_indices[sub_index]]:
                sub_index = sub_index + 1
            ordered_indices.insert(sub_index,current_index)
            current_index = current_index + 1
        return ordered_indices

    def select_mating_parents(num_mating_parents, fitness_values, current_population, is_maximizing):
        ordered_indices = GASolver.order_items(fitness_values)
        #print(ordered_indices)
        #print(fitness_values)
        #print(current_population)
        
        current_index = 0
        operation = GASolver.iterate_forwards
        if not is_maximizing:
            current_index = len(ordered_indices) - 1
            operation = GASolver.iterate_backwards

        selected_parents = []
        while (len(selected_parents) < num_mating_parents):
            selected_parents.append(current_population[ordered_indices[current_index]])
            current_index = operation(current_index)
        #print(selected_parents)
        return selected_parents
        
        
    def iterate_forwards(num):
        return num + 1
    def iterate_backwards(num):
        return num - 1
