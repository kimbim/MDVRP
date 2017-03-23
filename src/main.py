import Customer
import Depot
import Chromosome
import random
import copy
from operator import itemgetter
import matplotlib.pyplot as plt

BOUND = 2
POPULATION_SIZE = 200
GENERATION_SPAN = 250
NUM_ELITE = 4
CROSSOVER_PROB = 0.6
INTRA_D_MUTATION_PROB = 0.1

COLORS = ["blue","red","green","purple","black","orange","yellow","pink","turquoise","silver","skyblue","aquamarine","gray","darkblue"]

f = open('../Data/Data Files/2.txt','r')
data= f.readline().split()
m = int(data[0])
n = int(data[1])
t = int(data[2])

depots = []
for i in range(t):
    DQ = f.readline().split()
    depots.append( (int(DQ[0]), int(DQ[1])) )

customers = []
for j in range(n):
    info = f.readline().split()
    i = int(info[0])
    x = int(info[1])
    y = int(info[2])
    q = int(info[4])
    customers.append( Customer.Customer(i,x,y,q) )

for i in range(t):
    info = f.readline().split()
    k = int(info[0])-n
    x = int(info[1])
    y = int(info[2])
    D = depots[i][0]
    Q = depots[i][1]
    depots[i]= Depot.Depot(k,x,y,D,Q,m)

def initial_depot_clustering():
    for c in customers:
        distances = [(d.distance(c,d),d) for d in depots]
        distances.sort(key=itemgetter(0))
        for dist in distances:
            if dist[1].get_load()+c.q <= dist[1].Q*m:
                dist[1].customer_list.append(c)
                break

def alt_init():
    for c in customers:
        random_depot = random.choice(depots)
        random_depot.customer_list.append(c)

def initial_population():
    population = []
    for i in range(POPULATION_SIZE):
        temp_depots = copy.deepcopy(depots)
        for t in temp_depots:
            random.shuffle(t.customer_list)
        print("Creating chromosome " + str(i+1))
        population.append(Chromosome.Chromosome(temp_depots))
    return population

def plot(chromosome):
    for d in chromosome.depots:
        for vehicle in range(len(d.vehicles)):
            route_color = COLORS[vehicle]
            if len(d.vehicles[vehicle]) > 1:
                plt.plot((d.x,d.vehicles[vehicle][0].x),(d.y,d.vehicles[vehicle][0].y),color=route_color, alpha=0.5)
                for i in range(1,len(d.vehicles[vehicle])):
                    plt.plot((d.vehicles[vehicle][i-1].x,d.vehicles[vehicle][i].x),(d.vehicles[vehicle][i-1].y,d.vehicles[vehicle][i].y),\
                        color=route_color, alpha=0.5)
                plt.plot((d.x,d.vehicles[vehicle][-1].x),(d.y,d.vehicles[vehicle][-1].y),color=route_color, alpha=0.5)
            elif len(d.vehicles[vehicle]) == 1:
                plt.plot((d.x,d.vehicles[vehicle][0].x),(d.y,d.vehicles[vehicle][0].y),color=route_color, alpha=0.5)
    plt.plot([c.x for c in chromosome.get_repr()], \
            [c.y for c in chromosome.get_repr()],"k+",mew='1')
    plt.plot([d.x for d in chromosome.depots], \
            [d.y for d in chromosome.depots],"ks",markerfacecolor='none',markersize='8',mew='1')
    plt.show()

def print_sol(chromosome):
    total_customers = 0
    for d in chromosome.depots:
        for vehicle in range(len(d.vehicles)):
            total_customers += len(d.vehicles[vehicle])
            print(str(d.i)+"\t"+str(vehicle+1)+"\t"+str(round(d.route_duration(vehicle),2))+"\t"+ \
                str(d.vehicle_load(vehicle))+"\t"+"0 "+str(d.vehicles[vehicle]).strip("[,]").replace(",","")+" 0")

def run():
    alt_init()
    population = initial_population()
    for generation in range(GENERATION_SPAN):
        fitness = copy.deepcopy([(chrom.fitness(),chrom) for chrom in population])
        fitness.sort(key=itemgetter(0))
        avg_fitness = sum(f[0] for f in fitness)/len(population)
        print("Generation: "+str((generation+1))+" Average fitness: " + str(avg_fitness) + " Best fitness: " + str(fitness[0][0]))
        new_pop = []
        while len(new_pop) < len(population):
            p1 = selection(population)
            p2 = selection(population)
            while p1 == p2:
                p2 = selection(population)
            if random.random() <= CROSSOVER_PROB:
                c1,c2 = crossover(p1,p2)
            else:
                c1,c2 = p1,p2
            if random.random() <= INTRA_D_MUTATION_PROB:
                c1 = intra_d_mutate(c1)
            if random.random() <= INTRA_D_MUTATION_PROB:
                c2 = intra_d_mutate(c2)
            new_pop.append(c1)
            new_pop.append(c2)
        # Elitism
        num_elites = int(POPULATION_SIZE/100)
        if num_elites<1:
            num_elites=1
        for i in range(num_elites):
            new_pop.pop(random.randrange(len(new_pop)))
        for i in range(num_elites):
            new_pop.append(fitness[i][1])
        population = new_pop
    fitness = [(chrom.fitness(),chrom) for chrom in population]
    fitness.sort(key=itemgetter(0))
    best_candidate = fitness[0][1]
    print()
    print()
    print(best_candidate.total_route_duration())
    print_sol(best_candidate)
    plot(best_candidate)

