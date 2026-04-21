import random
import math

random.seed(10000)


X_MIN, X_MAX = 0, 50000
Y_MIN, Y_MAX = 0, 50000
def generate_data(n):
    return [
        [random.randint(X_MIN, X_MAX), random.randint(Y_MIN, Y_MAX)]
        for i in range(n)
    ]

class Nodo:
    def __init__(self, x_mid, y_mid):
        self.x_mid = x_mid
        self.y_mid = y_mid
        self.hijos = [None] * 4

class Hoja:
    def __init__(self, punto):
        self.punto = punto

def construir_arbol(puntos, x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX):
    if len(puntos) == 0:
        return None
    if len(puntos) == 1:
        return Hoja(puntos[0])

    x_mid = (x_min + x_max) / 2
    y_mid = (y_min + y_max) / 2

    so = [p for p in puntos if p[0] <  x_mid and p[1] <  y_mid]
    se = [p for p in puntos if p[0] >= x_mid and p[1] <  y_mid]
    no = [p for p in puntos if p[0] <  x_mid and p[1] >= y_mid]
    ne = [p for p in puntos if p[0] >= x_mid and p[1] >= y_mid]

    nodo = Nodo(x_mid, y_mid)
    nodo.hijos[0] = construir_arbol(so, x_min, x_mid, y_min, y_mid)
    nodo.hijos[1] = construir_arbol(se, x_mid, x_max, y_min, y_mid)
    nodo.hijos[2] = construir_arbol(no, x_min, x_mid, y_mid, y_max)
    nodo.hijos[3] = construir_arbol(ne, x_mid, x_max, y_mid, y_max)

    return nodo

def distancia(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def dist_a_bbox(punto, x_min, x_max, y_min, y_max):
    dx = max(x_min - punto[0], 0, punto[0] - x_max)
    dy = max(y_min - punto[1], 0, punto[1] - y_max)
    return math.sqrt(dx**2 + dy**2)

def vecino_mas_cercano(nodo, query, x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX):
    if nodo is None:
        return None, float('inf')
    if isinstance(nodo, Hoja):
        return nodo.punto, distancia(query, nodo.punto)

    bit_x = 1 if query[0] >= nodo.x_mid else 0
    bit_y = 1 if query[1] >= nodo.y_mid else 0
    principal = bit_y * 2 + bit_x
    orden = [principal] + [i for i in range(4) if i != principal]

    bboxes = [
        (x_min,      nodo.x_mid, y_min,      nodo.y_mid),
        (nodo.x_mid, x_max,      y_min,      nodo.y_mid),
        (x_min,      nodo.x_mid, nodo.y_mid, y_max),
        (nodo.x_mid, x_max,      nodo.y_mid, y_max),
    ]

    mejor_punto, mejor_dist = None, float('inf')

    for i in orden:
        if nodo.hijos[i] is None:
            continue
        if dist_a_bbox(query, *bboxes[i]) >= mejor_dist:
            continue
        punto, dist = vecino_mas_cercano(nodo.hijos[i], query, *bboxes[i])
        if dist < mejor_dist:
            mejor_dist = dist
            mejor_punto = punto

    return mejor_punto, mejor_dist

def busqueda_radio(nodo, query, radio, x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX):
    if nodo is None:
        return []
    if isinstance(nodo, Hoja):
        if distancia(query, nodo.punto) <= radio:
            return [nodo.punto]
        return []

    bboxes = [
        (x_min,      nodo.x_mid, y_min,      nodo.y_mid),
        (nodo.x_mid, x_max,      y_min,      nodo.y_mid),
        (x_min,      nodo.x_mid, nodo.y_mid, y_max),
        (nodo.x_mid, x_max,      nodo.y_mid, y_max),
    ]

    resultados = []
    for i, hijo in enumerate(nodo.hijos):
        if hijo is None:
            continue
        if dist_a_bbox(query, *bboxes[i]) > radio:
            continue
        resultados += busqueda_radio(hijo, query, radio, *bboxes[i])

    return resultados


puntos = generate_data(10000)
arbol = construir_arbol(puntos)
target = [5000, 5000]
radio = 500

