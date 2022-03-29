import numpy as np

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
    return r_b + ((r_a - r_b) // pembagi) * pengali
  
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
    return 1/(h(x, y) + 1)

def Pfitness(krom):
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
    print(x, y)

def sort_population(populasi):
    # urutin populasi dari nilai fitness terbesar, 
    # pake aja sorting manual dengan bandinginnya masukin ke fitness baru ditukar
    return sorted(populasi, key=lambda krom: fitness(krom))
    # return pop.sort(key=lambda ch: fitness(ch))

def tournament_selection(pop):
    best_parents = []
    # for i in range(2):
    n = np.random.randint(len(pop))-1
    indiv = pop[n]
    if len(best_parents) == 0 or fitness(indiv) > fitness(max(best_parents)):
        best_parents.append(indiv)
    while len(best_parents) <= 2:
        n = np.random.randint(len(pop))-1
        indiv = pop[n]
        if fitness(indiv) > fitness(max(best_parents)):
            best_parents.append(indiv)

    return best_parents

def persilangan(pop, probCross):
    N = len(pop[0])
    pop_cross = []
    while len(pop_cross) < len(pop):
        cross_prob = np.random.randint(0, 101)
        i = len(pop_cross)
        ch_new = pop[i].copy()
        rand_i = np.random.randint(len(pop))
        if cross_prob <= probCross and rand_i != i:
            ch_rand = pop[rand_i].copy()
            cross_idx = np.random.randint(len(ch_new))
            # yg bawah kyknya cuma perlu 1 aja yg atas, soalnya ini bakal hasilnya cuma tuker tempat doang
            ch_new[0:cross_idx], ch_rand[0:cross_idx] = ch_rand[0:cross_idx], ch_new[0:cross_idx]
            # ch_new[cross_idx:N], ch_rand[cross_idx:N] = ch_rand[cross_idx:N], ch_new[cross_idx:N]
        pop_cross.append(ch_new)
    return pop_cross

def mutasi(pop, probMutasi):
    pop_mutasi = []
    N = len(pop[0])
    for i in range(len(pop)):
        prob_mutasi = np.random.randint(0, 101)
        ch = pop[i].copy()
        if prob_mutasi <= probMutasi:
            rand_i = np.random.randint(len(pop))
            ch[rand_i] = int(np.floor(np.random.random()))
        pop_mutasi.append(ch)
    return pop_mutasi
  
def steady_state(pop, keturunan):
    N = len(keturunan)
    pop_worst = sort_population(pop)[N:]
    for i in range(N):
        pop.remove(pop_worst[i])
        pop.append(keturunan[i])
    return pop

populasi = [[np.random.randint(2) for i in range(8)] for i in range(64)]
for i in range(1):
    fit = [fitness(pop) for pop in populasi]
    OrangTua = tournament_selection(populasi)
    Keturunan = persilangan(OrangTua, 25)
    Keturunan = mutasi(Keturunan, 2)
    populasi = steady_state(populasi, Keturunan)
    print("-"*10,"Generasi",i+1,"-"*10)
    print(populasi)

best = sorted(populasi, key=fitness)[-1]
print('Kromosom terbaik =', best, 'dengan nilai fitness sebesar', fitness(best))
Pfitness(best)
# N = len(best)
# print(decode(best[:N//2], -5, 5))
# print(decode(best[N//2], -5, 5))