def selection(population):
    first,second = random.sample(population,2)
    r = random.random()
    if r <= 0.8:
        return first if first.fitness() > second.fitness() else second
    else:
        return random.choice([first,second])

def crossover(p1,p2): 
    depot_num = random.randint(0,t-1)
    r1 = random.randint(0,len(p1.depots[depot_num].vehicles)-1)
    route_1=copy.deepcopy(p1.depots[depot_num].vehicles[r1])
    r2 = random.randint(0,len(p2.depots[depot_num].vehicles)-1)
    route_2=copy.deepcopy(p2.depots[depot_num].vehicles[r2])
    p1_add = []
    p2_add = []
    for c in route_1:
        to_delete = None
        for d in p2.depots:
            for vehicle in range(len(d.vehicles)):
                for customer in d.vehicles[vehicle]:
                    if c.i == customer.i:
                        to_delete = (d.i,vehicle,customer)
                        break
        p2.depots[to_delete[0]-1].vehicles[to_delete[1]].remove(to_delete[2])
        p2_add.append(to_delete[2])
        p2.depots[to_delete[0]-1].update_customer_list()
    for c in route_2:
        to_delete = None
        for d in p1.depots:
            for vehicle in range(len(d.vehicles)):
                for customer in d.vehicles[vehicle]:
                    if c.i == customer.i:
                        to_delete = (d.i,vehicle,customer)
                        break
        p1.depots[to_delete[0]-1].vehicles[to_delete[1]].remove(to_delete[2])
        p1_add.append(to_delete[2])
        p1.depots[to_delete[0]-1].update_customer_list()
    for c in p2_add:
        ordered_list = []
        for vehicle in range(len(p2.depots[depot_num].vehicles)):
            for spot in range(len(p2.depots[depot_num].vehicles[vehicle])+1):
                duration_before = p2.depots[depot_num].route_duration(vehicle)
                p2.depots[depot_num].vehicles[vehicle].insert(spot,c)
                duration_after = p2.depots[depot_num].route_duration(vehicle)
                insertion_cost = duration_after-duration_before
                load = p2.depots[depot_num].vehicle_load(vehicle)
                p2.depots[depot_num].vehicles[vehicle].remove(c)
                feasible = False
                if duration_after <= p2.depots[depot_num].D and load <= p2.depots[depot_num].Q:
                    feasible = True
                ordered_list.append((insertion_cost,vehicle,spot,c,feasible))
        ordered_list.sort(key=itemgetter(0))
        k = random.random()
        if k <= 0.8:
            selected = next((obj for obj in ordered_list if obj[4] == True),False)
            if selected == False:
                p2.depots[depot_num].vehicles.append([c])
            else:
                p2.depots[depot_num].vehicles[selected[1]].insert(selected[2],selected[3])
        else:
            p2.depots[depot_num].vehicles[ordered_list[0][1]].insert(ordered_list[0][2],ordered_list[0][3])
    p2.depots[depot_num].update_customer_list()
    for c in p1_add:
        ordered_list = []
        for vehicle in range(len(p1.depots[depot_num].vehicles)):
            for spot in range(len(p1.depots[depot_num].vehicles[vehicle])+1):
                duration_before = p1.depots[depot_num].route_duration(vehicle)
                p1.depots[depot_num].vehicles[vehicle].insert(spot,c)
                duration_after = p1.depots[depot_num].route_duration(vehicle)
                insertion_cost = duration_after-duration_before
                load = p1.depots[depot_num].vehicle_load(vehicle)
                p1.depots[depot_num].vehicles[vehicle].remove(c)
                feasible = False
                if duration_after <= p1.depots[depot_num].D and load <= p1.depots[depot_num].Q:
                    feasible = True
                ordered_list.append((insertion_cost,vehicle,spot,c,feasible))
        ordered_list.sort(key=itemgetter(0))
        k = random.random()
        if k <= 0.8:
            selected = next((obj for obj in ordered_list if obj[4] == True),False)
            if selected == False:
                p1.depots[depot_num].vehicles.append([c])
            else:
                p1.depots[depot_num].vehicles[selected[1]].insert(selected[2],selected[3])
        else:
            p1.depots[depot_num].vehicles[ordered_list[0][1]].insert(ordered_list[0][2],ordered_list[0][3])
    p1.depots[depot_num].update_customer_list()
    for d in p1.depots:
        p1.depots[d.i-1].vehicles = [x for x in p1.depots[d.i-1].vehicles if x != []]
    for d in p2.depots:
        p2.depots[d.i-1].vehicles = [x for x in p2.depots[d.i-1].vehicles if x != []]
    return p1,p2

def intra_d_mutate(child): #Reversal mutation
    depot_num = random.randint(0,t-1)
    left = random.randint(0,len(child.depots[depot_num].customer_list)-2)
    right = random.randint(left+2,len(child.depots[depot_num].customer_list))
    sublist = child.depots[depot_num].customer_list[left:right]
    sublist.reverse()
    child.depots[depot_num].customer_list[left:right] = sublist
    child.depots[depot_num].update_routes()
    return child

run()