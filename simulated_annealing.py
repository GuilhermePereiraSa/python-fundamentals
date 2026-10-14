import random
import math


current_solution = [0,1,2,3,4]
temperature = 100 # valor maximo, sem os "murros" na mesa, valor q decresce

cities = [(0, 0), (2, 3), (5, 1), (6, 5), (1, 6)]


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def total_distance(route):
    return sum(distance(cities[route[i]], cities[route[(i + 1) % len(route)]]) for i in range(len(route)))
def get_neighbor(solution):
    neighbor = solution[:] # copia inteira

    i, j = random.sample(range(len(solution)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def simulated_annealing(solution, temperature, cooling_rate, iterations):
    current = solution[:]
    current_cost = total_distance(current)

    for _ in range(iterations):
        neighbor = get_neighbor(current)
        neighbor_cost = total_distance(neighbor)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = neighbor
            current_cost = neighbor_cost

        temperature *= cooling_rate

        if temperature < 1e-8:
            break

    return current, current_cost


initial_solution = list(range(len(cities)))

best_solution, best_cost = simulated_annealing(
    initial_solution,
    100,
    0.995,
    1000
)

print("Best Route:", best_solution)
print("Minimum Distance:", best_cost)
