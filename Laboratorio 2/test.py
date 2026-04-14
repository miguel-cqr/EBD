import matplotlib.pyplot as plt
from KDtree import *

#Visualizacion de los puntos generados
def plot_points(points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    plt.scatter(x, y)
    plt.title("Puntos generados")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

#Visualizacion de los puntos con divisiones del k-d tree

def plot_kdtree(node, min_x, max_x, min_y, max_y, axis=0):
    if node is None:
        return

    x, y = node.point

    if axis == 0:
        # línea vertical
        plt.plot([x, x], [min_y, max_y])

        # izquierda
        plot_kdtree(node.left, min_x, x, min_y, max_y, 1)
        # derecha
        plot_kdtree(node.right, x, max_x, min_y, max_y, 1)

    else:
        # línea horizontal
        plt.plot([min_x, max_x], [y, y])

        # izquierda
        plot_kdtree(node.left, min_x, max_x, min_y, y, 0)
        # derecha
        plot_kdtree(node.right, min_x, max_x, y, max_y, 0)

#Visualización del k-d tree con puntos y divisiones
def visualize_kdtree(points, tree):
    plt.figure()

    # dibujar puntos
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.scatter(x, y)

    # límites del espacio
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)

    # dibujar árbol
    plot_kdtree(tree, min_x, max_x, min_y, max_y)

    plt.title("KD-Tree con particiones")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

# Visualización de la búsqueda en radio con vecinos y vecino más cercano

def visualize_search(points, tree, target, radius):
    # obtener vecinos y vecino más cercano
    neighbors = range_search(tree, target, radius)
    nearest = nearest_neighbor(tree, target)

    # separar puntos
    x_all = [p[0] for p in points]
    y_all = [p[1] for p in points]

    x_neighbors = [p[0] for p in neighbors]
    y_neighbors = [p[1] for p in neighbors]

    # plot base
    plt.figure()

    # todos los puntos
    plt.scatter(x_all, y_all, label="Puntos")

    # vecinos en el radio
    plt.scatter(x_neighbors, y_neighbors, label="Vecinos en radio")

    # punto objetivo
    plt.scatter(target[0], target[1], marker='x', s=100, label="Target")

    # vecino más cercano
    if nearest:
        plt.scatter(nearest[0], nearest[1], marker='D', s=100, label="Más cercano")

    # dibujar círculo del radio
    circle = plt.Circle((target[0], target[1]), radius, fill=False)
    plt.gca().add_patch(circle)

    plt.title("Búsqueda en KD-Tree")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.axis('equal')  # importante para que el círculo no se vea deformado
    plt.show()

# Visualización de la búsqueda en radio con zoom al área del radio

def visualize_full(points, tree, target, radius):
    neighbors = range_search(tree, target, radius)
    nearest = nearest_neighbor(tree, target)

    plt.figure(figsize=(6,6))

    min_x = target[0] - radius
    max_x = target[0] + radius
    min_y = target[1] - radius
    max_y = target[1] + radius

    # 🔥 FILTRAR PUNTOS
    visible_points = [
        p for p in points
        if (min_x <= p[0] <= max_x) and (min_y <= p[1] <= max_y)
    ]

    # dibujar árbol
    plot_kdtree(tree, min_x, max_x, min_y, max_y)

    # puntos visibles
    x_vis = [p[0] for p in visible_points]
    y_vis = [p[1] for p in visible_points]
    plt.scatter(x_vis, y_vis)

    # vecinos
    x_neighbors = [p[0] for p in neighbors]
    y_neighbors = [p[1] for p in neighbors]
    plt.scatter(x_neighbors, y_neighbors)

    # target
    plt.scatter(target[0], target[1], marker='x', s=120)

    # nearest
    if nearest:
        plt.scatter(nearest[0], nearest[1], marker='D', s=120)
        plt.plot([target[0], nearest[0]], [target[1], nearest[1]])

    # círculo
    circle = plt.Circle((target[0], target[1]), radius, fill=False)
    plt.gca().add_patch(circle)

    # zoom real
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.gca().set_aspect('equal')

    plt.show()


x = generate_data(10000)
tree = build_tree(x)
target = [5000, 5000]  #Punto objetivo al que se le encuentra el vecino más cercano y los vecinos dentro del radio
radius = 500 #Radio para la búsqueda de vecinos

#plot_points(x) 

#visualize_kdtree(x, tree)

visualize_search(x, tree, target, radius)

visualize_full(x, tree, target, radius)

