from random import random, randint
 
##### BEGIN CONSTANTS #####
target = 4000
number_genes = 10
bits_per_gene = 10
gene_length = number_genes * bits_per_gene
 
population_size = 100
base_mutation_rate = 0.001
##### END CONSTANTS #####
 
class Chromosome:
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness
 
def run_genetic_algorithm(num_generations=None):
    population = initialize_population()
    # print_population_info(population)
    for i in range(num_generations):
        population = simulate_generation(population)
    # print_population_info(population)
    return sum([chromosome.fitness for chromosome in population])
 
def simulate_generation(population):
    next_generation = []
    next_generation_size = 0
    while next_generation_size < population_size:
        parent1 = population[generate_weighted_index(population)]
        parent2 = population[generate_weighted_index(population)]
        if parent1 != parent2:
            next_generation.append(create_child(parent1, parent2))
            next_generation_size += 1
    return next_generation
 
def create_child(parent1, parent2):
    cross_point = randint(0, gene_length - 1)
    child_genes = parent1.genes[:cross_point] + parent2.genes[cross_point:]
    adaptive_mutation_rate = \
        base_mutation_rate / ((parent1.fitness + parent2.fitness) / 2)
    for i in range(gene_length):
        if random() <= adaptive_mutation_rate:
            new_bit = '1' if child_genes[i] == '0' else '1'
            child_genes = child_genes[:i] + new_bit + child_genes[i+1:]
    child_fitness = calculate_genetic_fitness(child_genes)
    return Chromosome(child_genes, child_fitness)
 
def initialize_population():
    population = []
    for i in range(population_size):
        genes = generate_gene(gene_length)
        fitness = calculate_genetic_fitness(genes)
        population.append(Chromosome(genes, fitness))
    return population
 
def generate_gene(length):
    max_value = 2 ** length - 1
    return bin(randint(0, max_value))[2:].rjust(length, '0')
 
def generate_weighted_index(population):
    weights = [chromosome.fitness for chromosome in population]
    threshold = random() * sum(weights)
    for index, weight in enumerate(weights):
        threshold -= weight
        if threshold < 0:
            return index
 
def calculate_genetic_fitness(genes):
    gene_list = [genes[i:i+bits_per_gene] \
                     for i in range(0, gene_length, bits_per_gene)]
    total = 0
    for gene in gene_list:
        total += int(gene, 2)
    if total == target: return 1.0
    return 1.0 / (abs(target - total) + 1)
 
def print_population_info(population):
    score = 0.0
    for chromosome in population:
        score += chromosome.fitness
        # print chromosome.genes + " - " + str(chromosome.fitness)
    print "Generation Strength: " + str(score) + "/" + str(population_size)
    print "##################################"
 
 
##### TEST CODE #####
print "WITH MUTATION (ADAPTIVE)"
total = 0.0
for i in range(100):
    total += run_genetic_algorithm(100)
total /= 100
print "AVERAGE GENETIC STRENGTH: " + str(total) + "/100"
