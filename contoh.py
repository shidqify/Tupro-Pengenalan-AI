import numpy as np

h = lambda x, y: ((np.cos(x) + np.sin(y))**2) / x**2 + y**2

def decode(ch, r_min, r_max):
  exp = [2 ** -i for i in range(1, len(ch) + 1)]
  g_exp = sum(g * e for g, e in zip(ch, exp))
  return r_min + (r_max - r_min) / sum(exp) * g_exp
  
def fitness(ch):
  N = len(ch)
  x = decode(ch[:N//2], -5, 5)
  y = decode(ch[N//2:], -5, 5)
  return h(x, y)

def urut_populasi(pop):
    return sorted(pop, key=lambda ch: fitness(ch))

def tournament(pop, k):
  best = []
  for i in range(k):
    indv = pop[np.random.randint(len(pop))-1]
    if len(best) == 0 or fitness(indv) > fitness(max(best)):
      best.append(indv)
    return best

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
            ch_new[0:cross_idx], ch_rand[0:cross_idx] = ch_rand[0:cross_idx], ch_new[0:cross_idx]
            ch_new[cross_idx:N], ch_rand[cross_idx:N] = ch_rand[cross_idx:N], ch_new[cross_idx:N]
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
    pop_worst = urut_populasi(pop)[N:]
    for i in range(N):
        pop.remove(pop_worst[i])
        pop.append(keturunan[i])
    return pop

populasi = [[np.random.randint(2) for i in range(8)] for i in range(64)]
for i in range(320):
    fit = [fitness(pop) for pop in populasi]
    OrangTua = tournament(populasi, 2)
    Keturunan = persilangan(OrangTua, 25)
    Keturunan = mutasi(Keturunan, 2)
    populasi = steady_state(populasi, Keturunan)
    print("-"*10,"Generasi",i+1,"-"*10)
    print(populasi)

best = sorted(populasi, key=fitness)[-1]
print('Kromosom terbaik =', best, 'dengan nilai fitness sebesar', fitness(best))