import numpy as np

def objetive(x):
    return (-x[0] ** 2) + 5

def generate_neighboors(x, step_size = 0.1):
    return [np.array([x[0] + step_size]), np.array([x[0] - step_size])];

def hill_climbing(objetive, initial, n_iterations = 100, step_size = 0.1):
    current = np.array([initial])
    current_eval = objetive(current)

    for i in range(n_iterations):
        neighbors = generate_neighboors(current, step_size)
        neighbor_evals = [objetive(n) for n in neighbors]

        best_idx = np.argmax(neighbor_evals)
        if neighbor_evals[best_idx] > current_eval:
            current = neighbors[best_idx]
            current_eval = neighbor_evals[best_idx]

            print(f"Step {i+1}; x = {current[0] : .4f}, f(x) = {current_eval: .4f}")

        else:
            print("NO better neighbors found. Algorithm converged.")
            break

    return current, current_eval


initial_guess = 2.0
solution, value = hill_climbing(objetive, initial_guess, n_iterations=100, step_size=0.1)

print(f"\nBest solution x = {solution[0]: .4f}, f(x) = {value: .4f}")
