import numpy as np
from random import sample
from random import randint

def h(x, y):
    ''' 
    Untuk mereturn hasil fungsi
    '''
    return ((np.cos(x) + np.sin(y))**2) / x**2 + y**2

def decode(kromosom, r_b, r_a):
    '''
    Untuk mendecode gen pada kromosom dari representasi biner
    '''
    pembagi = 0
    pengali = 0
    for i in range(1, len(kromosom) + 1):
        pembagi += 2 ** -i
        pengali += kromosom[i-1] * (2 ** -i)

    return r_b + ((r_a - r_b) / pembagi) * pengali
  
def fitness(krom):
    '''
    Untuk menghitung nilai fitness dari suatu kromosom
    '''
    krom_x = krom[0:4]
    krom_y = krom[4:]

    x = decode(krom_x, -5, 5)
    y = decode(krom_y, -5, 5)

    return 1 / (h(x, y) + 1)

def print_x_y(krom):
    '''
    Untuk mengoutputkan nilai x dan y hasil decode
    '''
    krom_x = krom[0:4]
    krom_y = krom[4:]
    
    x = decode(krom_x, -5, 5)
    y = decode(krom_y, -5, 5)

    print("x = {:.2f}\ny = {:.2f}".format(x, y))

def sort_population_w_to_b(population):
    '''
    Untuk mensort populasi berdasarkan fitness kromosom dari yang terburuk hingga terbaik
    '''
    return sorted(population, key=lambda krom: fitness(krom))

def sort_population_b_to_w(population):
    '''
    Untuk mensort populasi berdasarkan fitness kromosom dari yang terbaik hingga terburuk
    '''
    return sorted(population, key=lambda krom: fitness(krom), reverse=True)

def tournament_selection(pop):
    '''
    Untuk melakukan tournament selection dengan mengambil 4 kromosom dengan fitness terbaik
    dari sample yang diacak
    '''
    best_parents = []
    sort_pop = sort_population_b_to_w(pop)

    best_parents.append(sort_pop[0])
    best_parents.append(sort_pop[1])
    best_parents.append(sort_pop[2])
    best_parents.append(sort_pop[3])

    return best_parents

def crossover(parents, Pc):
    '''
    Untuk melakukan crossover dari parents yang telah dipilih
    '''
    par_crossover = []
    while len(par_crossover) < len(parents):
        cross_prob = randint(0, 100)
        i = len(par_crossover)
        krom_new = parents[i].copy()
        rndm_i = randint(0, len(parents)-1)
        if cross_prob <= Pc and rndm_i != i:
            krom_rndm = parents[rndm_i].copy()
            cross_cut_idx = randint(0, len(krom_new)-1)
            krom_new[0:cross_cut_idx], krom_rndm[0:cross_cut_idx] = krom_rndm[0:cross_cut_idx], krom_new[0:cross_cut_idx]
            par_crossover.append(krom_new)

    return par_crossover

def mutation(child, Pm):
    '''
    Untuk melakukan mutasi dari hasil crossover
    '''
    child_mutasi = []
    for i in range(len(child)):
        prob_mutasi = randint(0, 100)
        krom = child[i].copy()
        if prob_mutasi <= Pm:
            rand_idx = randint(0, len(child)-1)
            krom[rand_idx] = randint(0, 1)
            child_mutasi.append(krom)
    return child_mutasi
  
def steady_state_survivor(pop, child):
    '''
    Untuk mengambil keturunan yang terbaik kemudian di salin di generasi selanjutnya
    '''
    N = len(child)
    pop_reversed = sort_population_w_to_b(pop)
    for i in range(N):
        pop.remove(pop_reversed[i])
        pop.append(child[i])
    return pop

'''Pengambilan populasi'''
population = []
for i in range(16):
    temp = []
    for j in range(8):
        temp.append(randint(0, 1))
    population.append(temp)

'''Looping tiap generasi'''
for i in range(320):
    random_par = sample(population, 8)
    parents = tournament_selection(random_par)
    childs = crossover(parents, 25)
    childs = mutation(childs, 2)
    population = steady_state_survivor(population, childs)
    print(f"\nGen-{i+1}")
    # print(population)
    for k in range(0, len(population), 2):
        print(population[k], population[k+1])

'''hasil'''
best = sort_population_b_to_w(population)
print("="*50)
print("Kromosom terbaik =", best[0])
print("Fitness =", fitness(best[0]))
print_x_y(best[0])