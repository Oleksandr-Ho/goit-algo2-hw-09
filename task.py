import random
import math

# Визначення функції Сфери
def sphere_function(x):
    return sum(xi ** 2 for xi in x)

# =========================
# Hill Climbing
# =========================
# Допоміжна функція для визначення сусідів поточної точки (для 2D)
def get_neighbors(current, step_size=0.1):
    x, y = current
    return [
        [x + step_size, y],
        [x - step_size, y],
        [x, y + step_size],
        [x, y - step_size]
    ]

def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    # Ініціалізація початкової точки у межах bounds (для 2D)
    current = [
        random.uniform(bounds[0][0], bounds[0][1]),
        random.uniform(bounds[1][0], bounds[1][1])
    ]
    current_value = func(current)
    step_size = 0.1  # крок для зміни координат

    for _ in range(iterations):
        neighbors = get_neighbors(current, step_size)
        best_neighbor = current
        best_value = current_value

        # Перебір всіх сусідів
        for neighbor in neighbors:
            # Забезпечення знаходження сусіда у межах bounds
            neighbor[0] = max(bounds[0][0], min(neighbor[0], bounds[0][1]))
            neighbor[1] = max(bounds[1][0], min(neighbor[1], bounds[1][1]))
            value = func(neighbor)
            # Оскільки мінімізуємо, шукаємо менше значення
            if value < best_value - epsilon:
                best_neighbor = neighbor
                best_value = value

        # Якщо жодного суттєвого покращення не знайдено, виходимо з циклу
        if best_neighbor == current:
            break

        current = best_neighbor
        current_value = best_value

    return current, current_value

# =========================
# Random Local Search
# =========================
# Допоміжна функція для визначення випадкового сусіда
def get_random_neighbor(current, step_size=0.5, bounds=None):
    neighbor = []
    for i, (lower, upper) in enumerate(bounds):
        new_val = current[i] + random.uniform(-step_size, step_size)
        # Переконуємося, що сусід залишається в межах bounds
        new_val = max(lower, min(new_val, upper))
        neighbor.append(new_val)
    return neighbor

def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    # Початкова точка
    current = [random.uniform(lower, upper) for lower, upper in bounds]
    current_value = func(current)
    step_size = 0.5  # розмір випадкової зміни
    probability = 0.2  # ймовірність прийняття гіршого сусіда

    for _ in range(iterations):
        neighbor = get_random_neighbor(current, step_size, bounds)
        neighbor_value = func(neighbor)

        # Якщо зміна функції менша за epsilon, завершуємо
        if abs(current_value - neighbor_value) < epsilon:
            current = neighbor
            current_value = neighbor_value
            break

        # Приймаємо сусіда, якщо він кращий або з певною ймовірністю
        if neighbor_value < current_value or random.random() < probability:
            current = neighbor
            current_value = neighbor_value

    return current, current_value

# =========================
# Simulated Annealing
# =========================
# Допоміжна функція для генерації сусіда
def generate_neighbor(current, bounds):
    neighbor = []
    for (lower, upper), value in zip(bounds, current):
        new_val = value + random.uniform(-1, 1)
        new_val = max(lower, min(new_val, upper))
        neighbor.append(new_val)
    return neighbor

def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    # Початкова точка
    current = [random.uniform(lower, upper) for lower, upper in bounds]
    current_value = func(current)
    best = current[:]
    best_value = current_value

    for _ in range(iterations):
        # Перевірка температури
        if temp < epsilon:
            break

        neighbor = generate_neighbor(current, bounds)
        neighbor_value = func(neighbor)

        # Якщо зміна значень менша за epsilon, завершуємо алгоритм
        if abs(neighbor_value - current_value) < epsilon:
            current = neighbor
            current_value = neighbor_value
            break

        delta = neighbor_value - current_value
        # Приймаємо сусіда, якщо він кращий або за ймовірністю, залежною від температури
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current = neighbor
            current_value = neighbor_value
            if current_value < best_value:
                best = current[:]
                best_value = current_value

        temp *= cooling_rate  # Охолодження

    return best, best_value

# =========================
# Головна частина програми
# =========================
if __name__ == "__main__":
    # Межі для функції: xi ∈ [−5, 5] для кожного параметра
    bounds = [(-5, 5), (-5, 5)]

    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", sa_value)
