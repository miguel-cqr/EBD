from QuadTree import *
import time

def brute_force_radio(puntos, target, radio):
    resultado = []
    for p in puntos:
        dx = p[0] - target[0]
        dy = p[1] - target[1]
        if (dx*dx + dy*dy) ** 0.5 <= radio:
            resultado.append(p)
    return resultado

def brute_force_vecino(puntos, target):
    mejor = None
    mejor_dist = float('inf')
    for p in puntos:
        dx = p[0] - target[0]
        dy = p[1] - target[1]
        dist = (dx*dx + dy*dy) ** 0.5
        if dist < mejor_dist:
            mejor_dist = dist
            mejor = p
    return mejor

def comparar(n_puntos):
    puntos = generate_data(n_puntos)
    arbol = construir_arbol(puntos)

    target = [5000, 5000]
    radio = 2000

    start = time.time()
    brute_force_radio(puntos, target, radio)
    bf_radio_time = time.time() - start

    start = time.time()
    busqueda_radio(arbol, target, radio)
    qt_radio_time = time.time() - start

    start = time.time()
    brute_force_vecino(puntos, target)
    bf_nn_time = time.time() - start

    start = time.time()
    vecino_mas_cercano(arbol, target)
    qt_nn_time = time.time() - start

    print(f"\n--- {n_puntos} puntos ---")
    print(f"Fuerza bruta radio:       {bf_radio_time:.6f}s")
    print(f"Quadtree radio:           {qt_radio_time:.6f}s")
    print(f"Fuerza bruta más cercano: {bf_nn_time:.6f}s")
    print(f"Quadtree más cercano:     {qt_nn_time:.6f}s")

print("Comparando fuerza bruta vs quadtree...\n")

comparar(5)
comparar(10)
comparar(100)
comparar(1000)
comparar(5000)
comparar(10000)