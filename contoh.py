import numpy as np
from random import sample

h = lambda x, y: ((np.cos(x) + np.sin(y))**2) / x**2 + y**2

def decode(kromosom, r_b, r_a):
    # rubah dengan for loop biasa tanpa 1 line function
    
    pembagi = 0
    pengali = 0
    for i in range(1, len(kromosom) + 1):
        pembagi += 2 ** -i
        pengali += kromosom[i-1] * (2 ** -i)
    
    # exp = [2 ** -i for i in range(1, len(kromosom) + 1)]
    # g_exp = sum(g * e for g, e in zip(kromosom, exp))
    
    # return r_b + ((r_a - r_b) // sum(exp)) * g_exp
    # print(pembagi, pengali)
    return r_b + ((r_a - r_b) / pembagi) * pengali
  
def fitness(krom):
    # ganti krom[..] dengan perhitungan angka dlu
    N = len(krom)
    
    # print(krom)
    krom_x = krom[0:4]
    krom_y = krom[4:]
    # print(krom_x, krom_y)
    
    x = decode(krom_x, -5, 5)
    y = decode(krom_y, -5, 5)
    # x = decode(krom[:N//2], -5, 5)
    # y = decode(krom[N//2:], -5, 5)
    # print(y)
    #   print(x, y)
    return 1 / (h(x, y) + 1)

def print_x_y(krom):
    N = len(krom)

    # print(krom)
    krom_x = krom[0:4]
    krom_y = krom[4:]
    print(krom_x, krom_y)
    
    x = decode(krom_x, -5, 5)
    y = decode(krom_y, -5, 5)
    # x = decode(krom[:N//2], -5, 5)
    # y = decode(krom[N//2:], -5, 5)
    # print(y)
    print("x = {:.2f}\ny = {:.2f}".format(x, y))

def sort_population(population):
    # urutin population dari nilai fitness terbesar, 
    # pake aja sorting manual dengan bandinginnya masukin ke fitness baru ditukar
    return sorted(population, key=lambda krom: fitness(krom))
    # return pop.sort(key=lambda ch: fitness(ch))

def tournament_selection(pop):
    best_parents = []
    # for i in range(2):
    # n = np.random.randint(len(pop))-1
    # print('a')
    # indiv = pop[n]
    # print('b')
    # best_parents.append(indiv)
    # while len(best_parents) < 2:
    #     print('c')
    #     n = np.random.randint(len(pop)-1)
    #     print('d')
    #     indiv = pop[n]
    #     print('e')
    #     if fitness(indiv) > fitness(max(best_parents)):
    #         best_parents.append(indiv)
    #         print('f')  

    # best_parents = sample(pop, 4)
    sort_pop = sort_population(pop)
    best_parents.append(sort_pop[0])
    best_parents.append(sort_pop[1])
    best_parents.append(sort_pop[2])
    best_parents.append(sort_pop[3])
    # print(best_parents)

    return best_parents

def crossover(parents, Pc):
    par_crossover = []
    # print(parents)
    while len(par_crossover) < len(parents):
        cross_prob = np.random.randint(0, 101)
        i = len(par_crossover)
        krom_new = parents[i].copy()
        rndm_i = np.random.randint(len(parents))
        if cross_prob <= Pc and rndm_i != i:
            krom_rndm = parents[rndm_i].copy()
            cross_cut_idx = np.random.randint(len(krom_new))
            krom_new[0:cross_cut_idx], krom_rndm[0:cross_cut_idx] = krom_rndm[0:cross_cut_idx], krom_new[0:cross_cut_idx]
            par_crossover.append(krom_new)

    
    # print(par_crossover)
    return par_crossover

def mutation(child, Pm):
    child_mutasi = []
    for i in range(len(child)):
        prob_mutasi = np.random.randint(0, 101)
        krom = child[i].copy()
        if prob_mutasi <= Pm:
            rand_idx = np.random.randint(len(child))
            krom[rand_idx] = np.random.randint(0, 2)
            child_mutasi.append(krom)
    return child_mutasi
  
def steady_state_survivor(pop, child):
    N = len(child)
    pop_reversed = sort_population(pop)[N:]
    for i in range(N):
        pop.remove(pop_reversed[i])
        pop.append(child[i])
    return pop

# population = [[np.random.randint(2) for i in range(8)] for i in range(8)]
population = []
for i in range(16):
    temp = []
    for j in range(8):
        temp.append(np.random.randint(0, 2))
    population.append(temp)

# print(population)

for i in range(320):
    # fit = [fitness(pop) for pop in population]
    list_fitness = []
    for j in population:
        list_fitness.append(fitness(j))
    print("1")
    random_par = sample(population, 8)
    parents = tournament_selection(random_par)
    print("2")
    childs = crossover(parents, 25)
    print("3")
    childs = mutation(childs, 2)
    print("4")
    population = steady_state_survivor(population, childs)
    print("5")
    print(f"Gen-{i+1}")
    # print(population)
    for k in range(len(population)//2):
        print(population[k], population[k+1])

best = sorted(population, key=fitness)[-1]
print("Kromosom terbaik =", best)
print("Fitness =", fitness(best))
print_x_y(best)