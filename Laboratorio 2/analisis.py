from KDtree import *
import time

#Busqueda de rango usando fuerza bruta
def brute_force_range(points, target, radius):
    result = []

    for p in points:
        dx = p[0] - target[0]
        dy = p[1] - target[1]
        dist = (dx*dx + dy*dy) ** 0.5

        if dist <= radius:
            result.append(p)

    return result
 #Busqueda del vecino más cercano usando fuerza bruta
def brute_force_nn(points, target):
    best = None
    best_dist = float('inf')

    for p in points:
        dx = p[0] - target[0]
        dy = p[1] - target[1]
        dist = (dx*dx + dy*dy) ** 0.5

        if dist < best_dist:
            best_dist = dist
            best = p

    return best

def compare_methods(n_points):
    points = generate_data(n_points)
    tree = build_tree(points)

    target = [5000, 5000]
    radius = 2000


    start = time.time()
    bf_range_res = brute_force_range(points, target, radius)
    bf_range_time = time.time() - start


    start = time.time()
    kd_range_res = range_search(tree, target, radius)
    kd_range_time = time.time() - start


    start = time.time()
    bf_nn_res = brute_force_nn(points, target)
    bf_nn_time = time.time() - start


    start = time.time()
    kd_nn_res = nearest_neighbor(tree, target)
    kd_nn_time = time.time() - start

    print(f"\n--- {n_points} puntos ---")
    print(f"Fuerza Bruta Rango: {bf_range_time:.6f}")
    print(f"KD-Tree Rango: {kd_range_time:.6f}")
    print(f"Fuerza Bruta Vecino mas cercano: {bf_nn_time:.6f}")
    print(f"KD-Tree Vecino mas cercano: {kd_nn_time:.6f}")

print("Comparando métodos con diferentes tamaños de datos...")

compare_methods(5)
compare_methods(10)
compare_methods(100)
compare_methods(1000)
compare_methods(5000)
compare_methods(10000)