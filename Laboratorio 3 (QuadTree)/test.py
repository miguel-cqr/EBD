import matplotlib.pyplot as plt
from QuadTree import *

def plot_points(puntos):
    x = [p[0] for p in puntos]
    y = [p[1] for p in puntos]
    plt.scatter(x, y, s=10)
    plt.title("Puntos generados")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def plot_quadtree(nodo, x_min, x_max, y_min, y_max):
    if nodo is None or isinstance(nodo, Hoja):
        return

    # línea vertical y horizontal en el punto de división
    plt.plot([nodo.x_mid, nodo.x_mid], [y_min, y_max], color='gray', linewidth=0.5)
    plt.plot([x_min, x_max], [nodo.y_mid, nodo.y_mid], color='gray', linewidth=0.5)

    plot_quadtree(nodo.hijos[0], x_min,      nodo.x_mid, y_min,      nodo.y_mid)  # SO
    plot_quadtree(nodo.hijos[1], nodo.x_mid, x_max,      y_min,      nodo.y_mid)  # SE
    plot_quadtree(nodo.hijos[2], x_min,      nodo.x_mid, nodo.y_mid, y_max)       # NO
    plot_quadtree(nodo.hijos[3], nodo.x_mid, x_max,      nodo.y_mid, y_max)       # NE

def visualize_quadtree(puntos, arbol):
    plt.figure()
    x = [p[0] for p in puntos]
    y = [p[1] for p in puntos]
    plt.scatter(x, y, s=10)
    plot_quadtree(arbol, 0, 50000, 0, 50000)
    plt.title("Quadtree con particiones")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def visualize_search(puntos, arbol, target, radio):
    vecinos = busqueda_radio(arbol, target, radio)
    cercano, _ = vecino_mas_cercano(arbol, target)

    plt.figure()
    x_all = [p[0] for p in puntos]
    y_all = [p[1] for p in puntos]
    plt.scatter(x_all, y_all, s=10, label="Puntos")

    if vecinos:
        plt.scatter([p[0] for p in vecinos], [p[1] for p in vecinos], s=15, label="Vecinos en radio")

    plt.scatter(target[0], target[1], marker='x', s=20, label="Target")

    if cercano:
        plt.scatter(cercano[0], cercano[1], color='red', s=20, label="Más cercano")

    circle = plt.Circle((target[0], target[1]), radio, fill=False)
    plt.gca().add_patch(circle)

    plt.title("Búsqueda en Quadtree")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.axis('equal')
    plt.show()

def visualize_full(puntos, arbol, target, radio):
    vecinos = busqueda_radio(arbol, target, radio)
    cercano, _ = vecino_mas_cercano(arbol, target)

    x_min = target[0] - radio
    x_max = target[0] + radio
    y_min = target[1] - radio
    y_max = target[1] + radio

    plt.figure(figsize=(6, 6))

    plot_quadtree(arbol, 0, 50000, 0, 50000)

    visibles = [p for p in puntos if x_min <= p[0] <= x_max and y_min <= p[1] <= y_max]
    plt.scatter([p[0] for p in visibles], [p[1] for p in visibles], s=10, label="Puntos")

    if vecinos:
        plt.scatter([p[0] for p in vecinos], [p[1] for p in vecinos], s=15, label="Vecinos en radio")

    plt.scatter(target[0], target[1], marker='x', s=20, label="Target")

    if cercano:
        plt.scatter(cercano[0], cercano[1], color='red', s=20, label="Más cercano")
        plt.plot([target[0], cercano[0]], [target[1], cercano[1]], color='red', linewidth=0.5)

    circle = plt.Circle((target[0], target[1]), radio, fill=False)
    plt.gca().add_patch(circle)

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.show()


def estadisticas_radio(puntos, arbol, target, radio):
    print("\n--- Estadísticas búsqueda por radio ---")

    vecinos = busqueda_radio(arbol, target, radio)
    distancias = [((p[0]-target[0])**2 + (p[1]-target[1])**2)**0.5 for p in vecinos]

    print(f"Radio:                 {radio}")
    print(f"Target:                {target}")
    print(f"Vecinos encontrados:   {len(vecinos)} de {len(puntos)} ({100*len(vecinos)/len(puntos):.2f}%)")
    if distancias:
        print(f"Distancia promedio:    {sum(distancias)/len(distancias):.2f}")
        print(f"Distancia mínima:      {min(distancias):.2f}")
        print(f"Distancia máxima:      {max(distancias):.2f}")
    else:
        print("No se encontraron vecinos en el radio.")

def estadisticas_vecino(arbol, target):
    print("\n--- Estadísticas vecino más cercano ---")

    vecino, dist = vecino_mas_cercano(arbol, target)
    print(f"Target:                {target}")
    print(f"Vecino más cercano:    {vecino}")
    print(f"Distancia:             {dist:.2f}")


puntos = generate_data(10000)
arbol = construir_arbol(puntos)
target = [25000, 25000]
radio = 500

plot_points(puntos)
visualize_quadtree(puntos, arbol)
visualize_search(puntos, arbol, target, radio)
visualize_full(puntos, arbol, target, radio)

estadisticas_radio(puntos, arbol, target, radio)
estadisticas_vecino(arbol, target)