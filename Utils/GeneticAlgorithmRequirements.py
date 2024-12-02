from Utils import NeuralNetRequirements as nn
import torch
import numpy as np
import copy

class GeneticAlgorithm:

    def __init__(self, population_size, input_size, hidden_size, output_size, encoded_defect_data, biscuit_thresholds, roll_length, vision_range):
        self.defects_tensor = torch.stack([torch.tensor(d, dtype=torch.float32) for d in encoded_defect_data])
        self.encoded_defects = encoded_defect_data
        self.biscuit_thresholds = biscuit_thresholds
        self.roll_length = roll_length
        self.roll = [None for _ in range(roll_length)]
        self.vision_range = vision_range
        self.pop_size = population_size

        self.model = nn.BiscuitPlacementNN(input_size, hidden_size, output_size)

        self.population = self.initialize_population(population_size=population_size)

        # For later stats and plots...
        self.best_individual = None
        self.best_individuals = []
        self.avg_scores = []
        
        

    def initialize_population(self, population_size):
        population = []     # Initialize my pop matrix

        for _ in range(population_size):   # Loop through all my individuals
            
            individual = [] # We define my individual as an array. The concat of all these arrays will make my big population array.
            
            # We get and loop through the parameters of my model (inputed in the function's params)
            for param in self.model.parameters():
                # We set a random value between -1 and 1 to each of my model's parameter
                individual.append(np.random.uniform(-1, 1, param.numel()))

            # Finally, we add the individual's array to the population array.
            population.append(np.concatenate(individual))

        return np.array(population)
    
    def set_model_weights(self, weights):
        start = 0
        for param in self.model.parameters():
            numel = param.numel()  # Number of elements
            param.data = torch.tensor(weights[start:start + numel]).view(param.size()).float()
            start += numel

    def solve_ind(self, individual):
        domain = [None, 0, 1, 2, 3]
        self.set_model_weights(individual)  # Apply individual's weights to the model
        rank = 0
        tempRoll = [None for _ in range(self.roll_length)]
        predictions = self.model(self.defects_tensor)
        while rank < self.roll_length:
            index = torch.argmax(predictions[rank]).item()
            value = domain[index]
            if value is not None:
                if rank + self.biscuit_thresholds[value]['size'] < self.roll_length:
                    for i in range(rank, rank + self.biscuit_thresholds[value]['size']):
                        tempRoll[i] = value
                    rank += self.biscuit_thresholds[value]['size']
                else:
                    rank += 1
            else:
                rank +=1

        """
        while rank < len(self.defects_tensor)-self.vision_range:
            predictions = self.model(self.defects_tensor[rank:rank+self.vision_range])
            index = torch.argmax(predictions[0]).item()
            value = domain[index]
            if value is not None:
                for i in range(rank, rank + self.biscuit_thresholds[value]['size']):
                    tempRoll[i] = value
                rank += self.biscuit_thresholds[value]['size']
            else:
                rank +=1
        """
        return tempRoll
    
    def population_fitness(self):
        fitnesses = []
        index = 0
        for individual in self.population:
            score = self.fitness_function(individual)
            fitnesses.append(score)

            index +=1
        
        return fitnesses
    
    def computeRollValue(self, roll):
        totalValue = 0
        rank = 0
        while rank < len(roll):
            biscuitType = roll[rank]
            if biscuitType is not None:
                totalValue += self.biscuit_thresholds[biscuitType]['value']

                rank += self.biscuit_thresholds[biscuitType]['size']
            else:
                rank += 1

        return totalValue
    
    def penalties(self, roll):
        penalties = 0
        rank = 0
        while rank < len(roll):
            biscuitType = roll[rank]
            if biscuitType is not None:
                aCount = 0
                bCount = 0
                cCount = 0
                for i in range(rank, rank + self.biscuit_thresholds[biscuitType]['size']):
                    if self.encoded_defects[i][0] == 1:
                        aCount += 1
                    if self.encoded_defects[i][1] == 1:
                        bCount += 1
                    if self.encoded_defects[i][2] == 1:
                        cCount += 1
                rank += self.biscuit_thresholds[biscuitType]['size']

                if aCount > self.biscuit_thresholds[biscuitType]['a']:
                    penalties += 500
                if bCount > self.biscuit_thresholds[biscuitType]['b']:
                    penalties += 500
                if cCount > self.biscuit_thresholds[biscuitType]['c']:
                    penalties += 500
            else:
                penalties += 10
                rank +=1

        return penalties 
    
    def fitness_function(self, individual):
        roll = self.solve_ind(individual)
        score = self.computeRollValue(roll) - self.penalties(roll)
        return score
    
    def two_point_crossover(self, parent1, parent2):
        size = len(parent1)
        p1, p2 = sorted(np.random.choice(range(size), 2, replace=False))
        
        offspring1 = np.concatenate((parent1[:p1], parent2[p1:p2], parent1[p2:]))
        offspring2 = np.concatenate((parent2[:p1], parent1[p1:p2], parent2[p2:]))
        
        return offspring1, offspring2
    
    def tournament_selection(self, population, fitness_scores, k=3):
        selected = []
        for _ in range(2):  # Select two parents
            tournament = np.random.choice(len(population), k, replace=False)
            best = tournament[np.argmax([fitness_scores[i] for i in tournament])]
            selected.append(population[best])
            
        return selected[0], selected[1]
    
    def mutate(self, individual, mutation_rate=0.1):
        for i in range(len(individual)):
            if np.random.rand() < mutation_rate:
                individual[i] += np.random.normal(-0.1, 0.1)
        return individual
    
    def solve(self, n_elites=10, n_generations=50, mutation_rate=0.1):
        best_fitnesses = []

        # Looping through generations...
        for generation in range(n_generations):
            
            # Calculating the fitness scores, returned as an array.
            fitness_scores = self.population_fitness()

            # Track best fitness
            best_fitnesses.append(max(fitness_scores))
            print(f'Generation {generation}, Best Fitness: {max(fitness_scores):.4f}')
            #print(sorted(fitness_scores))
            # Elitism

            sorted_population = [x for _, x in sorted(zip(fitness_scores, self.population), key=lambda pair: pair[0])]
            self.best_individual = sorted_population[len(sorted_population)-1]
            self.best_individuals.append(sorted_population[len(sorted_population)-1])
            self.avg_scores.append(round(sum(fitness_scores)/len(fitness_scores),2))
            # zip is used to pair up elements from fitness_scores and population.
            # we then sort them according to the key element, which is the first value of each pair, thus, the fitness score
            # finally, x for _, x in... returns the second element of each pair, thus the individual.

            new_population = sorted_population[n_elites:]  # Top n individuals (set in prior variable n_elites)
            

            # Selection, Crossover, and Mutation
            while len(new_population) < self.pop_size:

                # We make a tournament selection to select parents. Every time we make a tournament between 4 individuals
                parent1, parent2 = self.tournament_selection(self.population, fitness_scores, 4)
                
                # We can now create an offspring out of these two parents
                offspring1, offspring2 = self.two_point_crossover(parent1, parent2)

                # We add the mutated children to the new population list
                new_population.extend([self.mutate(offspring1, mutation_rate), self.mutate(offspring2, mutation_rate)])

            # ... and set the population to be the new population
            self.population = new_population
            
        return best_fitnesses
    
    def solve_with(self, individual):
        tempRoll = self.solve_ind(individual)
        score = self.fitness_function(individual)

        return score, tempRoll


