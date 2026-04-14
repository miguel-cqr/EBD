import random
import math
from operator import itemgetter

random.seed(10000)

def generate_data(n):

    return [
        [random.randint(0,10000),random.randint(0,10000)]
        for i in range(1,n+1)
    ] 
class Node:
    def __init__(self,point):
        self.left = None
        self.point = point
        self.right = None

def build_tree(x):
    root = None
    root = insert_node(root, x, 0)
    return root

def insert_node(root, list, axis):
    if not list:
        return None
    list, pos = median(list, axis)
    if(axis==1):
        next_axis = 0
    else:
        next_axis = 1
    point = list[pos]
    if root is None:
        root = Node(point)
    root.left = insert_node(None, list[0:pos], next_axis)
    root.right = insert_node(None, list[pos+1:], next_axis)
    
    return root

def median(array,axis):
    
    if len(array)>1:
        array = sorted(array, key=itemgetter(axis))
        middle = int(len(array) / 2)
    else:
        middle = 0


    return array, middle

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def range_search(node, target, radius, axis=0, results=None):
    if node is None:
        return

    if results is None:
        results = []

    point = node.point

    # Verificar si el punto está dentro del radio
    if distance(point, target) <= radius:
        results.append(point)

    # Decidir hacia dónde ir
    diff = target[axis] - point[axis]

    # lado cercano
    if diff < 0:
        range_search(node.left, target, radius, 1-axis, results)
    else:
        range_search(node.right, target, radius, 1-axis, results)

    # lado lejano (solo si es necesario)
    if abs(diff) <= radius:
        if diff < 0:
            range_search(node.right, target, radius, 1-axis, results)
        else:
            range_search(node.left, target, radius, 1-axis, results)

    return results

def nearest_neighbor(node, target, axis=0, best=None):
    if node is None:
        return best

    point = node.point

    # actualizar mejor
    if best is None or distance(point, target) < distance(best, target):
        best = point

    diff = target[axis] - point[axis]

    # explorar lado cercano primero
    if diff < 0:
        best = nearest_neighbor(node.left, target, 1-axis, best)
        near_branch = node.left
        far_branch = node.right
    else:
        best = nearest_neighbor(node.right, target, 1-axis, best)
        near_branch = node.right
        far_branch = node.left

    # revisar si el otro lado puede tener algo mejor
    if abs(diff) < distance(best, target):
        best = nearest_neighbor(far_branch, target, 1-axis, best)

    return best

