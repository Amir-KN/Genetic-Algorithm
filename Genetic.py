import random
import copy

P_crossover = 0.7
P_mutation = 0.001
P_carry = 0.4
population_len = 1000

class EquationSolver:
    
    def __init__(self, operators, operands, equationLen, goal_number):
        self.operators = operators
        self.operands = operands
        self.equationLen = equationLen
        self.goal_number = goal_number
        self.population = self.create_first_population()
        
    def create_first_population(self):
        population = []
        for _ in range(population_len) :
            new_chromosome = []
            for __ in range(self.equationLen//2):
                new_chromosome.append(random.choice(self.operands))
                new_chromosome.append(random.choice(self.operators))
            new_chromosome.append(random.choice(self.operands))
            population.append([new_chromosome, 0])

        return population

    def calc_fitness(self, population):
        for chromosome in population :
            chromosome_str = "".join(list(map(str, chromosome[0])))
            evaluate = abs(eval(chromosome_str) - self.goal_number)
            chromosome[1] = 1/(evaluate+1)

    def solve_EP(self):

        while (True):
            random.shuffle(self.population)
            self.calc_fitness(self.population)

            # If we have result, return it
            for i in range(population_len): 
                if self.population[i][1] == 1 :
                    return self.population[i][0]

            # Choose the chromoseme with high fitnesss to ttansfer next generation
            carried_chromosomes, best_chromosome = [], copy.deepcopy(self.population)
            best_chromosome.sort(reverse=True, key=lambda x : x[1])
            for i in range(0, int(population_len*P_carry)):
                carried_chromosomes.append(best_chromosome[i]) 

            # Chromosomes after crossover
            crossover_pool = self.do_crossover(copy.deepcopy(self.population))

            # Delete previous population for create new population
            self.population.clear()

            # Create New population from crossoverd chromosome and 
            # best chromosome in previous generation
            for i in range(population_len - int(population_len*P_carry)):
                self.population.append(self.do_mutation(crossover_pool[i]))
                
            # Add the best chromosome in previous generation
            self.population.extend(carried_chromosomes)
    
    
    def do_crossover(self, matingPool):
        crossover_pool, parents = [], []

        for i in range(len(matingPool)-1):
            if random.random() > P_crossover:
                crossover_pool.append(matingPool[i])
            else:
                parents.append(matingPool[i])

        for chromosome1, chromosome2 in zip(parents, parents[1:]):
            i = random.randint(1,self.equationLen-2)
            child1 = chromosome1[0][:i] + chromosome2[0][i:]
            child2 = chromosome2[0][:i] + chromosome1[0][i:]
            crossover_pool.append([child1, 0])
            crossover_pool.append([child2, 0])

        self.calc_fitness(crossover_pool)
        crossover_pool.sort(reverse=True, key=lambda x : x[1])

        return crossover_pool
    
    def do_mutation(self, chromosome):
        mutated_chromosome = copy.deepcopy(chromosome[0])
        for i, gen in enumerate(mutated_chromosome) :
            r = random.random()
            if r < P_mutation :
                if gen in self.operands :
                    mutated_chromosome[i] = random.choice(self.operands)
                else :
                    mutated_chromosome[i] = random.choice(self.operators)
        new_chro = [mutated_chromosome, 0]
        self.calc_fitness([new_chro])

        return new_chro

def get_input() :
    equationLen = int(input())
    operands = list(map(int, input().split()))
    operators = input().split()
    goal_number = int(input())
    return equationLen, operands, operators, goal_number 



### You can set input manually in the program OR read from a file(standard input) ###

## input 1
# operands = [1, 2, 3, 4, 5, 6, 7, 8]
# operators = ['+', '-', '*']
# equationLen = 21
# goal_number = 18019

## input 2
operands = [1, 2, 3, 4, 5, 6, 7, 8, 9]
operators = [ '*', '+', '%', '-']
equationLen = 25
goal_number = 139967

# equationLen, operands, operators, goal_number = get_input()
  
equation_splver = EquationSolver(operators, operands, equationLen, goal_number)
equation = equation_splver.solve_EP()
print(''.join(list(map(str, equation))))